import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, renderHook } from '@testing-library/react';
import { boundaryService, localizationService, mdmsService } from '@/api';
import type { Boundary } from '@/api/types';
import { saveBoundaryDraft, setBoundaryDraft, useBoundaryDraft, type BoundaryDraft } from './boundaryDraft';

vi.mock('@/api', () => ({
  ApiClientError: class ApiClientError extends Error {},
  apiClient: { getAuth: () => ({ token: null }) },
  boundaryService: {
    createHierarchyFromLevels: vi.fn(),
    getHierarchies: vi.fn(),
    createBoundaries: vi.fn(),
  },
  mdmsService: { ensureHierarchySchema: vi.fn(async () => undefined), upsertMapConfig: vi.fn(async () => undefined) },
  localizationService: {
    uploadBoundaryLocalizations: vi.fn(async () => ({ success: 1, failed: 0 })),
    uploadHierarchyLevelLocalizations: vi.fn(async () => ({ success: 1, failed: 0 })),
    cacheBust: vi.fn(async () => undefined),
  },
}));
vi.mock('../labelLocales', () => ({ labelLocales: vi.fn(async () => ['en_IN']) }));
vi.mock('../telemetry', () => ({ trackStepAction: vi.fn(), reportStepError: vi.fn() }));

const createHierarchy = vi.mocked(boundaryService.createHierarchyFromLevels);
const getHierarchies = vi.mocked(boundaryService.getHierarchies);
const createBoundaries = vi.mocked(boundaryService.createBoundaries);
const ensureSchema = vi.mocked(mdmsService.ensureHierarchySchema);
const boundaryLabels = vi.mocked(localizationService.uploadBoundaryLocalizations);

const area = (code: string, boundaryType: string, parent?: string): Boundary => ({
  tenantId: 'ke.nairobi',
  code,
  name: code,
  boundaryType,
  parent,
  hierarchyType: 'ADMIN',
});
const AREAS = [area('KE', 'County'), area('KE_W1', 'Ward', 'KE'), area('KE_W2', 'Ward', 'KE')];

const draft = (over: Partial<BoundaryDraft> = {}): BoundaryDraft => ({
  source: 'osm',
  hierarchyType: 'ADMIN',
  levels: ['County', 'Ward'],
  hierarchyExists: false,
  boundaries: AREAS,
  sourceText: 'the official boundaries for Kenya (OCHA COD-AB)',
  skipped: 0,
  attribution: null,
  preconfigured: null,
  resume: {
    kind: 'osm',
    searchTerm: 'Nairobi',
    pickedSuggestion: null,
    turbopassSource: 'official',
    fetchedPlace: { id: 'p1', name: 'Nairobi', label: 'Nairobi, Kenya', country: 'Kenya' },
    adminLevels: [],
    attribution: null,
    officialSet: null,
  },
  ...over,
});

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal('fetch', vi.fn(async () => new Response(null, { status: 204 })));
  createHierarchy.mockResolvedValue({ tenantId: 'ke.nairobi', hierarchyType: 'ADMIN', boundaryHierarchy: [] });
  createBoundaries.mockImplementation(async (boundaries) => ({ success: boundaries, failed: [] }));
});

describe('the draft store', () => {
  it('keeps one draft per workspace until it is cleared', () => {
    const nairobi = renderHook(() => useBoundaryDraft('ke.nairobi'));
    const maputo = renderHook(() => useBoundaryDraft('mz.maputo'));
    expect(nairobi.result.current).toBeNull();

    const chosen = draft();
    act(() => setBoundaryDraft('ke.nairobi', chosen));
    expect(nairobi.result.current).toBe(chosen);
    expect(maputo.result.current).toBeNull();

    act(() => setBoundaryDraft('ke.nairobi', null));
    expect(nairobi.result.current).toBeNull();
  });
});

describe('saveBoundaryDraft', () => {
  it('creates the hierarchy, then its areas, then the hierarchy record', async () => {
    const result = await saveBoundaryDraft('ke.nairobi', draft());
    expect(createHierarchy).toHaveBeenCalledWith('ke.nairobi', 'ADMIN', ['County', 'Ward']);
    expect(createBoundaries).toHaveBeenCalledWith(AREAS);
    expect(ensureSchema).toHaveBeenCalledWith('ke.nairobi', { hierarchy: 'ADMIN', highestHierarchy: 'County', lowestHierarchy: 'Ward' });
    expect(boundaryLabels).toHaveBeenCalledOnce();
    expect(result).toEqual({ created: AREAS, failed: [], schemaError: null });
  });

  it('leaves an existing hierarchy definition alone', async () => {
    await saveBoundaryDraft('ke.nairobi', draft({ hierarchyExists: true }));
    expect(createHierarchy).not.toHaveBeenCalled();
    expect(createBoundaries).toHaveBeenCalledOnce();
  });

  it('carries on when the hierarchy was already defined with the same levels', async () => {
    createHierarchy.mockRejectedValue(new Error('Hierarchy definition already exists'));
    getHierarchies.mockResolvedValue([
      { tenantId: 'ke.nairobi', hierarchyType: 'ADMIN', boundaryHierarchy: [{ boundaryType: 'County', active: true }, { boundaryType: 'Ward', active: true }] },
    ]);
    await saveBoundaryDraft('ke.nairobi', draft());
    expect(createBoundaries).toHaveBeenCalledOnce();
  });

  it('writes no area when an existing hierarchy has other levels', async () => {
    createHierarchy.mockRejectedValue(new Error('DUPLICATE_RECORD'));
    getHierarchies.mockResolvedValue([
      { tenantId: 'ke.nairobi', hierarchyType: 'ADMIN', boundaryHierarchy: [{ boundaryType: 'Province', active: true }, { boundaryType: 'Ward', active: true }] },
    ]);
    await expect(saveBoundaryDraft('ke.nairobi', draft())).rejects.toThrow(/\[Province → Ward\], which do not match yours \[County → Ward\]/);
    expect(createBoundaries).not.toHaveBeenCalled();
  });

  it('writes nothing alongside the areas when none of them landed', async () => {
    createBoundaries.mockResolvedValue({ success: [], failed: AREAS.map((boundary) => ({ boundary, error: 'refused' })) });
    const result = await saveBoundaryDraft('ke.nairobi', draft());
    expect(result.created).toEqual([]);
    expect(result.failed).toHaveLength(3);
    expect(ensureSchema).not.toHaveBeenCalled();
    expect(boundaryLabels).not.toHaveBeenCalled();
  });

  it('reports a hierarchy record that did not save, with the areas that did', async () => {
    ensureSchema.mockRejectedValue(new Error('MDMS down'));
    const result = await saveBoundaryDraft('ke.nairobi', draft());
    expect(result.created).toEqual(AREAS);
    expect(result.schemaError).toBe("Boundaries were saved, but the hierarchy record didn't save: MDMS down");
  });
});
