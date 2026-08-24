# DIGIT Configurator & Employee UI — visual walkthrough

A screen-by-screen capture of **[bometfeedbackhub.digit.org](https://bometfeedbackhub.digit.org)** —
the DIGIT configurator (4-phase onboarding wizard + management console) and the digit-ui employee app.

**90 screens · 18 flows · captured 2026-08-24 · read-only.** Nothing on the deployment was
created, updated or deleted; see [How the capture stayed read-only](#how-the-capture-stayed-read-only).

> **There is an interactive version.** This page is the flat, shareable rendering. The capture also
> produces an interactive sitemap graph — one thumbnail node per screen, edges following the real
> navigation, click-to-zoom — and a grouped grid gallery. Both are in
> [`walkthrough/output/`](../walkthrough/output): open `index.html` for the graph, `gallery.html` for
> the grid. See [How to view the interactive version](#how-to-view-the-interactive-version).

---

## Contents

- [Configurator · Sign In](#configurator--sign-in)
- [Onboarding · Phase 1 — Tenant & Branding](#onboarding--phase-1--tenant--branding)
- [Onboarding · Phase 2 — Boundary Setup](#onboarding--phase-2--boundary-setup)
- [Onboarding · Phase 3 — Common Masters](#onboarding--phase-3--common-masters)
- [Onboarding · Phase 4 — Employee Onboarding](#onboarding--phase-4--employee-onboarding)
- [Onboarding · Complete](#onboarding--complete)
- [Configurator · Management console](#configurator--management-console)
- [Configurator · Tenant, boundaries & map](#configurator--tenant-boundaries--map)
- [Configurator · Complaints & localization](#configurator--complaints--localization)
- [Configurator · People & org structure](#configurator--people--org-structure)
- [Configurator · System (roles, workflow, MDMS)](#configurator--system-roles-workflow-mdms)
- [Configurator · Notifications](#configurator--notifications)
- [Configurator · Public dashboard](#configurator--public-dashboard)
- [Employee UI · Sign In](#employee-ui--sign-in)
- [Employee UI · Complaint inbox](#employee-ui--complaint-inbox)
- [Employee UI · Complaint detail & workflow](#employee-ui--complaint-detail--workflow)
- [Employee UI · New complaint intake](#employee-ui--new-complaint-intake)
- [Employee UI · Search complaint](#employee-ui--search-complaint)
- [Screen inventory, against the product doc](#screen-inventory-against-the-product-doc)
- [What the capture found on bomet](#what-the-capture-found-on-bomet)
- [How the capture stayed read-only](#how-the-capture-stayed-read-only)
- [How to view the interactive version](#how-to-view-the-interactive-version)
- [Re-running the capture](#re-running-the-capture)

---

## Configurator · Sign In

`/configurator/login`. One form, one switch: **Onboarding** drives the 4-phase provisioning wizard, **Management** drives the react-admin console. Both authenticate against the root (state-level) tenant, `ke`. The `?` next to Tenant Code is a native tooltip, not a screen.

**The sign-in form as it loads**

![The sign-in form as it loads](../walkthrough/output/en/01_login/01_signin_blank.png)

**Filled, Onboarding mode selected**

![Filled, Onboarding mode selected](../walkthrough/output/en/01_login/02_signin_filled_onboarding_mode.png)

**Filled, Management mode selected**

![Filled, Management mode selected](../walkthrough/output/en/01_login/03_signin_filled_management_mode.png)

---

## Onboarding · Phase 1 — Tenant & Branding

Two ways out of the landing screen: reuse a tenant that already exists, or upload a Tenant Master workbook. The workbook is parsed **in the browser**, so the preview screens below cost the deployment nothing — the sample file describes Maputo, which is why the preview shows `mz.maputo` rather than Bomet. Everything past **Upload to DIGIT** (branding, the image preview modal, the Phase 1 summary) writes, and is listed as not captured in the [screen inventory](#screen-inventory-against-the-product-doc).

**Phase 1 landing. Tenants already exist under `ke`, so the skip-ahead banner offers to reuse one**

![Phase 1 landing. Tenants already exist under ke, so the skip-ahead banner offers to reuse one](../walkthrough/output/en/02_phase1_tenant/01_p1_landing.png)

**Use Existing Tenant. Picking a row jumps to Phase 2 without creating anything**

![Use Existing Tenant. Picking a row jumps to Phase 2 without creating anything](../walkthrough/output/en/02_phase1_tenant/02_p1_select_existing_tenant.png)

**Step 1.1 — the Tenant Master dropzone**

![Step 1.1 — the Tenant Master dropzone](../walkthrough/output/en/02_phase1_tenant/03_p1_upload_tenant_master.png)

**Preview, Tenant Info tab: the parsed row and exactly what creating it would do**

![Preview, Tenant Info tab: the parsed row and exactly what creating it would do](../walkthrough/output/en/02_phase1_tenant/04_p1_preview_tenant_info.png)

**Preview, Branding Details tab**

![Preview, Branding Details tab](../walkthrough/output/en/02_phase1_tenant/05_p1_preview_branding_details.png)

***← Change File* returns to the dropzone**

![← Change File returns to the dropzone](../walkthrough/output/en/02_phase1_tenant/06_p1_change_file_back_to_upload.png)

---

## Onboarding · Phase 2 — Boundary Setup

The widest phase, and **both of its paths are captured below**.

The **Upload from Excel** path (shots 2–11) picks or defines a hierarchy, hands you a template shaped to that hierarchy's levels, then validates the filled workbook row by row, with an optional GeoJSON sidecar for real map outlines.

The **Fetch from OpenStreetMap** path (shots 12–16) types an area into the Nominatim typeahead, pulls that relation's administrative levels from Overpass, and asks you to include and name each one. `Cidade de Maputo` is used here because it resolves to a clean three-level hierarchy — one city, six *distritos municipais*, sixty-three *bairros* — all three included and named.

Both paths stop at the same wall: the button that creates the hierarchy and the boundaries.

**Choose the boundary source: OpenStreetMap or Excel**

![Choose the boundary source: OpenStreetMap or Excel](../walkthrough/output/en/03_phase2_boundary/01_p2_landing_choose_source.png)

**Excel path — define a new hierarchy or reuse an existing one**

![Excel path — define a new hierarchy or reuse an existing one](../walkthrough/output/en/03_phase2_boundary/02_p2_excel_choose_path.png)

**Define Hierarchy — name plus an ordered, contiguous level list**

![Define Hierarchy — name plus an ordered, contiguous level list](../walkthrough/output/en/03_phase2_boundary/03_p2_create_hierarchy_blank.png)

**The same form filled in. *Create Hierarchy* writes, so it was not clicked**

![The same form filled in. Create Hierarchy writes, so it was not clicked](../walkthrough/output/en/03_phase2_boundary/04_p2_create_hierarchy_filled.png)

**Select Existing Hierarchy — every entry offered is a `PW_*` test leftover; the real `ADMIN` hierarchy is the 273rd definition at this tenant and the screen only asks for the first 100 (see [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies))**

![Select Existing Hierarchy — every entry offered is a PW_ test leftover; the real ADMIN hierarchy is the 273rd definition at this tenant and the screen only asks for the first 100 (see finding 2(#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies))](../walkthrough/output/en/03_phase2_boundary/05_p2_select_existing_hierarchy.png)

**A hierarchy selected**

![A hierarchy selected](../walkthrough/output/en/03_phase2_boundary/06_p2_hierarchy_selected.png)

**Boundary Data Upload — the template is generated for the chosen hierarchy's levels**

![Boundary Data Upload — the template is generated for the chosen hierarchy's levels](../walkthrough/output/en/03_phase2_boundary/07_p2_download_template.png)

**Verify Boundary Data, All tab — every row of the sample workbook, parsed in the browser**

![Verify Boundary Data, All tab — every row of the sample workbook, parsed in the browser](../walkthrough/output/en/03_phase2_boundary/08_p2_verify_all.png)

**Valid tab**

![Valid tab](../walkthrough/output/en/03_phase2_boundary/09_p2_verify_valid.png)

**Errors tab — empty for this file**

![Errors tab — empty for this file](../walkthrough/output/en/03_phase2_boundary/10_p2_verify_errors.png)

**With the optional GeoJSON sidecar attached — it reports how many boundaries it can give real outlines to**

![With the optional GeoJSON sidecar attached — it reports how many boundaries it can give real outlines to](../walkthrough/output/en/03_phase2_boundary/11_p2_verify_with_geojson.png)

**OSM path — search the area to import**

![OSM path — search the area to import](../walkthrough/output/en/03_phase2_boundary/12_p2_osm_search.png)

**The Nominatim typeahead resolving *Cidade de Maputo/Mozambique*; picking a suggestion scopes the Overpass lookup to that exact relation**

![The Nominatim typeahead resolving Cidade de Maputo/Mozambique; picking a suggestion scopes the Overpass lookup to that exact relation](../walkthrough/output/en/03_phase2_boundary/13_p2_osm_search_typeahead.png)

**Suggestion picked, ready to search**

![Suggestion picked, ready to search](../walkthrough/output/en/03_phase2_boundary/14_p2_osm_search_typed.png)

**Map Admin Levels — the three levels Overpass returned: 1 city (level 4), 6 distritos municipais (level 5), 63 bairros (level 8)**

![Map Admin Levels — the three levels Overpass returned: 1 city (level 4), 6 distritos municipais (level 5), 63 bairros (level 8)](../walkthrough/output/en/03_phase2_boundary/15_p2_osm_map_levels.png)

**Each level named — *Município → Distrito Municipal → Bairro*. The selection is now valid and *Create Hierarchy & Boundaries* is enabled; that click writes, so this is where the capture stops**

![Each level named — Município → Distrito Municipal → Bairro. The selection is now valid and Create Hierarchy & Boundaries is enabled; that click writes, so this is where the capture stops](../walkthrough/output/en/03_phase2_boundary/16_p2_osm_levels_named.png)

---

## Onboarding · Phase 3 — Common Masters

Departments, designations and complaint types from one workbook. Upload and preview are client-side; **Create & Continue** writes, so the complaint-hierarchy step behind it is not captured.

**Phase 3 landing**

![Phase 3 landing](../walkthrough/output/en/04_phase3_masters/01_p3_landing.png)

**Common Master dropzone**

![Common Master dropzone](../walkthrough/output/en/04_phase3_masters/02_p3_upload_common_master.png)

**Parsed departments and designations with per-row validation**

![Parsed departments and designations with per-row validation](../walkthrough/output/en/04_phase3_masters/03_p3_preview_departments_designations.png)

---

## Onboarding · Phase 4 — Employee Onboarding

Phase 4 is **blocked on this deployment** — its reference load reports *No boundaries found for tenant "ke"*, which disables **Start Phase 4** and hides the template generator behind it. Why that happens is [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies). The file input is rendered outside the step, so the employee workbook can still be parsed and its per-row validation captured.

**Phase 4 landing. Note the contradiction: *Prerequisites Met — Phase 2: Boundaries configured*, directly under *No boundaries found for tenant "ke"***

![Phase 4 landing. Note the contradiction: Prerequisites Met — Phase 2: Boundaries configured, directly under No boundaries found for tenant "ke"](../walkthrough/output/en/05_phase4_employees/01_p4_landing.png)

**Per-row employee validation. Every row fails on the missing boundary, so *Create Employees* stays disabled and the confirmation dialog behind it is unreachable**

![Per-row employee validation. Every row fails on the missing boundary, so Create Employees stays disabled and the confirmation dialog behind it is unreachable](../walkthrough/output/en/05_phase4_employees/02_p4_preview_validation.png)

---

## Onboarding · Complete

The end-of-wizard summary: live tenant totals, links into the employee and citizen apps, and three buttons. **View Setup History** has no `onClick` handler in `configurator/src/pages/CompletePage.tsx` — it renders and does nothing.

**The completion summary**

![The completion summary](../walkthrough/output/en/06_onboarding_complete/01_complete_summary.png)

---

## Configurator · Management console

The react-admin console. Home counts every registry; **Advanced** exposes every generic MDMS master the data provider knows about.

**Management console home**

![Management console home](../walkthrough/output/en/07_home/01_dashboard_home.png)

**Advanced — every generic MDMS master**

![Advanced — every generic MDMS master](../walkthrough/output/en/07_home/02_advanced_all_masters.png)

---

## Configurator · Tenant, boundaries & map

Tenant registry, boundary hierarchy definitions, boundary records and the per-tenant map configuration, plus the boundary create form (filled, never submitted).

**Tenant registry**

![Tenant registry](../walkthrough/output/en/08_tenant/01_tenants_list.png)

**Boundary hierarchy definitions**

![Boundary hierarchy definitions](../walkthrough/output/en/08_tenant/02_boundary_hierarchies_list.png)

**One hierarchy in detail**

![One hierarchy in detail](../walkthrough/output/en/08_tenant/03_boundary_hierarchies_detail.png)

**Boundary records**

![Boundary records](../walkthrough/output/en/08_tenant/04_boundaries_list.png)

**One boundary in detail**

![One boundary in detail](../walkthrough/output/en/08_tenant/05_boundaries_detail.png)

**Map Configuration — centre, zoom and tiles per tenant**

![Map Configuration — centre, zoom and tiles per tenant](../walkthrough/output/en/08_tenant/06_map_configuration.png)

**Boundary create form, blank**

![Boundary create form, blank](../walkthrough/output/en/08_tenant/07_boundary_create_blank.png)

**The same form filled in — never submitted**

![The same form filled in — never submitted](../walkthrough/output/en/08_tenant/08_boundary_create_filled.png)

---

## Configurator · Complaints & localization

The complaint registry and the masters behind it — complaint types, the category/sub-type hierarchy, and the localization messages that label them in the citizen and employee apps.

**Complaint registry**

![Complaint registry](../walkthrough/output/en/09_complaints/01_complaints_list.png)

**Complaint Types**

![Complaint Types](../walkthrough/output/en/09_complaints/02_complaint_types_list.png)

**Complaint Hierarchies**

![Complaint Hierarchies](../walkthrough/output/en/09_complaints/03_complaint_hierarchies_list.png)

**The PGR hierarchy in detail**

![The PGR hierarchy in detail](../walkthrough/output/en/09_complaints/04_complaint_hierarchies_detail.png)

**Localization messages**

![Localization messages](../walkthrough/output/en/09_complaints/05_localization_messages_list.png)

---

## Configurator · People & org structure

Departments, designations, employees, users and the org chart, plus the two bulk-import surfaces and the department/employee create forms.

**Departments**

![Departments](../walkthrough/output/en/10_people/01_departments_list.png)

**One department in detail**

![One department in detail](../walkthrough/output/en/10_people/02_departments_detail.png)

**Designations**

![Designations](../walkthrough/output/en/10_people/03_designations_list.png)

**One designation in detail**

![One designation in detail](../walkthrough/output/en/10_people/04_designations_detail.png)

**Employees**

![Employees](../walkthrough/output/en/10_people/05_employees_list.png)

**One employee in detail**

![One employee in detail](../walkthrough/output/en/10_people/06_employees_detail.png)

**Org chart**

![Org chart](../walkthrough/output/en/10_people/07_org_chart.png)

**Users**

![Users](../walkthrough/output/en/10_people/08_users_list.png)

**One user in detail**

![One user in detail](../walkthrough/output/en/10_people/09_users_detail.png)

**Employee bulk import**

![Employee bulk import](../walkthrough/output/en/10_people/10_employees_bulk_import.png)

**Localization bulk import**

![Localization bulk import](../walkthrough/output/en/10_people/11_localization_bulk_import.png)

**Department create form, blank**

![Department create form, blank](../walkthrough/output/en/10_people/12_department_create_blank.png)

**The same form filled in — never submitted**

![The same form filled in — never submitted](../walkthrough/output/en/10_people/13_department_create_filled.png)

**Employee create form, blank**

![Employee create form, blank](../walkthrough/output/en/10_people/14_employee_create_blank.png)

**The same form filled in — never submitted**

![The same form filled in — never submitted](../walkthrough/output/en/10_people/15_employee_create_filled.png)

---

## Configurator · System (roles, workflow, MDMS)

Access roles, the PGR workflow business service (the state machine every complaint runs through), live workflow process instances, and the MDMS v2 schema registry.

**Access roles**

![Access roles](../walkthrough/output/en/11_system/01_access_roles_list.png)

**One role in detail**

![One role in detail](../walkthrough/output/en/11_system/02_access_roles_detail.png)

**Workflow business services**

![Workflow business services](../walkthrough/output/en/11_system/03_workflows_list.png)

**The PGR state machine in detail**

![The PGR state machine in detail](../walkthrough/output/en/11_system/04_workflows_detail.png)

**Workflow process instances**

![Workflow process instances](../walkthrough/output/en/11_system/05_processes_list.png)

**MDMS v2 schemas**

![MDMS v2 schemas](../walkthrough/output/en/11_system/06_mdms_schemas_list.png)

**One schema in detail**

![One schema in detail](../walkthrough/output/en/11_system/07_mdms_schemas_detail.png)

---

## Configurator · Notifications

Routing configuration, templates, provider templates, the delivery log from the Novu bridge, configured providers, and per-user preferences.

**Notification routing configuration**

![Notification routing configuration](../walkthrough/output/en/12_notifications/01_notification_configure.png)

**Notification Routing rules**

![Notification Routing rules](../walkthrough/output/en/12_notifications/02_notification_routing.png)

**Notification templates**

![Notification templates](../walkthrough/output/en/12_notifications/03_notification_templates.png)

**Provider templates (WhatsApp)**

![Provider templates (WhatsApp)](../walkthrough/output/en/12_notifications/04_provider_templates_whatsapp.png)

**Delivery log from the Novu bridge**

![Delivery log from the Novu bridge](../walkthrough/output/en/12_notifications/05_notification_logs.png)

**Configured providers**

![Configured providers](../walkthrough/output/en/12_notifications/06_notification_providers.png)

**Per-user notification preferences**

![Per-user notification preferences](../walkthrough/output/en/12_notifications/07_user_preferences.png)

---

## Configurator · Public dashboard

Anonymous, credential-free access to the tenant's dashboard, and the stable URL it is shared under. `/manage/pgr-dashboard` exists in `configurator/src/App.tsx` but not in the bundle bomet serves — that route falls back to the console home.

**Public dashboard configuration**

![Public dashboard configuration](../walkthrough/output/en/13_dashboards/01_public_dashboard_configure.png)

---

## Employee UI · Sign In

`/digit-ui/employee`. City picker, credentials, privacy consent. Tenant `ke` is the only selection that authenticates, because `ADMIN` exists only there — and since the cleanup the picker labels it **Ke**, not *Bomet County*. Its MDMS record still reads `Bomet County`, so this is digit-ui falling back to a prettified tenant code when the label's localization message is missing, not lost data.

**The employee sign-in screen**

![The employee sign-in screen](../walkthrough/output/en/14_employee_login/01_employee_signin_blank.png)

**The city picker — six tenants, `ke` among them as *Ke***

![The city picker — six tenants, ke among them as Ke](../walkthrough/output/en/14_employee_login/02_employee_city_picker.png)

**Filled, with privacy consent ticked**

![Filled, with privacy consent ticked](../walkthrough/output/en/14_employee_login/03_employee_signin_filled.png)

**Employee home. Only PGR is enabled here**

![Employee home. Only PGR is enabled here](../walkthrough/output/en/14_employee_login/04_employee_home.png)

---

## Employee UI · Complaint inbox

Inbox v2 with its search panel and filter rail, and the legacy inbox behind it. It opens on **My Complaints**, which is empty for `ADMIN` — the deployment's complaints belong to other employees, and **All Complaints** is the tab that shows them.

**Inbox v2 as it opens — search panel, filter rail, and the *My Complaints* tab, empty for this operator**

![Inbox v2 as it opens — search panel, filter rail, and the My Complaints tab, empty for this operator](../walkthrough/output/en/15_employee_inbox/01_inbox_v2_my_complaints.png)

**The *All Complaints* tab: complaint number, locality, status, current owner and SLA days remaining**

![The All Complaints tab: complaint number, locality, status, current owner and SLA days remaining](../walkthrough/output/en/15_employee_inbox/02_inbox_v2_all_complaints.png)

**The legacy inbox**

![The legacy inbox](../walkthrough/output/en/15_employee_inbox/03_inbox_v1_legacy.png)

---

## Employee UI · Complaint detail & workflow

One complaint opened from the inbox: the detail card, and the workflow history below the fold. Opening a complaint is a read; none of the action buttons on it were clicked.

**A complaint opened from the inbox: category, sub-type, jurisdiction, status, description and map pin**

![A complaint opened from the inbox: category, sub-type, jurisdiction, status, description and map pin](../walkthrough/output/en/16_employee_complaint_detail/01_complaint_detail.png)

**The complaint timeline below it — applied, assigned, then auto-escalated on an SLA breach**

![The complaint timeline below it — applied, assigned, then auto-escalated on an SLA breach](../walkthrough/output/en/16_employee_complaint_detail/02_complaint_workflow_timeline.png)

---

## Employee UI · New complaint intake

The counter-staff intake form: complainant details, the complaint type → category → sub-type cascade, a Leaflet map pin, and a description. Filled in for the capture and **not** submitted.

**The intake form as it loads**

![The intake form as it loads](../walkthrough/output/en/17_employee_new_complaint/01_create_complaint_blank.png)

**Complaint category picker open**

![Complaint category picker open](../walkthrough/output/en/17_employee_new_complaint/02_dropdown_category_open.png)

**County picker open**

![County picker open](../walkthrough/output/en/17_employee_new_complaint/03_dropdown_county_open.png)

**Filled in and left there — SUBMIT was never clicked**

![Filled in and left there — SUBMIT was never clicked](../walkthrough/output/en/17_employee_new_complaint/04_create_complaint_filled_not_submitted.png)

---

## Employee UI · Search complaint

The Search Complaint entry point from the home screen.

**Search Complaint from the home screen — the same inbox surface, opened on its search panel**

![Search Complaint from the home screen — the same inbox surface, opened on its search panel](../walkthrough/output/en/18_employee_search/01_search_complaint_entry.png)

---

## Screen inventory, against the product doc

The rows below follow the *CMS Configurator: Onboarding UI Screens & Windows Inventory* doc —
every trigger it lists, and what this capture could reach. A screen is marked **write** when the
button that opens it POSTs to DIGIT: this capture runs against a live shared deployment and never
writes, so those screens are named here rather than faked.

All **42** triggers the doc lists are accounted for below: **21** captured, **12** behind a write this capture will not perform, **3** blocked by [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies), and **6** that open no new screen of their own — client-side navigation into a phase this capture reaches by URL, a tooltip, a file download, or a dead button.

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

---

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

`ke` holds **2,257 complaints**, where an earlier capture found none across every tenant. The
employee inbox, the complaint registry, the workflow process list and the complaint detail +
workflow-history screens all have data to show.

The console's other counts at capture time: 6 tenants, 33 departments,
50 designations, 778 complaint types, 321 employees,
60 boundaries, 15,492 localization messages.

### 4. Only PGR is enabled in the employee UI

`/dss/*`, `/hrms/*` and `/workbench/*` all fall back to the employee home screen. The employee app on
bomet is PGR-only.

### Incidental: what the cleanup did and did not reach

The tenant registry has been cleaned — 6 tenants, down from the 138 an earlier capture found, so
the `Target Tenant NNNNNN` leftovers are gone from the tenant list and from Phase 1's
*Use Existing Tenant* picker. The boundary hierarchies were not: 273 definitions, 271 of them
`PW_*` (see finding 2).

One side effect worth knowing: the employee city picker now labels tenant `ke` as **Ke** rather than
*Bomet County*. The MDMS record still carries `"name": "Bomet County"`, so digit-ui is falling back
to a prettified code because the label's localization message no longer resolves. `ADMIN` still
exists only at `ke`, so it remains the only selection that authenticates.

---

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
