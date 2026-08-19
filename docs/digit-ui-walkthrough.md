# DIGIT Configurator & Employee UI — visual walkthrough

A screen-by-screen capture of **[bometfeedbackhub.digit.org](https://bometfeedbackhub.digit.org)** —
the DIGIT configurator (onboarding wizard + management console) and the digit-ui employee app.

**63 screens · 14 flows · captured 2026-08-19 · read-only.** Nothing on the deployment was created,
updated or deleted; see [How the capture stayed read-only](#how-the-capture-stayed-read-only).

> **There is an interactive version.** This page is the flat, shareable rendering. The capture also
> produces an interactive sitemap graph — one thumbnail node per screen, edges following the real
> navigation, click-to-zoom — and a grouped grid gallery. Both are in
> [`walkthrough/output/`](../walkthrough/output): open `index.html` for the graph, `gallery.html` for
> the grid. See [How to view the interactive version](#how-to-view-the-interactive-version).

---

## Contents

- [Configurator · Sign In](#configurator--sign-in)
- [Configurator · Onboarding wizard](#configurator--onboarding-wizard)
- [Configurator · Management console](#configurator--management-console)
- [Configurator · Tenant management](#configurator--tenant-management)
- [Configurator · Complaints & localization](#configurator--complaints--localization)
- [Configurator · People](#configurator--people)
- [Configurator · System](#configurator--system)
- [Configurator · Notifications](#configurator--notifications)
- [Configurator · Dashboards](#configurator--dashboards)
- [Configurator · Known gaps on this deployment](#configurator--known-gaps-on-this-deployment)
- [Employee UI · Sign In](#employee-ui--sign-in)
- [Employee UI · Complaint inbox](#employee-ui--complaint-inbox)
- [Employee UI · New complaint intake](#employee-ui--new-complaint-intake)
- [Employee UI · Search complaint](#employee-ui--search-complaint)
- [What the capture found on bomet](#what-the-capture-found-on-bomet)
- [How the capture stayed read-only](#how-the-capture-stayed-read-only)
- [How to view the interactive version](#how-to-view-the-interactive-version)
- [Re-running the capture](#re-running-the-capture)

---

## Configurator · Sign In

`/configurator/login`. One form, one switch: **Onboarding** drives the 4-phase provisioning wizard, **Management** drives the react-admin console. Both authenticate against the root (state-level) tenant, `ke`.

**The sign-in form as it loads**

![The sign-in form as it loads](../walkthrough/output/en/01_login/01_signin_blank.png)

**Filled, with **Onboarding** mode selected**

![Filled, with **Onboarding** mode selected](../walkthrough/output/en/01_login/02_signin_filled_onboarding_mode.png)

**Filled, with **Management** mode selected**

![Filled, with **Management** mode selected](../walkthrough/output/en/01_login/03_signin_filled_management_mode.png)

---

## Configurator · Onboarding wizard

The four provisioning phases plus the completion summary. Captured by navigating directly to `/configurator/phase/1` … `/phase/4` — clicking through the wizard would have run real tenant provisioning against `ke`. Note the view-only banners on phases 2–4: this operator's roles can review those steps but not write them.

**Phase 1 — Tenant & Branding Setup. 100 tenants already exist under `ke`, so the wizard offers to skip ahead**

![Phase 1 — Tenant & Branding Setup. 100 tenants already exist under `ke`, so the wizard offers to skip ahead](../walkthrough/output/en/02_onboarding/01_phase1_tenant_info.png)

**Phase 2 — Boundary Setup (view-only for this operator)**

![Phase 2 — Boundary Setup (view-only for this operator)](../walkthrough/output/en/02_onboarding/02_phase2_boundaries.png)

**Phase 3 — Common Masters: departments, designations, complaint types**

![Phase 3 — Common Masters: departments, designations, complaint types](../walkthrough/output/en/02_onboarding/03_phase3_masters.png)

**Phase 4 — Employee Onboarding, bulk accounts with roles and jurisdictions**

![Phase 4 — Employee Onboarding, bulk accounts with roles and jurisdictions](../walkthrough/output/en/02_onboarding/04_phase4_employees.png)

**Completion summary: 33 departments, 46 designations, 685 complaint types at `ke`**

![Completion summary: 33 departments, 46 designations, 685 complaint types at `ke`](../walkthrough/output/en/02_onboarding/05_complete.png)

---

## Configurator · Management console

The console landing page and the Advanced view that exposes every generic MDMS master the data provider knows about.

**Management console home, with per-registry record counts**

![Management console home, with per-registry record counts](../walkthrough/output/en/03_home/01_dashboard_home.png)

**Advanced — every generic MDMS master**

![Advanced — every generic MDMS master](../walkthrough/output/en/03_home/02_advanced_all_masters.png)

---

## Configurator · Tenant management

Tenant registry, boundary hierarchy definitions, and the department create form — shot blank and filled, never submitted.

**Tenant registry**

![Tenant registry](../walkthrough/output/en/04_tenant/01_tenants_list.png)

**Boundary hierarchy definitions**

![Boundary hierarchy definitions](../walkthrough/output/en/04_tenant/02_boundary_hierarchies_list.png)

**The ADMIN hierarchy in detail**

![The ADMIN hierarchy in detail](../walkthrough/output/en/04_tenant/03_boundary_hierarchies_detail.png)

**Department create form, blank**

![Department create form, blank](../walkthrough/output/en/04_tenant/04_department_create_blank.png)

**The same form filled — never submitted**

![The same form filled — never submitted](../walkthrough/output/en/04_tenant/05_department_create_filled.png)

---

## Configurator · Complaints & localization

The complaint registry (empty on this deployment — see the findings below) and the 14,258 localization messages.

**Complaint registry — no records exist on this deployment**

![Complaint registry — no records exist on this deployment](../walkthrough/output/en/05_complaints/01_complaints_list_empty.png)

**Localization messages (14,258 of them)**

![Localization messages (14,258 of them)](../walkthrough/output/en/05_complaints/02_localization_messages_list.png)

---

## Configurator · People

HRMS employees, user accounts, the org chart, both bulk-import surfaces, and the employee create form blank and filled.

**HRMS employees**

![HRMS employees](../walkthrough/output/en/06_people/01_employees_list.png)

**An employee record**

![An employee record](../walkthrough/output/en/06_people/02_employees_detail.png)

**Department / designation org chart**

![Department / designation org chart](../walkthrough/output/en/06_people/03_org_chart.png)

**User accounts**

![User accounts](../walkthrough/output/en/06_people/04_users_list.png)

**A user record**

![A user record](../walkthrough/output/en/06_people/05_users_detail.png)

**Employee bulk import (XLSX)**

![Employee bulk import (XLSX)](../walkthrough/output/en/06_people/06_employees_bulk_import.png)

**Localization bulk import**

![Localization bulk import](../walkthrough/output/en/06_people/07_localization_bulk_import.png)

**Employee create form, blank**

![Employee create form, blank](../walkthrough/output/en/06_people/08_employee_create_blank.png)

**The same form filled — never submitted**

![The same form filled — never submitted](../walkthrough/output/en/06_people/09_employee_create_filled.png)

---

## Configurator · System

Access roles, the PGR workflow state machine, workflow process instances, MDMS v2 schemas, and boundary records — each with its detail view where one exists.

**Access roles (49 on this deployment)**

![Access roles (49 on this deployment)](../walkthrough/output/en/07_system/01_access_roles_list.png)

**A role and its actions**

![A role and its actions](../walkthrough/output/en/07_system/02_access_roles_detail.png)

**Workflow business services**

![Workflow business services](../walkthrough/output/en/07_system/03_workflows_list.png)

**The PGR state machine**

![The PGR state machine](../walkthrough/output/en/07_system/04_workflows_detail.png)

**Workflow process instances — empty, since no complaints exist**

![Workflow process instances — empty, since no complaints exist](../walkthrough/output/en/07_system/05_processes_list_empty.png)

**MDMS v2 schema definitions**

![MDMS v2 schema definitions](../walkthrough/output/en/07_system/06_mdms_schemas_list.png)

**A schema in detail**

![A schema in detail](../walkthrough/output/en/07_system/07_mdms_schemas_detail.png)

**Boundary records**

![Boundary records](../walkthrough/output/en/07_system/08_boundaries_list.png)

**The BOMET boundary**

![The BOMET boundary](../walkthrough/output/en/07_system/09_boundaries_detail.png)

**Boundary create form, blank**

![Boundary create form, blank](../walkthrough/output/en/07_system/10_boundary_create_blank.png)

**The same form filled — never submitted**

![The same form filled — never submitted](../walkthrough/output/en/07_system/11_boundary_create_filled.png)

---

## Configurator · Notifications

The Novu-backed notification surfaces: routing configuration, templates, the delivery log, configured providers, and per-user preferences.

**Notification routing configuration**

![Notification routing configuration](../walkthrough/output/en/08_notifications/01_notification_configure.png)

**Notification templates**

![Notification templates](../walkthrough/output/en/08_notifications/02_notification_templates.png)

**Delivery log (Novu bridge)**

![Delivery log (Novu bridge)](../walkthrough/output/en/08_notifications/03_notification_logs.png)

**Configured providers**

![Configured providers](../walkthrough/output/en/08_notifications/04_notification_providers.png)

**Per-user notification preferences**

![Per-user notification preferences](../walkthrough/output/en/08_notifications/05_user_preferences.png)

---

## Configurator · Dashboards

The PGR operational dashboard and the public dashboard configuration screen.

**PGR operational dashboard**

![PGR operational dashboard](../walkthrough/output/en/09_dashboards/01_pgr_dashboard.png)

**Public dashboard configuration**

![Public dashboard configuration](../walkthrough/output/en/09_dashboards/02_public_dashboard_configure.png)

---

## Configurator · Known gaps on this deployment

**These seven screens do not work on bomet today.** They are collected here rather than scattered through the tour above. All seven fail the same way and for the same reason — see [What the capture found](#what-the-capture-found-on-bomet).

**Departments — *Error loading data: No static resource v2/_count***

![Departments — *Error loading data: No static resource v2/_count*](../walkthrough/output/en/10_known_gaps/01_departments_list_error.png)

**Designations — same failure**

![Designations — same failure](../walkthrough/output/en/10_known_gaps/02_designations_list_error.png)

**Complaint Types — same failure**

![Complaint Types — same failure](../walkthrough/output/en/10_known_gaps/03_complaint_types_list_error.png)

**Complaint Hierarchies — same failure**

![Complaint Hierarchies — same failure](../walkthrough/output/en/10_known_gaps/04_complaint_hierarchies_list_error.png)

**Map Configuration — same failure**

![Map Configuration — same failure](../walkthrough/output/en/10_known_gaps/05_map_configuration_error.png)

**Notification Routing — same failure**

![Notification Routing — same failure](../walkthrough/output/en/10_known_gaps/06_notification_routing_error.png)

**Provider Templates (WhatsApp) — same failure**

![Provider Templates (WhatsApp) — same failure](../walkthrough/output/en/10_known_gaps/07_provider_templates_whatsapp_error.png)

---

## Employee UI · Sign In

`/digit-ui/employee`. City picker, credentials, privacy consent. The city list holds ~126 tenants, almost all of them `Target Tenant NNNNNN` leftovers from automated test runs; **Bomet County** is the real one.

**The employee sign-in card, in Bomet County branding**

![The employee sign-in card, in Bomet County branding](../walkthrough/output/en/11_employee_login/01_employee_signin_blank.png)

**City picker, filtered**

![City picker, filtered](../walkthrough/output/en/11_employee_login/02_employee_city_picker.png)

**Filled, with consent given**

![Filled, with consent given](../walkthrough/output/en/11_employee_login/03_employee_signin_filled.png)

**Employee home. Only PGR is enabled here — `/dss/*`, `/hrms/*` and `/workbench/*` all fall back to this screen**

![Employee home. Only PGR is enabled here — `/dss/*`, `/hrms/*` and `/workbench/*` all fall back to this screen](../walkthrough/output/en/11_employee_login/04_employee_home.png)

---

## Employee UI · Complaint inbox

Inbox v2 with its search panel (complaint number, mobile, date range) and filter rail (subtype, county, status), plus the legacy inbox. Both are empty because the deployment holds no complaints.

**Inbox v2 — search panel and filter rail**

![Inbox v2 — search panel and filter rail](../walkthrough/output/en/12_employee_inbox/01_inbox_v2_search_and_filters.png)

**After running a search: no results**

![After running a search: no results](../walkthrough/output/en/12_employee_inbox/02_inbox_v2_search_results_empty.png)

**The legacy inbox**

![The legacy inbox](../walkthrough/output/en/12_employee_inbox/03_inbox_v1_legacy.png)

---

## Employee UI · New complaint intake

The counter-staff intake form: complainant details, complaint type → category → sub-type cascade, a Leaflet map pin for the location, and a description. Filled in for the capture and **not** submitted.

**The intake form as it loads**

![The intake form as it loads](../walkthrough/output/en/13_employee_new_complaint/01_create_complaint_blank.png)

**Complaint category picker open**

![Complaint category picker open](../walkthrough/output/en/13_employee_new_complaint/02_dropdown_category_open.png)

**County picker open**

![County picker open](../walkthrough/output/en/13_employee_new_complaint/03_dropdown_county_open.png)

**Filled in and left there — SUBMIT was never clicked**

![Filled in and left there — SUBMIT was never clicked](../walkthrough/output/en/13_employee_new_complaint/04_create_complaint_filled_not_submitted.png)

---

## Employee UI · Search complaint

The Search Complaint entry point from the home screen.

**Search Complaint — no results**

![Search Complaint — no results](../walkthrough/output/en/14_employee_search/01_search_complaint_no_results.png)

---

## What the capture found on bomet

Three things worth knowing before anyone reads the screens above as a product demo.

### 1. Seven management screens fail to load

Departments, Designations, Complaint Types, Complaint Hierarchies, Map Configuration, Notification
Routing and Provider Templates all render **"Error loading data — No static resource v2/_count."**

The configurator's datagrid calls `POST /egov-mdms-service/v2/_count` to size its pagination. The
egov-mdms image deployed on bomet does not serve that endpoint, although `v2/_search` works fine:

```
POST /egov-mdms-service/v2/_count   → NoResourceFoundException: No static resource v2/_count.
POST /egov-mdms-service/v2/_search  → 200, returns records
```

The same gap is why the management dashboard shows `…` instead of numbers on its Tenants,
Departments, Designations and Complaint Types tiles. **This is deployment version skew, not missing
data** — the records are there and `_search` returns them. Fixing it means moving bomet onto an
egov-mdms build that serves `v2/_count`.

### 2. The deployment holds no complaints

`pgr-services/v2/request/_search` returns zero rows for **all 126 tenants**, and `_count` at `ke` is
`0`. So the employee inbox, the complaint registry and the workflow process list are all genuinely
empty, and there is no complaint-detail or workflow-history screen to show. Seeding one would have
been a write, so it was not done.

Curiously the PGR analytics endpoint still reports `complaintsResolved: 85` — aggregates outliving
the records they were computed from.

### 3. Only PGR is enabled in the employee UI

`/dss/*`, `/hrms/*` and `/workbench/*` all fall back to the employee home screen. The employee app on
bomet is PGR-only.

### Incidental: tenant `ke` *is* "Bomet County"

The employee UI's city picker lists ~126 tenants, all but a handful named `Target Tenant NNNNNN` —
leftovers from automated test runs. `ADMIN` exists only at `ke`, so **Bomet County** is the only city
selection that authenticates.

---

## How the capture stayed read-only

The capture runs against a live shared deployment as `ADMIN`, whose roles include `SUPERUSER` and
`MDMS_ADMIN`. A stray "Save" click would have written real configuration to tenant `ke`. Three
independent layers prevented that:

1. **A request guard.** `install_readonly_guard()` aborts every request whose path carries a DIGIT
   write verb — `_create`, `_update`, `_delete`, `_upsert`, `_transition`, and so on — plus every
   `PUT`, `PATCH` and `DELETE`. It cannot simply block `POST`: DIGIT *reads* are
   `POST /…/_search`. Blocked attempts are logged to `output/_guard.log`.
2. **No forward-clicking.** Screens are reached by direct URL navigation. The scraper library's
   `click_forward()` helper — which is built to press Continue / Submit / Create / Publish / Go Live —
   is never called.
3. **Forms are filled but abandoned.** Every create form is shot blank, smart-filled, then left.

Every run ended with `read-only guard: no mutating requests were attempted`.

---

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

---

## Re-running the capture

Everything needed lives in [`walkthrough/`](../walkthrough), built on
[ChakshuGautam/playwright-scraper](https://github.com/ChakshuGautam/playwright-scraper).

```bash
cd walkthrough
./setup.sh      # once — venv, playwright-scraper, headless chromium
./run_all.sh    # ~12 min: re-captures both apps and re-renders the site
```

Individual pieces:

```bash
.venv/bin/python capture_configurator.py 07_system   # one flow
.venv/bin/python capture_employee.py                 # all employee flows
.venv/bin/python build_site.py                       # re-render the HTML only
```

Host, tenant and credentials default to bomet and are overridable:

```bash
WT_HOST=https://other.digit.org WT_TENANT=xx WT_USER=… WT_PASS=… ./run_all.sh
```

[`walkthrough/README.md`](../walkthrough/README.md) documents the scripts, the route tables they
drive, and the reconnaissance helpers to re-run when the deployment changes.
