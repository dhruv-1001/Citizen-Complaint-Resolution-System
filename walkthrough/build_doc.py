#!/usr/bin/env python3
"""Render docs/digit-ui-walkthrough.md from the captured screenshots.

The markdown is a flat, GitHub-renderable version of what output/index.html and
output/gallery.html show interactively: every screenshot, in flow order, with a
caption, plus the findings the capture turned up.

Section order and per-shot captions live in this file; the image list comes from
the capture itself, so a re-capture that adds or drops a screen is picked up by
re-running this script.

    .venv/bin/python build_doc.py
"""
from __future__ import annotations

import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "en"
DOC = HERE.parent / "docs" / "digit-ui-walkthrough.md"
REL = "../walkthrough/output/en"

CAPTURED = "2026-08-24"

# flow dir -> (heading, intro prose)
SECTIONS = [
    ("01_login", "Configurator · Sign In",
     "`/configurator/login`. One form, one switch: **Onboarding** drives the 4-phase provisioning "
     "wizard, **Management** drives the react-admin console. Both authenticate against the root "
     "(state-level) tenant, `ke`. The `?` next to Tenant Code is a native tooltip, not a screen."),

    ("02_phase1_tenant", "Onboarding · Phase 1 — Tenant & Branding",
     "Two ways out of the landing screen: reuse a tenant that already exists, or upload a Tenant "
     "Master workbook. The workbook is parsed **in the browser**, so the preview screens below cost "
     "the deployment nothing — the sample file describes Maputo, which is why the preview shows "
     "`mz.maputo` rather than Bomet. Everything past **Upload to DIGIT** (branding, the image "
     "preview modal, the Phase 1 summary) writes, and is listed as not captured in the "
     "[screen inventory](#screen-inventory-against-the-product-doc)."),

    ("03_phase2_boundary", "Onboarding · Phase 2 — Boundary Setup",
     "The widest phase, and **both of its paths are captured below**.\n\n"
     "The **Upload from Excel** path (shots 2–11) picks or defines a hierarchy, hands you a "
     "template shaped to that hierarchy's levels, then validates the filled workbook row by row, "
     "with an optional GeoJSON sidecar for real map outlines.\n\n"
     "The **Fetch from OpenStreetMap** path (shots 12–16) types an area into the Nominatim "
     "typeahead, pulls that relation's administrative levels from Overpass, and asks you to include "
     "and name each one. `Cidade de Maputo` is used here because it resolves to a clean "
     "three-level hierarchy — one city, six *distritos municipais*, sixty-three *bairros* — all "
     "three included and named.\n\n"
     "Both paths stop at the same wall: the button that creates the hierarchy and the boundaries."),

    ("04_phase3_masters", "Onboarding · Phase 3 — Common Masters",
     "Departments, designations and complaint types from one workbook. Upload and preview are "
     "client-side; **Create & Continue** writes, so the complaint-hierarchy step behind it is not "
     "captured."),

    ("05_phase4_employees", "Onboarding · Phase 4 — Employee Onboarding",
     "Phase 4 is **blocked on this deployment** — its reference load reports *No boundaries found "
     "for tenant \"ke\"*, which disables **Start Phase 4** and hides the template generator behind "
     "it. Why that happens is [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-"
     "hierarchies). The file input is rendered outside the step, so the employee workbook can still "
     "be parsed and its per-row validation captured."),

    ("06_onboarding_complete", "Onboarding · Complete",
     "The end-of-wizard summary: live tenant totals, links into the employee and citizen apps, and "
     "three buttons. **View Setup History** has no `onClick` handler in "
     "`configurator/src/pages/CompletePage.tsx` — it renders and does nothing."),

    ("07_home", "Configurator · Management console",
     "The react-admin console. Home counts every registry; **Advanced** exposes every generic MDMS "
     "master the data provider knows about."),

    ("08_tenant", "Configurator · Tenant, boundaries & map",
     "Tenant registry, boundary hierarchy definitions, boundary records and the per-tenant map "
     "configuration, plus the boundary create form (filled, never submitted)."),

    ("09_complaints", "Configurator · Complaints & localization",
     "The complaint registry and the masters behind it — complaint types, the category/sub-type "
     "hierarchy, and the localization messages that label them in the citizen and employee apps."),

    ("10_people", "Configurator · People & org structure",
     "Departments, designations, employees, users and the org chart, plus the two bulk-import "
     "surfaces and the department/employee create forms."),

    ("11_system", "Configurator · System (roles, workflow, MDMS)",
     "Access roles, the PGR workflow business service (the state machine every complaint runs "
     "through), live workflow process instances, and the MDMS v2 schema registry."),

    ("12_notifications", "Configurator · Notifications",
     "Routing configuration, templates, provider templates, the delivery log from the Novu bridge, "
     "configured providers, and per-user preferences."),

    ("13_dashboards", "Configurator · Public dashboard",
     "Anonymous, credential-free access to the tenant's dashboard, and the stable URL it is shared "
     "under. `/manage/pgr-dashboard` exists in `configurator/src/App.tsx` but not in the bundle "
     "bomet serves — that route falls back to the console home."),

    ("14_employee_login", "Employee UI · Sign In",
     "`/digit-ui/employee`. City picker, credentials, privacy consent. Tenant `ke` is the only "
     "selection that authenticates, because `ADMIN` exists only there — and since the cleanup the "
     "picker labels it **Ke**, not *Bomet County*. Its MDMS record still reads `Bomet County`, so "
     "this is digit-ui falling back to a prettified tenant code when the label's localization "
     "message is missing, not lost data."),

    ("15_employee_inbox", "Employee UI · Complaint inbox",
     "Inbox v2 with its search panel and filter rail, and the legacy inbox behind it. It opens on "
     "**My Complaints**, which is empty for `ADMIN` — the deployment's complaints belong to other "
     "employees, and **All Complaints** is the tab that shows them."),

    ("16_employee_complaint_detail", "Employee UI · Complaint detail & workflow",
     "One complaint opened from the inbox: the detail card, and the workflow history below the "
     "fold. Opening a complaint is a read; none of the action buttons on it were clicked."),

    ("17_employee_new_complaint", "Employee UI · New complaint intake",
     "The counter-staff intake form: complainant details, the complaint type → category → sub-type "
     "cascade, a Leaflet map pin, and a description. Filled in for the capture and **not** "
     "submitted."),

    ("18_employee_search", "Employee UI · Search complaint",
     "The Search Complaint entry point from the home screen."),
]

