import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import type { Boundary } from '@/api/types';
import type { BoundaryDraft } from './boundaryDraft';
import { BoundaryDraftCard } from './BoundaryDraftCard';

const area = (code: string, boundaryType: string): Boundary => ({
  tenantId: 'lr.monrovia',
  code,
  name: code,
  boundaryType,
  hierarchyType: 'ADMIN',
});

const draft: BoundaryDraft = {
  source: 'osm',
  hierarchyType: 'ADMIN',
  levels: ['Country', 'County', 'District'],
  hierarchyExists: false,
  boundaries: [area('LR', 'Country'), area('C1', 'County'), area('C2', 'County'), area('D1', 'District')],
  sourceText: 'the official boundaries for Liberia (OCHA COD-AB)',
  skipped: 2,
  attribution: 'Boundary data: OCHA COD-AB',
  preconfigured: null,
  resume: {
    kind: 'excel',
    hierarchy: { tenantId: 'lr.monrovia', hierarchyType: 'ADMIN', boundaryHierarchy: [] },
    file: null,
    parsed: [],
    valid: [],
    invalid: [],
    polygonFile: null,
    polygonSidecar: null,
  },
};

describe('BoundaryDraftCard', () => {
  it('shows the unsaved selection level by level', () => {
    render(<BoundaryDraftCard draft={draft} onEdit={vi.fn()} onRemove={vi.fn()} />);
    expect(screen.getByText('Not saved yet')).toBeTruthy();
    expect(screen.getByText('4 areas from the official boundaries for Liberia (OCHA COD-AB).')).toBeTruthy();
    const rows = screen.getAllByRole('row').map((r) => r.textContent);
    expect(rows).toEqual(['LevelAreas', '1Country1', '2County2', '3District1', 'Total4']);
    expect(screen.getByText(/2 areas were left out/)).toBeTruthy();
    expect(screen.getByTestId('boundary-attribution').textContent).toBe('Boundary data: OCHA COD-AB');
  });

  it('reopens the choice for Edit', () => {
    const onEdit = vi.fn();
    render(<BoundaryDraftCard draft={draft} onEdit={onEdit} onRemove={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(onEdit).toHaveBeenCalledOnce();
  });

  it('removes the selection only once confirmed', () => {
    const onRemove = vi.fn();
    render(<BoundaryDraftCard draft={draft} onEdit={vi.fn()} onRemove={onRemove} />);
    fireEvent.click(screen.getByRole('button', { name: /remove/i }));
    expect(onRemove).not.toHaveBeenCalled();
    expect(screen.getByText('Remove these boundaries?')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Delete' }));
    expect(onRemove).toHaveBeenCalledOnce();
  });

  it('cannot be changed while it is being saved', () => {
    render(<BoundaryDraftCard draft={draft} onEdit={vi.fn()} onRemove={vi.fn()} disabled />);
    expect((screen.getByRole('button', { name: /edit/i }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole('button', { name: /remove/i }) as HTMLButtonElement).disabled).toBe(true);
  });
});
