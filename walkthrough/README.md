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
| Configurator · Onboarding wizard | phases 1–4 + the completion summary |
| Configurator · Management console | dashboard home, Advanced (all MDMS masters) |
| Configurator · Tenant management | tenants, boundary hierarchies + detail, department create form |
| Configurator · Complaints & localization | complaint registry, localization messages |
| Configurator · People | employees + detail, org chart, users + detail, bulk imports, employee create form |
| Configurator · System | access roles, workflow services + detail, processes, MDMS schemas + detail, boundaries + detail, boundary create form |
| Configurator · Notifications | configure, templates, logs, providers, user preferences |
| Configurator · Dashboards | PGR dashboard, public dashboard config |
| Configurator · Known gaps | the seven screens that error on this deployment (see below) |
| Employee UI · Sign In | city picker, credentials, consent |
| Employee UI · Inbox | PGR inbox v2 (search + filters), legacy inbox |
| Employee UI · New complaint | intake form blank → filled, with the category and county pickers open |
| Employee UI · Search complaint | search result state |

The onboarding wizard is reached by **direct URL** (`/configurator/phase/1` … `/phase/4`), not by
clicking through it — walking it with clicks would run real tenant provisioning against `ke`.

---

## The capture is read-only

This runs against a live shared deployment as `ADMIN`, whose roles include `SUPERUSER` and
`MDMS_ADMIN`. A stray "Save" click would write real config to tenant `ke`. Three things prevent
that:

1. **A request guard.** `lib.install_readonly_guard()` aborts every request whose path carries a
   DIGIT write verb (`_create`, `_update`, `_delete`, `_upsert`, `_transition`, …) and every
   `PUT`/`PATCH`/`DELETE`. It cannot simply block `POST` — DIGIT reads are `POST /…/_search`.
   Blocked attempts are printed and written to `output/_guard.log`.
2. **No forward-clicking.** The capture scripts navigate by URL and never call the library's
   `click_forward()`, which is built to press Continue/Submit/Create/Publish.
3. **Forms are filled but never submitted.** Create forms are shot blank, then smart-filled, then
   abandoned.

Every run so far has ended with `read-only guard: no mutating requests were attempted`.

---

## Re-running it

```bash
./setup.sh      # once — venv, playwright-scraper, headless chromium
./run_all.sh    # ~12 min: wipes output/en, re-captures both apps, re-renders the site
```

Individual pieces:

```bash
.venv/bin/python capture_configurator.py 07_system     # one flow
.venv/bin/python capture_employee.py                   # all employee flows
.venv/bin/python build_site.py                         # re-render HTML only
```

Credentials and target default to `ADMIN` / `eGov@123` / tenant `ke` on bomet and are overridable:

```bash
WT_HOST=https://other.digit.org WT_TENANT=xx WT_USER=… WT_PASS=… ./run_all.sh
```

### Files

| File | What it does |
|---|---|
| `lib.py` | read-only guard, both login helpers, retrying `goto` |
| `capture_configurator.py` | the ten configurator flows; route table mirrors `configurator/src/admin/DigitLayout.tsx` |
| `capture_employee.py` | the four employee-UI flows |
| `build_site.py` | screen graph + captions → `index.html`, `gallery.html`, `_graph_all.png` |
| `recon.py`, `probe_routes.py`, `probe_employee.py` | reconnaissance; re-run when bomet changes |
| `output/_recon/` | route-state JSON the flow lists were derived from |

`output/en/` (the 63 captured screens) and the rendered `index.html` / `gallery.html` are committed, so
the gallery works straight from a clone with no re-run. Only `output/_recon/` and the `_graph_all.png`
composite are gitignored — both are regenerated by `./run_all.sh`.

A flat, GitHub-readable rendering of the same capture lives at
[`docs/digit-ui-walkthrough.md`](../docs/digit-ui-walkthrough.md).

---

## What the capture found on bomet

Recorded here because it shapes what the gallery shows.

**1. Seven management screens fail to load.** Departments, Designations, Complaint Types,
Complaint Hierarchies, Map Configuration, Notification Routing and Provider Templates all render
*"Error loading data — No static resource v2/\_count."* The configurator's datagrid calls
`POST /egov-mdms-service/v2/_count` for pagination; the egov-mdms image deployed on bomet does not
serve that endpoint, though `v2/_search` works:

```
POST /egov-mdms-service/v2/_count  → NoResourceFoundException: No static resource v2/_count.
POST /egov-mdms-service/v2/_search → 200, returns records
```

The same gap explains the `…` placeholders instead of counts on the management dashboard's
Tenants / Departments / Designations / Complaint Types tiles. It is a deployment version skew,
not a data problem — the data is there. They are captured in the `10_known_gaps` flow rather than
scattered through the tour.

**2. The deployment holds no complaints.** `pgr-services/v2/request/_search` returns zero rows for
all 126 tenants, and `_count` at `ke` is 0. So the employee inbox, the complaint registry and
workflow processes are all genuinely empty, and there is no complaint detail screen to capture.
The PGR analytics endpoint still reports `complaintsResolved: 85` — aggregates outliving the
records they were computed from. Seeding a complaint would have been a write, so it was not done.

**3. Only PGR is enabled in the employee UI.** `/dss/*`, `/hrms/*` and `/workbench/*` all fall
back to the home screen.

**4. Tenant `ke` *is* "Bomet County".** The employee UI's city picker lists ~126 tenants, all but a
handful named `Target Tenant NNNNNN` — leftovers from automated test runs. `ADMIN` exists only at
`ke`, so "Bomet County" is the only city selection that authenticates.
