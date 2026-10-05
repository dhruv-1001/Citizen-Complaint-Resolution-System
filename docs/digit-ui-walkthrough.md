# DIGIT Configurator & Employee UI — visual walkthrough

A screen-by-screen capture of **[bometfeedbackhub.digit.org](https://bometfeedbackhub.digit.org)** —
the DIGIT configurator (4-phase onboarding wizard + management console), the digit-ui employee app,
both citizen apps and the public dashboard. The develop-branch UI (Keycloak sign-in, five-step
onboarding) is captured separately on the develop deployment: [`digit-ui-walkthrough-develop.md`](digit-ui-walkthrough-develop.md).

**104 screens · 22 flows · captured 2026-10-05 · read-only.** Nothing on the deployment was
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
- [Employee UI · File a Complaint](#employee-ui--file-a-complaint)
- [Employee UI · Search complaint](#employee-ui--search-complaint)
- [Employee UI · Dashboard](#employee-ui--dashboard)
- [Citizen UI · /citizen sign-in](#citizen-ui--citizen-sign-in)
- [Citizen UI · /digit-ui/citizen](#citizen-ui--digit-uicitizen)
- [Public dashboard](#public-dashboard)
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

**Select Existing Hierarchy — all 100 entries offered are test leftovers (`PW_*`, `ROOT → MID → LEAF`, `ONLY`, `X`); `ke` now has 285 hierarchy definitions and the screen asks for the first 100, unsorted, so the real `ADMIN` hierarchy is never among them (see [finding 2](#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies))**

![Select Existing Hierarchy — all 100 entries offered are test leftovers (PW_, ROOT → MID → LEAF, ONLY, X); ke now has 285 hierarchy definitions and the screen asks for the first 100, unsorted, so the real ADMIN hierarchy is never among them (see finding 2(#2-phase-4-is-blocked-by-test-leftover-boundary-hierarchies))](../walkthrough/output/en/03_phase2_boundary/05_p2_select_existing_hierarchy.png)

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

**Map Admin Levels — the three levels Overpass returned: 1 city (level 4), 6 distritos municipais (level 5), 63 bairros (level 8). The same city through OCHA COD-AB on the develop deployment gives 7 districts and 64 bairros: OSM is missing KaNyaka**

![Map Admin Levels — the three levels Overpass returned: 1 city (level 4), 6 distritos municipais (level 5), 63 bairros (level 8). The same city through OCHA COD-AB on the develop deployment gives 7 districts and 64 bairros: OSM is missing KaNyaka](../walkthrough/output/en/03_phase2_boundary/15_p2_osm_map_levels.png)

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

**Complaint Categories (the console's new name for complaint types)**

![Complaint Categories (the console's new name for complaint types)](../walkthrough/output/en/09_complaints/02_complaint_types_list.png)

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

`/digit-ui/employee`. City picker, credentials, privacy consent. Tenant `ke` is the only selection that authenticates, because `ADMIN` exists only there. The picker is long again — the `Target Tenant NNNNNN` / `My City Council` / `E2E Roles` test tenants that the August cleanup removed are back — and it still labels `ke` as **Ke**, not *Bomet County*. After sign-in the app opens in the new employee shell (#2038): a full-width top bar carrying the tenant, department and role counts, and a collapsible rail with **Home**, **File a Complaint**, **Search Complaint** and **Dashboard**.

**The employee sign-in screen**

![The employee sign-in screen](../walkthrough/output/en/14_employee_login/01_employee_signin_blank.png)

**The city picker — about seventy entries again, almost all of them test tenants; `ke` is near the bottom as *Ke***

![The city picker — about seventy entries again, almost all of them test tenants; ke is near the bottom as Ke](../walkthrough/output/en/14_employee_login/02_employee_city_picker.png)

**Filled, with privacy consent ticked**

![Filled, with privacy consent ticked](../walkthrough/output/en/14_employee_login/03_employee_signin_filled.png)

**Employee home in the new shell: top bar with tenant · departments · roles, and the rail**

![Employee home in the new shell: top bar with tenant · departments · roles, and the rail](../walkthrough/output/en/14_employee_login/04_employee_home.png)

---

## Employee UI · Complaint inbox

Inbox v2 with its search card and filter rail, and the legacy inbox behind it. It opens on **My Complaints**, which is empty for `ADMIN`; **All Complaints** is the tab that shows the deployment's complaints. The filter now says *Complaint Category*, the name the console uses too.

**Inbox v2 as it opens — search card, filter rail, and the *My Complaints* tab, empty for this operator**

![Inbox v2 as it opens — search card, filter rail, and the My Complaints tab, empty for this operator](../walkthrough/output/en/15_employee_inbox/01_inbox_v2_my_complaints.png)

**The *All Complaints* tab: complaint number, locality, status, current owner and SLA days remaining**

![The All Complaints tab: complaint number, locality, status, current owner and SLA days remaining](../walkthrough/output/en/15_employee_inbox/02_inbox_v2_all_complaints.png)

**The legacy inbox**

![The legacy inbox](../walkthrough/output/en/15_employee_inbox/03_inbox_v1_legacy.png)

---

## Employee UI · Complaint detail & workflow

One complaint opened from the inbox: the detail card, and the complaint timeline below the fold. Opening a complaint is a read; **Take action** and the buttons behind it were not clicked.

**A complaint opened from the inbox: category, subcategory, location, status, description and map pin**

![A complaint opened from the inbox: category, subcategory, location, status, description and map pin](../walkthrough/output/en/16_employee_complaint_detail/01_complaint_detail.png)

**The complaint timeline below it — *Applied*, then *Assigned*, with who acted and their comment**

![The complaint timeline below it — Applied, then Assigned, with who acted and their comment](../walkthrough/output/en/16_employee_complaint_detail/02_complaint_workflow_timeline.png)

---

## Employee UI · File a Complaint

The rebuilt intake form (#2038). Complainant phone and name; a description; **Complaint Category → Complaint Subcategory** as searchable pickers; a Leaflet pin; and the boundary cascade **County → Sub County → Ward**, every level visible from the start. Filled in for the capture and **not** submitted. The base map shows *API KEY REQUIRED* tiles — the CARTO basemap it points at wants a key this deployment does not have.

**File a Complaint as it loads**

![File a Complaint as it loads](../walkthrough/output/en/17_employee_new_complaint/01_create_complaint_blank.png)

**The whole form. In a full-page capture the fixed rail is drawn over the page and the field labels drop out — a screenshot artefact; they render normally on screen (shot above)**

![The whole form. In a full-page capture the fixed rail is drawn over the page and the field labels drop out — a screenshot artefact; they render normally on screen (shot above)](../walkthrough/output/en/17_employee_new_complaint/02_create_complaint_blank_full_page.png)

***Complaint Category* — a searchable picker; test categories (`QA Test Utilities`) are listed beside real ones**

![Complaint Category — a searchable picker; test categories (QA Test Utilities) are listed beside real ones](../walkthrough/output/en/17_employee_new_complaint/03_category_picker_open.png)

***Complaint Subcategory*, scoped to the category picked**

![Complaint Subcategory, scoped to the category picked](../walkthrough/output/en/17_employee_new_complaint/04_subcategory_picker_open.png)

**The boundary cascade starts at *County***

![The boundary cascade starts at County](../walkthrough/output/en/17_employee_new_complaint/05_county_picker_open.png)

**Filled in and left there — SUBMIT was never clicked**

![Filled in and left there — SUBMIT was never clicked](../walkthrough/output/en/17_employee_new_complaint/06_create_complaint_filled_not_submitted.png)

---

## Employee UI · Search complaint

**Search Complaint** on the rail opens the same inbox surface on its search card.

**Search Complaint — the inbox surface, opened on its search card**

![Search Complaint — the inbox surface, opened on its search card](../walkthrough/output/en/18_employee_search/01_search_complaint_entry.png)

---

## Employee UI · Dashboard

`/digit-ui/employee/dashboard` — *Complaint Resolution Operations*, new since the last capture. KPI tiles (resolution rate, breached SLA, resolved complaints, reopen rate, citizen satisfaction) with sparklines, date / ward / type filters, open complaints by workflow stage, a complaint map, and flow ratio by department. The tile layout leaves a large empty block beside the workflow-stage chart at this width.

**Complaint Resolution Operations — filters and KPI tiles**

![Complaint Resolution Operations — filters and KPI tiles](../walkthrough/output/en/19_employee_dashboard/01_dashboard_top.png)

**The whole dashboard: workflow stages, complaint map, flow ratio by department**

![The whole dashboard: workflow stages, complaint map, flow ratio by department](../walkthrough/output/en/19_employee_dashboard/02_dashboard_full_page.png)

**Filters expanded**

![Filters expanded](../walkthrough/output/en/19_employee_dashboard/03_dashboard_filters_open.png)

---

## Citizen UI · /citizen sign-in

The new citizen SPA (digit-ui-v2) at `/citizen`. Sign-in is by Google or by mobile number + OTP. The capture enters a number and stops: **Send OTP** would text a real phone.

**`/citizen` sign-in — Google, or mobile number + OTP**

![/citizen sign-in — Google, or mobile number + OTP](../walkthrough/output/en/20_citizen_v2/01_citizen_v2_signin.png)

**A number entered; *Send OTP* not pressed**

![A number entered; Send OTP not pressed](../walkthrough/output/en/20_citizen_v2/02_citizen_v2_signin_number_entered_not_sent.png)

---

## Citizen UI · /digit-ui/citizen

The classic citizen app, now inside the same shell as the employee app. Signed out it shows **All Services**; **File a Complaint** and **My Complaints** both route to its sign-in.

**Signed out: All Services**

![Signed out: All Services](../walkthrough/output/en/21_citizen_classic/01_citizen_all_services.png)

***File a Complaint* while signed out routes to sign-in**

![File a Complaint while signed out routes to sign-in](../walkthrough/output/en/21_citizen_classic/02_file_a_complaint_signed_out.png)

**So does *My Complaints***

![So does My Complaints](../walkthrough/output/en/21_citizen_classic/03_my_complaints_signed_out.png)

**The classic citizen sign-in**

![The classic citizen sign-in](../walkthrough/output/en/21_citizen_classic/04_citizen_classic_login.png)

---

## Public dashboard

`/digit-ui/public-dashboard` — the anonymous view of the operations dashboard, open to anyone. Its *Complaints by type* chart publishes this deployment's test categories (`QA Test Utilities`, `PWTESTESCALATION`, …) alongside the real ones.

**The public dashboard — no sign-in**

![The public dashboard — no sign-in](../walkthrough/output/en/22_public_dashboard/01_public_dashboard_top.png)

**All of it, including *Complaints by type* with the test categories**

![All of it, including Complaints by type with the test categories](../walkthrough/output/en/22_public_dashboard/02_public_dashboard_full_page.png)

**Filters expanded**

![Filters expanded](../walkthrough/output/en/22_public_dashboard/03_public_dashboard_filters_open.png)

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

### 1. What changed since the 2026-08-24 capture

bomet now runs `master` as of 2026-10-02 (`6f9634f6`). The configurator — sign-in, the 4-phase
wizard, the management console — looks and behaves as it did; the rename of complaint *types* to
**Complaint Categories / Subcategories** is the visible difference there. The employee and citizen
apps changed a lot (#2038):

* **A new shell.** Full-width top bar with the tenant, its department count and the operator's role
  count; a collapsible rail with Home, File a Complaint, Search Complaint and Dashboard.
* **File a Complaint, rebuilt.** Searchable category → subcategory pickers, every boundary level
  shown from the start (County → Sub County → Ward), sticky actions.
* **An employee dashboard** at `/digit-ui/employee/dashboard`, and its anonymous twin at
  `/digit-ui/public-dashboard`.
* **The citizen side** — the new `/citizen` SPA (Google or OTP sign-in) and the classic
  `/digit-ui/citizen` app in the same shell. Neither was in the previous walkthrough.

The develop-branch UI (Keycloak sign-in, the five-step onboarding) is not on bomet; it is
captured on the develop deployment in [`digit-ui-walkthrough-develop.md`](digit-ui-walkthrough-develop.md).

### 2. Phase 4 is blocked by test-leftover boundary hierarchies

Unchanged since August, and slightly worse. Phase 4 still refuses to start — **"No boundaries
found for tenant `ke`"** — although the console lists the real `ADMIN` hierarchy
(`County → SubCounty → Ward`).

`Phase4Page.tsx` takes `getHierarchies(tenant)[0]`, and `boundary.ts` fetches that list unsorted
with `limit: 100`. `ke` now holds **285** hierarchy definitions (273 in August); the 100 the wizard
gets back are all test leftovers — `PW_*`, `ROOT → MID → LEAF`, `ONLY`, `X` — so the first one is a
throwaway hierarchy with no boundaries. The same list is what Phase 2's *Select Existing Hierarchy*
offers, and why the completion page reports `0 boundaries`.

Two fixes still apply: delete the junk (`boundary-hierarchy-definition/_delete` exists and
`utilities/crs_dataloader/unified_loader.py` calls it), and stop picking a hierarchy by array
position out of an unsorted, truncated list.

### 3. The test junk came back

The August cleanup took the tenant registry from 138 to 45. It is at **75** again, and the
`Target Tenant NNNNNN` rows are back in Phase 1's *Use Existing Tenant* picker and in the employee
city picker. The suite keeps writing to this deployment; a one-off cleanup does not hold.

It now reaches people who are not testers: the employee **Complaint Category** picker and the
anonymous **public dashboard** both list test categories (`QA Test Utilities`, `PWTESTESCALATION`)
next to real ones.

### 4. The base map needs a key

File a Complaint's pin map draws *API KEY REQUIRED* tiles. The tile URL points at CARTO's basemaps,
which now require a key; nothing on the form breaks, but the map is unreadable.

### 5. Counts at capture time

From the console's own tiles: 4,731 complaints (5,179 in August), 75 tenants,
42 departments, 50 designations, 1,195 complaint categories,
500 employees, 31 boundaries, 17,777 localization messages,
100 users, 27 access roles.

Only PGR is enabled in the employee app: `/dss/*`, `/hrms/*` and `/workbench/*` still fall back to
the home screen. The new dashboard is the shell's own page, not DSS.

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
.venv/bin/python capture_citizen.py                     # citizen apps + public dashboard
.venv/bin/python build_site.py                          # re-render the HTML only
.venv/bin/python build_doc.py                           # re-render this markdown
```

Host, tenant and credentials default to bomet and are overridable:

```bash
WT_HOST=https://other.digit.org WT_TENANT=xx WT_USER=… WT_PASS=… ./run_all.sh
```

[`walkthrough/README.md`](../walkthrough/README.md) documents the scripts, the route tables they
drive, and the reconnaissance helpers to re-run when the deployment changes.