# label (filename minus the NN_ prefix and .png) -> caption
SHOTS = {
    "signin_blank": "The sign-in form as it loads",
    "signin_filled_onboarding_mode": "Filled, Onboarding mode selected",
    "signin_filled_management_mode": "Filled, Management mode selected",

    "p1_landing": "Phase 1 landing. Tenants already exist under `ke`, so the skip-ahead banner offers to reuse one",
    "p1_select_existing_tenant": "Use Existing Tenant. Picking a row jumps to Phase 2 without creating anything",
    "p1_upload_tenant_master": "Step 1.1 — the Tenant Master dropzone",
    "p1_preview_tenant_info": "Preview, Tenant Info tab: the parsed row and exactly what creating it would do",
    "p1_preview_branding_details": "Preview, Branding Details tab",
    "p1_change_file_back_to_upload": "**← Change File** returns to the dropzone",

    "p2_landing_choose_source": "Choose the boundary source: OpenStreetMap or Excel",
    "p2_excel_choose_path": "Excel path — define a new hierarchy or reuse an existing one",
    "p2_create_hierarchy_blank": "Define Hierarchy — name plus an ordered, contiguous level list",
    "p2_create_hierarchy_filled": "The same form filled in. **Create Hierarchy** writes, so it was not clicked",
    "p2_select_existing_hierarchy": "Select Existing Hierarchy — every entry offered is a `PW_*` test leftover; the real `ADMIN` hierarchy is the 273rd definition at this tenant and the screen only asks for the first 100 (see [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies))",
    "p2_hierarchy_selected": "A hierarchy selected",
    "p2_download_template": "Boundary Data Upload — the template is generated for the chosen hierarchy's levels",
    "p2_verify_all": "Verify Boundary Data, All tab — every row of the sample workbook, parsed in the browser",
    "p2_verify_valid": "Valid tab",
    "p2_verify_errors": "Errors tab — empty for this file",
    "p2_verify_with_geojson": "With the optional GeoJSON sidecar attached — it reports how many boundaries it can give real outlines to",
    "p2_osm_search": "OSM path — search the area to import",
    "p2_osm_search_typeahead": "The Nominatim typeahead resolving *Cidade de Maputo/Mozambique*; picking a suggestion scopes the Overpass lookup to that exact relation",
    "p2_osm_search_typed": "Suggestion picked, ready to search",
    "p2_osm_map_levels": "Map Admin Levels — the three levels Overpass returned: 1 city (level 4), 6 distritos municipais (level 5), 63 bairros (level 8)",
    "p2_osm_levels_selected": "All three levels included",
    "p2_osm_levels_named": "Each level named — *Município → Distrito Municipal → Bairro*. The selection is now valid and **Create Hierarchy & Boundaries** is enabled; that click writes, so this is where the capture stops",

    "p3_landing": "Phase 3 landing",
    "p3_upload_common_master": "Common Master dropzone",
    "p3_preview_departments_designations": "Parsed departments and designations with per-row validation",

    "p4_landing": "Phase 4 landing. Note the contradiction: *Prerequisites Met — Phase 2: Boundaries configured*, directly under *No boundaries found for tenant \"ke\"*",
    "p4_preview_validation": "Per-row employee validation. Every row fails on the missing boundary, so **Create Employees** stays disabled and the confirmation dialog behind it is unreachable",

    "complete_summary": "The completion summary",

    "dashboard_home": "Management console home",
    "advanced_all_masters": "Advanced — every generic MDMS master",

    "tenants_list": "Tenant registry",
    "boundary_hierarchies_list": "Boundary hierarchy definitions",
    "boundary_hierarchies_detail": "One hierarchy in detail",
    "boundaries_list": "Boundary records",
    "boundaries_detail": "One boundary in detail",
    "map_configuration": "Map Configuration — centre, zoom and tiles per tenant",
    "boundary_create_blank": "Boundary create form, blank",
    "boundary_create_filled": "The same form filled in — never submitted",

    "complaints_list": "Complaint registry",
    "complaint_types_list": "Complaint Types",
    "complaint_types_detail": "One complaint type in detail",
    "complaint_hierarchies_list": "Complaint Hierarchies",
    "complaint_hierarchies_detail": "The PGR hierarchy in detail",
    "localization_messages_list": "Localization messages",
    "localization_messages_detail": "One message in detail",

    "departments_list": "Departments",
    "departments_detail": "One department in detail",
    "designations_list": "Designations",
    "designations_detail": "One designation in detail",
    "employees_list": "Employees",
    "employees_detail": "One employee in detail",
    "org_chart": "Org chart",
    "users_list": "Users",
    "users_detail": "One user in detail",
    "employees_bulk_import": "Employee bulk import",
    "localization_bulk_import": "Localization bulk import",
    "department_create_blank": "Department create form, blank",
    "department_create_filled": "The same form filled in — never submitted",
    "employee_create_blank": "Employee create form, blank",
    "employee_create_filled": "The same form filled in — never submitted",

    "access_roles_list": "Access roles",
    "access_roles_detail": "One role in detail",
    "workflows_list": "Workflow business services",
    "workflows_detail": "The PGR state machine in detail",
    "processes_list": "Workflow process instances",
    "mdms_schemas_list": "MDMS v2 schemas",
    "mdms_schemas_detail": "One schema in detail",

    "notification_configure": "Notification routing configuration",
    "notification_routing": "Notification Routing rules",
    "notification_templates": "Notification templates",
    "provider_templates_whatsapp": "Provider templates (WhatsApp)",
    "notification_logs": "Delivery log from the Novu bridge",
    "notification_providers": "Configured providers",
    "notification_providers_detail": "One provider in detail",
    "user_preferences": "Per-user notification preferences",

    "public_dashboard_configure": "Public dashboard configuration",

    "employee_signin_blank": "The employee sign-in screen",
    "employee_city_picker": "The city picker — six tenants, `ke` among them as *Ke*",
    "employee_signin_filled": "Filled, with privacy consent ticked",
    "employee_home": "Employee home. Only PGR is enabled here",

    "inbox_v2_my_complaints": "Inbox v2 as it opens — search panel, filter rail, and the **My Complaints** tab, empty for this operator",
    "inbox_v2_all_complaints": "The **All Complaints** tab: complaint number, locality, status, current owner and SLA days remaining",
    "inbox_v1_legacy": "The legacy inbox",

    "complaint_detail": "A complaint opened from the inbox: category, sub-type, jurisdiction, status, description and map pin",
    "complaint_workflow_timeline": "The complaint timeline below it — applied, assigned, then auto-escalated on an SLA breach",

    "create_complaint_blank": "The intake form as it loads",
    "dropdown_category_open": "Complaint category picker open",
    "dropdown_county_open": "County picker open",
    "create_complaint_filled_not_submitted": "Filled in and left there — SUBMIT was never clicked",

    "search_complaint_entry": "Search Complaint from the home screen — the same inbox surface, opened on its search panel",
}


