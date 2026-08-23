# DIGIT Configurator + Employee UI — walkthrough capture

A read-only screenshot walkthrough of **https://bometfeedbackhub.digit.org**, rendered as a
browsable webpage: an interactive sitemap graph of every screen plus a grouped grid gallery,
in the same shape as https://govt-onboard-flow.proto.theflywheel.in.

Built with [ChakshuGautam/playwright-scraper](https://github.com/ChakshuGautam/playwright-scraper).

---

## Open it as a webpage

The rendered site lives in `output/`. It is fully static — no build step, no server-side code.

### 1. Locally, over http (recommended)

```bash
cd walkthrough/output
python3 -m http.server 8080
```

Then open <http://localhost:8080/> — that is the sitemap graph. `gallery.html` is the grid view,
and each page links to the other.

### 2. Locally, straight off disk

```bash
xdg-open walkthrough/output/index.html      # macOS: open
```

Every screenshot path is relative and the screen index is inlined into the HTML, so `file://`
works. The only external asset is the vis-network library the graph is drawn with, pulled from
unpkg — so the graph page needs internet the first time. `gallery.html` needs nothing.

### 3. Hosted, like the govt-onboard-flow link

`output/` is a plain directory of HTML + PNG. Copy it under any web root and point a
vhost at it:

```bash
rsync -a --delete walkthrough/output/ user@host:/var/www/proto.theflywheel.in/digit-bomet/
```

With nginx serving `proto.theflywheel.in`, that publishes it at
`https://digit-bomet.proto.theflywheel.in/` (or `/digit-bomet/`, depending on how the vhost is
mapped). Nothing else is required — no PHP, no node, no rewrite rules.

If it is served from a **subdirectory** rather than a subdomain, re-render the two HTML pages
with root-absolute asset paths first, otherwise the thumbnails 404 when the URL gains a path
segment:

```python
# in build_site.py, pass asset_prefix to both builders
build_sitemap(..., asset_prefix="/digit-bomet/")
build_flow_gallery(..., asset_prefix="/digit-bomet/")
```

---

## What's in it

| Flow | Screens |
|---|---|
| Configurator · Sign In | login form, both mode toggles |
| Onboarding · Phase 1 — Tenant & Branding | landing, use-existing-tenant picker, upload, preview (both tabs), change-file |
| Onboarding · Phase 2 — Boundary Setup | source choice, both Excel paths, define/select hierarchy, template, verify (All/Valid/Errors + GeoJSON), OSM search → map levels |
| Onboarding · Phase 3 — Common Masters | landing, upload, parsed departments + designations |
| Onboarding · Phase 4 — Employee Onboarding | landing (blocked on this deployment), per-row employee validation |
| Onboarding · Complete | the completion summary |
| Configurator · Management console | dashboard home, Advanced (all MDMS masters) |
| Configurator · Tenant, boundaries & map | tenants, boundary hierarchies + detail, boundaries + detail, map configuration, boundary create form |
| Configurator · Complaints & localization | complaint registry, complaint types, complaint hierarchies + detail, localization messages |
| Configurator · People & org structure | departments + detail, designations + detail, employees + detail, org chart, users + detail, bulk imports, create forms |
| Configurator · System | access roles, workflow services + detail, processes, MDMS schemas + detail |
| Configurator · Notifications | configure, routing, templates, provider templates, logs, providers, preferences |
| Configurator · Public dashboard | anonymous-access configuration |
| Employee UI · Sign In | city picker, credentials, consent |
| Employee UI · Inbox | PGR inbox v2 (search + filters), legacy inbox |
| Employee UI · Complaint detail | one complaint opened from the inbox + its workflow timeline |
| Employee UI · New complaint | intake form blank → filled, with the category and county pickers open |
| Employee UI · Search complaint | search result state |

The onboarding wizard is walked with **real clicks**, stopping at every control that would POST to
DIGIT. The screens behind those controls are named — not faked — in the
[screen inventory](../docs/digit-ui-walkthrough.md#screen-inventory-against-the-product-doc), which
follows the product team's *CMS Configurator: Onboarding UI Screens & Windows Inventory* doc.

---

## The capture is read-only

This runs against a live shared deployment as `ADMIN`, whose roles include `SUPERUSER` and
`MDMS_ADMIN`. A stray "Save" click would write real config to tenant `ke`. Three things prevent
that:

1. **A request guard.** `lib.install_readonly_guard()` aborts every request whose path carries a
   DIGIT write verb (`_create`, `_update`, `_delete`, `_upsert`, `_transition`, …) and every
   `PUT`/`PATCH`/`DELETE`. It cannot simply block `POST` — DIGIT reads are `POST /…/_search`.
   Blocked attempts are printed and written to `output/_guard.log`.
2. **A hard stop before every write control.** The wizard is walked by clicking, but never through
   *Upload to DIGIT*, *Create Hierarchy*, *Upload N Boundaries*, *Create & Continue*,
   *Create Hierarchy & Boundaries* or the Create-Employees confirmation. The library's
   `click_forward()` — built to press Continue/Submit/Create/Publish — is never called.
3. **Uploads that never leave the browser.** The wizard parses each workbook client-side, so the
   preview/verify screens are reached by handing a sample file from `fixtures/` to the file input.
   Create forms are shot blank, then smart-filled, then abandoned.

Every run so far has ended with `read-only guard: no mutating requests were attempted`.

---

## Re-running it

```bash
./setup.sh      # once — venv, playwright-scraper, headless chromium
./run_all.sh    # ~20 min: wipes output/en, re-captures both apps, re-renders the site
```

Individual pieces:

```bash
.venv/bin/python capture_configurator.py 11_system     # one management flow
.venv/bin/python capture_onboarding.py 03_phase2_boundary   # one wizard phase
.venv/bin/python capture_employee.py                   # all employee flows
.venv/bin/python build_site.py                         # re-render HTML only
.venv/bin/python build_doc.py                          # re-render the markdown
```

Credentials and target default to `ADMIN` / `eGov@123` / tenant `ke` on bomet and are overridable:

```bash
WT_HOST=https://other.digit.org WT_TENANT=xx WT_USER=… WT_PASS=… ./run_all.sh
```

### Files

| File | What it does |
|---|---|
| `lib.py` | read-only guard, both login helpers, retrying `goto` |
| `capture_configurator.py` | sign-in + the management console; route table mirrors `configurator/src/admin/DigitLayout.tsx` |
| `capture_onboarding.py` | the 4-phase wizard, walked screen by screen up to each write |
| `capture_employee.py` | the five employee-UI flows |
| `fixtures/` | sample onboarding workbooks, parsed in-browser to reach the preview/verify screens |
| `build_site.py` | screen graph + captions → `index.html`, `gallery.html`, `_graph_all.png` |
| `build_doc.py` | the same capture → `docs/digit-ui-walkthrough.md` |
| `recon.py`, `probe_routes.py`, `probe_employee.py` | reconnaissance; re-run when bomet changes |
| `output/_recon/` | route-state JSON the flow lists were derived from |
| `output/_thumbs/` | top-cropped node images for the graph — vis-network scales an image node by width, so a full-page screenshot of a long wizard screen would otherwise stretch into a sliver |

`output/en/` (the 89 captured screens), `output/_thumbs/` and the rendered `index.html` /
`gallery.html` are committed, so
the gallery works straight from a clone with no re-run. Only `output/_recon/` and the `_graph_all.png`
composite are gitignored — both are regenerated by `./run_all.sh`.

A flat, GitHub-readable rendering of the same capture lives at
[`docs/digit-ui-walkthrough.md`](../docs/digit-ui-walkthrough.md).

---

## What the capture found on bomet

Recorded here because it shapes what the gallery shows. The long version, with evidence, is in
[`docs/digit-ui-walkthrough.md`](../docs/digit-ui-walkthrough.md#what-the-capture-found-on-bomet).

**1. The seven broken management screens are fixed.** Departments, Designations, Complaint Types,
Complaint Hierarchies, Map Configuration, Notification Routing and Provider Templates used to render
*"Error loading data — No static resource v2/\_count."* The deployment now serves
`POST /egov-mdms-service/v2/_count` (200, `totalCount`), so all seven load and the management
dashboard shows real numbers instead of `…`. They live in their normal sections now; the
`10_known_gaps` flow is gone.

**2. Phase 4 is blocked by test-leftover boundary hierarchies.** It reports *"No boundaries found for
tenant ke"* even though 88 boundaries exist under `ADMIN`. `Phase4Page.tsx` takes
`getHierarchies(tenant)[0]`, and that list comes back unsorted with `limit: 100` — on bomet all 100
entries on the first page are `PW_*` Playwright leftovers and `ADMIN` is not among them. The same
list is what Phase 2's *Select Existing Hierarchy* screen offers, and it is why the completion page
reports `0 boundaries`.

**3. The deployment now has real complaints.** 5,179 at `ke`, where an earlier capture found none
anywhere. The inbox, the registry, workflow processes and the complaint detail + workflow timeline
all have data.

**4. Only PGR is enabled in the employee UI.** `/dss/*`, `/hrms/*` and `/workbench/*` all fall
back to the home screen.

**5. Test data everywhere.** 138 tenants and 270 boundary hierarchies, mostly named `PW_*`,
`ke.tgt*` or `Target Tenant NNNNNN`. Tenant `ke` *is* "Bomet County", and `ADMIN` exists only there,
so it is the only city selection in the employee UI that authenticates.