def slug(heading: str) -> str:
    """GitHub's heading-anchor slug: lowercase, drop punctuation, spaces to hyphens.

    It does NOT collapse the run of hyphens left behind by a removed `·`, which
    is why the anchors below carry double hyphens.
    """
    s = heading.lower()
    s = re.sub(r"[^a-z0-9 _-]", "", s)
    return s.replace(" ", "-")


def label_of(png: Path) -> str:
    return re.sub(r"^\d+_", "", png.stem)


def console_counts() -> dict[str, str]:
    """Registry counts as the management console reported them in this capture.

    The dashboard renders each tile as a number followed by its label, so the
    findings below can quote live numbers instead of ones that rot between runs.
    """
    txt = OUT / "07_home" / "01_dashboard_home.txt"
    if not txt.exists():
        return {}
    lines = [ln.strip() for ln in txt.read_text().splitlines() if ln.strip()]
    out = {}
    for a, b in zip(lines, lines[1:]):
        if a.replace(",", "").isdigit():
            out[b] = f"{int(a.replace(',', '')):,}"
    return out


def flow_shots(flow: str) -> list[Path]:
    d = OUT / flow
    return sorted(d.glob("*.png")) if d.exists() else []


# --------------------------------------------------------------- prose blocks

INVENTORY = """
## Screen inventory, against the product doc

The rows below follow the *CMS Configurator: Onboarding UI Screens & Windows Inventory* doc —
every trigger it lists, and what this capture could reach. A screen is marked **write** when the
button that opens it POSTs to DIGIT: this capture runs against a live shared deployment and never
writes, so those screens are named here rather than faked.

{TALLY}

### Entry: Login

| Trigger | Opens | In this capture |
| --- | --- | --- |
| Open the configurator URL | Sign-In screen | [captured](#configurator--sign-in) |
| Sign In (Onboarding mode) | Phase 1 landing | [captured](#onboarding--phase-1--tenant--branding) |
| Help (`?`) icon | — | native `title` tooltip on the Tenant Code label, not a screen |

### Phase 1 — Tenant & Branding

| Trigger | Opens | In this capture |
| --- | --- | --- |
| "Use existing tenant →" | Select Existing Tenant | [captured](#onboarding--phase-1--tenant--branding) |
| "Use this →" on a row | Skips to Phase 2 landing | [captured](#onboarding--phase-2--boundary-setup) |
| "Start Setup →" | Upload Tenant Master Excel | [captured](#onboarding--phase-1--tenant--branding) |
| Successful file upload | Preview (Tenant Info / Branding Details) | [captured](#onboarding--phase-1--tenant--branding) |
| "← Change File" | Back to Upload | [captured](#onboarding--phase-1--tenant--branding) |
| "Upload to DIGIT" | Branding (Step 1.2) | **write** — creates the tenant |
| "Preview" on a branding row | Image Preview modal | behind the write above |
| "Continue" on Branding | Phase 1 Complete summary | behind the write above |
| "Continue to Phase 2" | Phase 2 landing | reached by URL instead |

### Phase 2 — Boundary Setup

| Trigger | Opens | In this capture |
| --- | --- | --- |
| "Proceed to Phase 3" | Skips to Phase 3 landing | [captured](#onboarding--phase-2--boundary-setup) — the banner is on the landing shot, because `ke` already has a hierarchy |
| "Search OSM" | OSM Search | [captured](#onboarding--phase-2--boundary-setup) |
| Running a search | Select Map Levels | [captured](#onboarding--phase-2--boundary-setup) |
| Confirming levels (areas skipped) | Review Skipped Areas | **write** — the same button creates immediately when nothing was skipped, so it was never clicked |
| Confirming the OSM import | Creating → Boundaries Created | **write** |
| "Upload Excel" | Excel Landing (new vs existing hierarchy) | [captured](#onboarding--phase-2--boundary-setup) |
| "Create New Hierarchy" | Define Hierarchy | [captured](#onboarding--phase-2--boundary-setup) (filled, not submitted) |
| "Use Existing Hierarchy" | Select Hierarchy | [captured](#onboarding--phase-2--boundary-setup) |
| Confirming a hierarchy | Download Template | [captured](#onboarding--phase-2--boundary-setup) |
| Naming every OSM level | selection becomes valid | [captured](#onboarding--phase-2--boundary-setup) |
| Uploading the filled file | Verify Boundary Data (+ GeoJSON slot) | [captured](#onboarding--phase-2--boundary-setup) |
| "Upload N Boundaries" | Boundaries Created | **write** |
| "Continue to Phase 3" | Phase 3 landing | reached by URL instead |

### Phase 3 — Common Masters

| Trigger | Opens | In this capture |
| --- | --- | --- |
| "Start Setup" | Upload Common Master Excel | [captured](#onboarding--phase-3--common-masters) |
| Successful upload | Preview (departments / designations) | [captured](#onboarding--phase-3--common-masters) |
| "Create & Continue" | Creating → Define Complaint Hierarchy | **write** |
| Confirming hierarchy levels | Download Complaint Hierarchy Template | behind the write above |
| Uploading the complaint-type file | Verify Complaint Hierarchy | behind the write above |
| "Create N Sub-types" | Phase 3 Complete | **write** |

### Phase 4 — Employee Onboarding

| Trigger | Opens | In this capture |
| --- | --- | --- |
| "Start Phase 4" | Generate Employee Template | **blocked on this deployment** — see [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies) |
| "Download Template" | file download, no new screen | not reachable, same cause |
| Uploading the filled file | Preview (per-row validation) | [captured](#onboarding--phase-4--employee-onboarding) |
| "Create N Employees" | Confirmation dialog | disabled — 0 valid rows, same cause |
| "Create" in the dialog | Creating Employees | **write** |
| Creation finishes | Complete Setup (+ credentials CSV) | **write** |
| "Re-upload Fixed File" | file picker, back through Preview | [captured](#onboarding--phase-4--employee-onboarding) — the button sits on the preview screen |
| "Complete Setup" | Onboarding Complete | reached by URL instead |

### Final: Onboarding Complete

| Trigger | Opens | In this capture |
| --- | --- | --- |
| End of Phase 4 | Complete page | [captured](#onboarding--complete) |
| "Start New Setup" | Phase 1 landing (does not reset prior state) | client-side only — `handleStartNew` is a bare `navigate('/phase/1')`, and the source says so: *"In real app, would reset state"* |
| "View Setup History" | nothing | confirmed: the button has no `onClick` handler |
"""

FINDINGS = """
## What the capture found on bomet

### 1. The seven broken management screens are fixed

Departments, Designations, Complaint Types, Complaint Hierarchies, Map Configuration, Notification
Routing and Provider Templates used to render **"Error loading data — No static resource
v2/_count."** They all load now:

```
POST /egov-mdms-service/v2/_count   → 200 {"totalCount": 692}
POST /egov-mdms-service/v2/_search  → 200, returns records
```

The configurator's datagrid calls `_count` to size its pagination, and the egov-mdms image on bomet
did not serve that endpoint. It does now, so those seven screens sit in their normal sections in
this walkthrough instead of in a "known gaps" section, and the management dashboard shows real
numbers on every tile rather than `…`.

### 2. Phase 4 is blocked by test-leftover boundary hierarchies

Phase 4 refuses to start: **"No boundaries found for tenant `ke`. Complete Phase 2 (boundaries)
first, then retry."** Boundaries *do* exist — the console lists them under the `ADMIN` hierarchy,
`BOMET → SubCounty → Ward`. The wizard just never looks at them.

`Phase4Page.tsx` picks the hierarchy to search by taking the first one the API returns:

```ts
const hierarchies = await boundaryService.getHierarchies(targetTenant).catch(() => []);
const hierarchyType = hierarchies[0]?.hierarchyType;
```

and `boundary.ts` fetches that list **unsorted, `limit: 100`, `offset: 0`**. Paging through every
definition at `ke` shows why that never works here:

```
273 boundary hierarchy definitions at tenant ke
  2 are real:      POC_MZPT_ADMIN, ADMIN
271 are PW_*       Playwright test leftovers
ADMIN is the LAST one returned (index 272 of 273)
the wizard only ever asks for the first 100 → it never sees ADMIN
```

So `hierarchies[0]` is a throwaway hierarchy from an automated test run, the boundary search under
it returns nothing, and Phase 4 blocks. The same list is what Phase 2's **Select Existing
Hierarchy** screen renders, which is why that screen shows a hundred `PW_*` entries and offers no
way to reach `ADMIN`, and why the completion page reports `0 boundaries`.

Note the tenant cleanup already done on this deployment did *not* clear these: tenants dropped from
138 to 45, while the boundary hierarchies stayed at 273. `boundary-service` does expose
`boundary-hierarchy-definition/_delete` — `utilities/crs_dataloader/unified_loader.py` calls it — so
they can be removed the same way.

Two separate things to fix: the deployment is still carrying boundary-hierarchy test junk, and the
wizard should not be picking a hierarchy by array position out of an unsorted, truncated list.

Phase 4's landing screen also states *Prerequisites Met — Phase 2: Boundaries configured* directly
above the error saying there are none; the checklist is static text, not a live check.

### 3. The deployment now has real complaints

`ke` holds **{Complaints} complaints**, where an earlier capture found none across every tenant. The
employee inbox, the complaint registry, the workflow process list and the complaint detail +
workflow-history screens all have data to show.

The console's other counts at capture time: {Tenants} tenants, {Departments} departments,
{Designations} designations, {Complaint Types} complaint types, {Employees} employees,
{Boundaries} boundaries, {Localization Messages} localization messages.

### 4. Only PGR is enabled in the employee UI

`/dss/*`, `/hrms/*` and `/workbench/*` all fall back to the employee home screen. The employee app on
bomet is PGR-only.

### Incidental: what the cleanup did and did not reach

The tenant registry has been cleaned — {Tenants} tenants, down from the 138 an earlier capture found, so
the `Target Tenant NNNNNN` leftovers are gone from the tenant list and from Phase 1's
*Use Existing Tenant* picker. The boundary hierarchies were not: 273 definitions, 271 of them
`PW_*` (see finding 2).

One side effect worth knowing: the employee city picker now labels tenant `ke` as **Ke** rather than
*Bomet County*. The MDMS record still carries `"name": "Bomet County"`, so digit-ui is falling back
to a prettified code because the label's localization message no longer resolves. `ADMIN` still
exists only at `ke`, so it remains the only selection that authenticates.
"""

READONLY = """
## How the capture stayed read-only

The capture runs against a live shared deployment as `ADMIN`, whose roles include `SUPERUSER` and
`MDMS_ADMIN`. A stray "Save" click would have written real configuration to tenant `ke`. Three
independent layers prevented that:

1. **A request guard.** `install_readonly_guard()` aborts every request whose path carries a DIGIT
   write verb — `_create`, `_update`, `_delete`, `_upsert`, `_transition`, and so on — plus every
   `PUT`, `PATCH` and `DELETE`. It cannot simply block `POST`: DIGIT *reads* are
   `POST /…/_search`. Blocked attempts are logged to `output/_guard.log`.
2. **A hard stop before every write control.** The onboarding wizard is walked with real clicks, but
   the capture stops at **Upload to DIGIT**, **Create Hierarchy**, **Upload N Boundaries**,
   **Create & Continue**, **Create Hierarchy & Boundaries** and the Create-Employees confirmation.
   The scraper library's `click_forward()` helper — built to press Continue / Submit / Create — is
   never called.
3. **Uploads that never leave the browser.** The wizard parses each workbook client-side, so the
   preview and verification screens are reached by handing a sample file to the file input and
   letting the SPA read it. Nothing is sent to the deployment; the sample workbooks are in
   [`walkthrough/fixtures/`](../walkthrough/fixtures).

Create forms are shot blank, smart-filled, then abandoned. Every run ended with
`read-only guard: no mutating requests were attempted`.
"""

VIEWING = """
## How to view the interactive version

The rendered site is static — no build step, no server-side code.

```bash
cd walkthrough/output
python3 -m http.server 8080
# then open http://localhost:8080/
```

`index.html` is the sitemap graph, `gallery.html` the grid; each links to the other. Opening
`index.html` straight off disk works too — the screenshot paths are relative and the screen index is
inlined — the graph page just needs internet for the vis-network library it draws with.

To publish it the way the reference prototypes are published, copy the directory under any web root:

```bash
rsync -a --delete walkthrough/output/ user@host:/var/www/proto.theflywheel.in/digit-bomet/
```

If it is served from a subdirectory rather than a subdomain, re-render with root-absolute asset paths
first — `build_sitemap(..., asset_prefix="/digit-bomet/")` and the same on `build_flow_gallery` —
otherwise the thumbnails 404 once the URL gains a path segment.
"""

RERUN = """
## Re-running the capture

Everything needed lives in [`walkthrough/`](../walkthrough), built on
[ChakshuGautam/playwright-scraper](https://github.com/ChakshuGautam/playwright-scraper).

```bash
cd walkthrough
./setup.sh      # once — venv, playwright-scraper, headless chromium
./run_all.sh    # ~20 min: re-captures both apps and re-renders the site
```

Individual pieces:

```bash
.venv/bin/python capture_configurator.py 11_system      # one management flow
.venv/bin/python capture_onboarding.py 03_phase2_boundary   # one wizard phase
.venv/bin/python capture_employee.py                    # all employee flows
.venv/bin/python build_site.py                          # re-render the HTML only
.venv/bin/python build_doc.py                           # re-render this markdown
```

Host, tenant and credentials default to bomet and are overridable:

```bash
WT_HOST=https://other.digit.org WT_TENANT=xx WT_USER=… WT_PASS=… ./run_all.sh
```

[`walkthrough/README.md`](../walkthrough/README.md) documents the scripts, the route tables they
drive, and the reconnaissance helpers to re-run when the deployment changes.
"""


def inventory_with_tally() -> str:
    """Fill in the coverage tally by counting the inventory's own rows, so the
    sentence can never drift from the table under it."""
    rows = [ln for ln in INVENTORY.splitlines()
            if ln.startswith("| ") and "| ---" not in ln and not ln.startswith("| Trigger")]
    captured = sum(1 for r in rows if "[captured](" in r)
    write = sum(1 for r in rows if "**write**" in r or "behind the write" in r)
    blocked = sum(1 for r in rows if "blocked" in r or "disabled" in r or "not reachable" in r)
    other = len(rows) - captured - write - blocked
    tally = (f"All **{len(rows)}** triggers the doc lists are accounted for below: "
             f"**{captured}** captured, **{write}** behind a write this capture will not perform, "
             f"**{blocked}** blocked by [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-"
             f"hierarchies), and **{other}** that open no new screen of their own — client-side "
             f"navigation into a phase this capture reaches by URL, a tooltip, a file download, or "
             f"a dead button.")
    print(f"inventory: {len(rows)} rows — {captured} captured / {write} write / "
          f"{blocked} blocked / {other} other")
    return INVENTORY.strip().replace("{TALLY}", tally)


def main() -> int:
    missing = [f for f, _, _ in SECTIONS if not flow_shots(f)]
    if missing:
        print(f"!! no screenshots for: {', '.join(missing)}")

    total = sum(len(flow_shots(f)) for f, _, _ in SECTIONS)
    parts: list[str] = []
    parts.append(f"""# DIGIT Configurator & Employee UI — visual walkthrough

A screen-by-screen capture of **[bometfeedbackhub.digit.org](https://bometfeedbackhub.digit.org)** —
the DIGIT configurator (4-phase onboarding wizard + management console) and the digit-ui employee app.

**{total} screens · {len(SECTIONS)} flows · captured {CAPTURED} · read-only.** Nothing on the deployment was
created, updated or deleted; see [How the capture stayed read-only](#how-the-capture-stayed-read-only).

> **There is an interactive version.** This page is the flat, shareable rendering. The capture also
> produces an interactive sitemap graph — one thumbnail node per screen, edges following the real
> navigation, click-to-zoom — and a grouped grid gallery. Both are in
> [`walkthrough/output/`](../walkthrough/output): open `index.html` for the graph, `gallery.html` for
> the grid. See [How to view the interactive version](#how-to-view-the-interactive-version).

---

## Contents
""")
    toc = [f"- [{h}](#{slug(h)})" for _, h, _ in SECTIONS]
    toc += [f"- [{h}](#{slug(h)})" for h in
            ("Screen inventory, against the product doc", "What the capture found on bomet",
             "How the capture stayed read-only", "How to view the interactive version",
             "Re-running the capture")]
    parts.append("\n".join(toc) + "\n\n---\n")

    for flow, heading, intro in SECTIONS:
        shots = flow_shots(flow)
        if not shots:
            continue
        parts.append(f"## {heading}\n\n{intro}\n")
        for png in shots:
            label = label_of(png)
            cap = SHOTS.get(label)
            if cap is None:
                print(f"  [no caption] {flow}/{png.name}")
                cap = label.replace("_", " ")
            alt = re.sub(r"[*`\[\]]", "", cap)
            # the caption line is bold, so a **strong** span inside it would
            # close the wrapper early — demote nested bold to italic
            parts.append(f"**{cap.replace('**', '*')}**\n\n![{alt}]({REL}/{flow}/{png.name})\n")
        parts.append("---\n")

    counts = console_counts()
    findings = FINDINGS.strip()
    for k, v in counts.items():
        findings = findings.replace("{" + k + "}", v)
    if "{" in findings and "}" in findings:
        import re as _re
        left = set(_re.findall(r"\{([A-Za-z ]+)\}", findings))
        if left:
            print(f"  [counts missing] {sorted(left)} — console tiles seen: {sorted(counts)}")
    parts += [inventory_with_tally() + "\n", "---\n", findings + "\n", "---\n",
              READONLY.strip() + "\n", "---\n", VIEWING.strip() + "\n", "---\n",
              RERUN.strip() + "\n"]

    DOC.write_text("\n".join(parts))
    print(f"{DOC}: {total} images, {len(SECTIONS)} flows")

    # validate: every image resolves, every TOC anchor has a heading
    text = DOC.read_text()
    broken = [m for m in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
              if not (DOC.parent / m).resolve().exists()]
    heads = {slug(h[3:].strip()) for h in text.splitlines() if h.startswith("## ")}
    heads |= {slug(h[4:].strip()) for h in text.splitlines() if h.startswith("### ")}
    anchors = [a for a in re.findall(r"\]\(#([^)]+)\)", text) if a not in heads]
    print(f"broken images: {len(broken)}{' ' + str(broken[:3]) if broken else ''}")
    print(f"broken anchors: {len(anchors)}{' ' + str(anchors) if anchors else ''}")
    return 1 if (broken or anchors) else 0


if __name__ == "__main__":
    sys.exit(main())
