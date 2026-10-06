# DIGIT develop UI — visual walkthrough

A screen-by-screen capture of **[141.94.92.163.nip.io](https://141.94.92.163.nip.io/configurator/)** — the develop-branch
DIGIT configurator: Keycloak sign-in, self-serve sign-up, the five-step onboarding carried out for
**Cidade de Maputo** with OCHA COD-AB boundaries, and the management console as the new workspace's
founder sees it; plus the employee and citizen apps.

**80 screens · 11 flows · captured 2026-10-05.** Unlike the bomet walkthrough this one
**writes**: the sign-up and the onboarding steps created a throwaway workspace (authorised for this
capture; see [What was changed on the server](#9-what-was-changed-on-the-server-for-this-capture)).
Everything else was captured read-only.

The `master`-branch UI on bomet — the 4-phase wizard, the employee app's new shell, the citizen apps —
is in [`digit-ui-walkthrough.md`](digit-ui-walkthrough.md).

---

## Contents

- [Sign in · Keycloak](#sign-in--keycloak)
- [Sign up · a new workspace](#sign-up--a-new-workspace)
- [Onboarding · 1 Branding](#onboarding--1-branding)
- [Onboarding · 2 Geography](#onboarding--2-geography)
- [Onboarding · 2b Geography — Preconfigured](#onboarding--2b-geography--preconfigured)
- [Onboarding · 3 Departments](#onboarding--3-departments)
- [Onboarding · 4 Employees](#onboarding--4-employees)
- [Onboarding · 5 Complaints Template](#onboarding--5-complaints-template)
- [Onboarding · finished](#onboarding--finished)
- [Management console · as the new founder](#management-console--as-the-new-founder)
- [Citizen app](#citizen-app)
- [What the capture found on the develop deployment](#what-the-capture-found-on-the-develop-deployment)
- [How this capture was made](#how-this-capture-was-made)

---

## Sign in · Keycloak

`/configurator/` no longer has its own form. **Log in** hands off to Keycloak (realm `digit`, served by the same host under `/auth/`), which is username-first: email, then password, or GitHub. You pick a workspace after signing in. Accounts without a password — anyone who came in through a sign-up link — use **Set up or reset your password**. The `ADMIN / eGov@123` DIGIT account is not a Keycloak user, so it cannot sign in here.

**`/configurator/` — one button, *Log in*; the form lives in Keycloak**

![/configurator/ — one button, Log in; the form lives in Keycloak](../walkthrough/output-develop/en/d01_signin/01_configurator_landing.png)

**Keycloak, step one: email (or GitHub)**

![Keycloak, step one: email (or GitHub)](../walkthrough/output-develop/en/d01_signin/02_keycloak_email_step.png)

**Step two: password**

![Step two: password](../walkthrough/output-develop/en/d01_signin/03_keycloak_password_step.png)

***Set up or reset your password* — a one-use link by mail**

![Set up or reset your password — a one-use link by mail](../walkthrough/output-develop/en/d01_signin/04_password_setup_link_form.png)

***Create an account*: name and email**

![Create an account: name and email](../walkthrough/output-develop/en/d01_signin/05_signup_blank.png)

---

## Sign up · a new workspace

**Create an account** is self-serve: name and email, then a one-use sign-in link by mail. On this deployment mail lands in Mailpit (`/mailpit/`, basic auth). Then three steps — **Account** (name and a derived code), **Preferences** (country, languages, time zone, financial year, URL slug, the founder's mobile), **Review** — and a provisioning run that creates the tenant, the organisation, the founder's DIGIT login and their roles.

The account below is the throwaway workspace this walkthrough onboarded: **Cidade de Maputo**, code `MZ-CDM`, tenant `cidadedemaputo`, Mozambique, English + Portuguese, `Africa/Maputo`, January–December. Provisioning hits a timing race on this deployment and is finished by the backend's own retries a few minutes later; the error it shows in between is described in [finding 3](#3-sign-up-provisioning-fails-on-a-read-after-write-race) rather than pictured.

**Filled in**

![Filled in](../walkthrough/output-develop/en/d02_signup/01_signup_filled.png)

**Check your email**

![Check your email](../walkthrough/output-develop/en/d02_signup/02_signup_check_email.png)

**The sign-in link, caught by Mailpit**

![The sign-in link, caught by Mailpit](../walkthrough/output-develop/en/d02_signup/03_mailpit_signin_link_email.png)

**Back from the link: email verified, now name the account**

![Back from the link: email verified, now name the account](../walkthrough/output-develop/en/d02_signup/04_account_email_verified.png)

***Cidade de Maputo* — the code `CDM` is derived from the name**

![Cidade de Maputo — the code CDM is derived from the name](../walkthrough/output-develop/en/d02_signup/05_account_name_and_code.png)

**Preferences**

![Preferences](../walkthrough/output-develop/en/d02_signup/06_preferences_blank.png)

**Picking Mozambique pre-fills `Africa/Maputo` and the slug `cidade-de-maputo`, but not Portuguese**

![Picking Mozambique pre-fills Africa/Maputo and the slug cidade-de-maputo, but not Portuguese](../walkthrough/output-develop/en/d02_signup/07_preferences_mozambique_defaults.png)

**Portuguese added, financial year January–December, founder's mobile**

![Portuguese added, financial year January–December, founder's mobile](../walkthrough/output-develop/en/d02_signup/08_preferences_filled.png)

**Review — the code is now `MZ-CDM`**

![Review — the code is now MZ-CDM](../walkthrough/output-develop/en/d02_signup/09_review.png)

**Provisioning: account, organisation, membership, permissions, DIGIT login**

![Provisioning: account, organisation, membership, permissions, DIGIT login](../walkthrough/output-develop/en/d02_signup/10_provisioning.png)

**Provisioned — choose the workspace**

![Provisioned — choose the workspace](../walkthrough/output-develop/en/d02_signup/11_choose_workspace.png)

---

## Onboarding · 1 Branding

Logo, organisation name (read-only here; it lives in Workspace settings) and one of three brand themes. The logo is a generated *CM* monogram, not the municipality's crest. **Save and continue** unlocks Geography.

**Branding, 0 of 5 done, every later step locked**

![Branding, 0 of 5 done, every later step locked](../walkthrough/output-develop/en/d03_branding/01_branding_blank.png)

**Logo uploaded**

![Logo uploaded](../walkthrough/output-develop/en/d03_branding/02_branding_logo_uploaded.png)

**Green and Gold theme selected**

![Green and Gold theme selected](../walkthrough/output-develop/en/d03_branding/03_branding_green_and_gold.png)

---

## Onboarding · 2 Geography

Three sources: *Preconfigured* (coming soon), **Fetch boundaries**, and **Upload from Excel**. Fetch boundaries searches turbopass, which is now deployed on this box itself, with the same official boundary DB as naipepea.

The source is **OCHA COD-AB** — the best set for Mozambique in the #1994 evaluation (COD *enhanced*, 2025). For Mozambique the default *Official* source resolves to the same set; it is picked explicitly here so the screenshots name it. COD-AB gives Cidade de Maputo four nested levels with no gaps: 1 province-level city → 7 districts → 7 administrative posts → 64 bairros, 79 areas. In Maputo city the districts and the administrative posts are the same seven places, and the level picker only accepts a contiguous range, so dropping the duplicate would also drop either the city or the bairros. All four are kept, named *Cidade → Distrito Municipal → Posto Administrativo → Bairro*.

For comparison, OpenStreetMap (bomet's Overpass path) returns three levels for the same city — 1 / 6 / 63 — and misses the KaNyaka district.

**Geography: Preconfigured (coming soon), Fetch boundaries, Upload from Excel**

![Geography: Preconfigured (coming soon), Fetch boundaries, Upload from Excel](../walkthrough/output-develop/en/d04_geography/01_geography_choose_source.png)

**Fetch boundaries — source picker, area search, optional map provider**

![Fetch boundaries — source picker, area search, optional map provider](../walkthrough/output-develop/en/d04_geography/02_fetch_boundaries.png)

**Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture**

![Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture](../walkthrough/output-develop/en/d04_geography/03_boundary_source_options.png)

**COD-AB suggestion: *Cidade de Maputo — Province, Moçambique · L1 · 78 sub-areas***

![COD-AB suggestion: Cidade de Maputo — Province, Moçambique · L1 · 78 sub-areas](../walkthrough/output-develop/en/d04_geography/04_cod_suggestions.png)

**Map Admin Levels — licence line, a data check (79 areas, every level fully nested), and the polygons on the map**

![Map Admin Levels — licence line, a data check (79 areas, every level fully nested), and the polygons on the map](../walkthrough/output-develop/en/d04_geography/05_cod_map_admin_levels.png)

**All four levels named; *Create Hierarchy & Boundaries* writes**

![All four levels named; Create Hierarchy & Boundaries writes](../walkthrough/output-develop/en/d04_geography/06_levels_named.png)

**Boundaries created — 79 areas in four levels, with the licence line**

![Boundaries created — 79 areas in four levels, with the licence line](../walkthrough/output-develop/en/d04_geography/07_boundaries_created.png)

**Back on Geography: one hierarchy, *1 cidade · 7 distrito municipals · 7 posto administrativos · 64 bairros* (English plurals on Portuguese names)**

![Back on Geography: one hierarchy, 1 cidade · 7 distrito municipals · 7 posto administrativos · 64 bairros (English plurals on Portuguese names)](../walkthrough/output-develop/en/d04_geography/08_geography_with_hierarchy.png)

---

## Onboarding · 2b Geography — Preconfigured

The **Preconfigured** source (PR #2311, deployed on this server on 2026-10-06). The card already knows the workspace's country — from the tenant record, else the founder's dial code (+258 → Mozambique) — and the best boundary set for it. **Use these boundaries** opens the same search as Fetch boundaries, but with the source **fixed** to that official set, a **High / Medium / Low** confidence tag and a one-line headline; suggestions are limited to the country.

The tag comes from how far a second, independently drawn source (here geoBoundaries) agrees, level by level: *High* when every level it has is confirmed, *Medium* when some only partly match or the other source is years older, *Low* when nothing could be cross-checked. Mozambique is **Medium**: provinces confirmed, districts and administrative posts partly match an older source, localities exist in one source only. *One source only* means a level could not be checked, not that it is wrong.

**Geography: the *Preconfigured* card names Mozambique's official set, its levels, a confidence tag and the headline**

![Geography: the Preconfigured card names Mozambique's official set, its levels, a confidence tag and the headline](../walkthrough/output-develop/en/d04b_preconfigured/01_geography_preconfigured_card.png)

**Use these boundaries → the Fetch search, with the source fixed to Mozambique's official set: *Medium confidence*, OCHA COD-AB · Jan 2025**

![Use these boundaries → the Fetch search, with the source fixed to Mozambique's official set: Medium confidence, OCHA COD-AB · Jan 2025](../walkthrough/output-develop/en/d04b_preconfigured/02_preconfigured_search.png)

**Suggestions come only from Mozambique's official set**

![Suggestions come only from Mozambique's official set](../walkthrough/output-develop/en/d04b_preconfigured/03_preconfigured_suggestions.png)

**The level screen for Cidade de Maputo: the same summary and tag, the data check, the polygons**

![The level screen for Cidade de Maputo: the same summary and tag, the data check, the polygons](../walkthrough/output-develop/en/d04b_preconfigured/04_preconfigured_levels.png)

**Each level with its status against the second source — *Confirmed*, *Partly confirmed · n%*, *One source only***

![Each level with its status against the second source — Confirmed, Partly confirmed · n%, One source only](../walkthrough/output-develop/en/d04b_preconfigured/05_per_level_confidence.png)

**Boundaries created — 79 areas in four levels, with the licence line**

![Boundaries created — 79 areas in four levels, with the licence line](../walkthrough/output-develop/en/d04b_preconfigured/06_boundaries_created.png)

---

## Onboarding · 3 Departments

Departments and designations, typed in or uploaded. A new workspace starts with `ONBOARDING_ADMIN` / Administration and the founder's `ONBOARDING_FOUNDER` designation. Added: Solid Waste and Sanitation, Roads and Drainage, Markets and Fairs, Parks and Public Spaces; designations Grievance Redressal Officer and Field Officer, linked to all four. Codes are derived from the names.

**Departments as a new workspace starts**

![Departments as a new workspace starts](../walkthrough/output-develop/en/d05_departments/01_departments_seeded.png)

**Upload a departments file, with a template to download**

![Upload a departments file, with a template to download](../walkthrough/output-develop/en/d05_departments/02_departments_upload.png)

**Add department — code derived from the name**

![Add department — code derived from the name](../walkthrough/output-develop/en/d05_departments/03_add_department.png)

**Add designation, linked to departments**

![Add designation, linked to departments](../walkthrough/output-develop/en/d05_departments/04_add_designation.png)

**Five departments, three designations**

![Five departments, three designations](../walkthrough/output-develop/en/d05_departments/05_departments_filled.png)

---

## Onboarding · 4 Employees

Add people one at a time or upload a staff list. Each employee gets departments (the first is their main one), a designation, system roles and jurisdictions; they are created in HRMS and invited to the identity service. Seven in the end: the founder, one GRO per complaint department, and two field officers (`PGR_LME`). Two things went wrong on the way — [finding 5](#5-email-optional-is-required) and [finding 6](#6-an-expired-identity-session-breaks-writes-without-saying-so).

**Employees: create manually or bulk upload**

![Employees: create manually or bulk upload](../walkthrough/output-develop/en/d06_employees/01_employees_landing.png)

**Bulk upload**

![Bulk upload](../walkthrough/output-develop/en/d06_employees/02_employees_upload.png)

**Add an employee — note *Email (optional)*, and that *System roles* lists every role, `SUPERUSER` and `INTERNAL_MICROSERVICE_ROLE` included**

![Add an employee — note Email (optional), and that System roles lists every role, SUPERUSER and INTERNAL_MICROSERVICE_ROLE included](../walkthrough/output-develop/en/d06_employees/03_employee_form_blank.png)

**A field officer: Roads and Drainage, `EMPLOYEE` + `PGR_LME`, jurisdiction Nhlamankulo**

![A field officer: Roads and Drainage, EMPLOYEE + PGR_LME, jurisdiction Nhlamankulo](../walkthrough/output-develop/en/d06_employees/04_employee_form_filled.png)

**Three employees plus the founder — whose roles include `SUPERUSER` and `INTERNAL_MICROSERVICE_ROLE`**

![Three employees plus the founder — whose roles include SUPERUSER and INTERNAL_MICROSERVICE_ROLE](../walkthrough/output-develop/en/d06_employees/05_employees_list.png)

**Seven employees: the founder, one GRO per complaint department, two field officers**

![Seven employees: the founder, one GRO per complaint department, two field officers](../walkthrough/output-develop/en/d06_employees/06_employees_one_gro_per_department.png)

---

## Onboarding · 5 Complaints Template

Complaint categories, each handled by one department, with subcategories one per line, and one resolution target for all of them. Four categories, fourteen subcategories, 3 days. **Finish setup** was refused the first time — [finding 4](#4-finish-setup-needs-one-gro-per-department-and-does-not-say-so) — and went through once every complaint department had its own GRO.

**Complaints Template: start from scratch or bulk upload**

![Complaints Template: start from scratch or bulk upload](../walkthrough/output-develop/en/d07_complaints/01_complaints_landing.png)

**Bulk upload**

![Bulk upload](../walkthrough/output-develop/en/d07_complaints/02_complaints_upload.png)

**Add a complaint category: name, handling department, subcategories one per line**

![Add a complaint category: name, handling department, subcategories one per line](../walkthrough/output-develop/en/d07_complaints/03_add_category.png)

**Four categories, fourteen subcategories, 3-day target**

![Four categories, fourteen subcategories, 3-day target](../walkthrough/output-develop/en/d07_complaints/04_four_categories_sla_3_days.png)

---

## Onboarding · finished

Each step revisited after **Finish setup**, read-only: the state an administrator comes back to.

**Back in Onboarding after setup: all five steps done — Branding**

![Back in Onboarding after setup: all five steps done — Branding](../walkthrough/output-develop/en/d08_onboarding_done/01_branding_done.png)

**Geography, done**

![Geography, done](../walkthrough/output-develop/en/d08_onboarding_done/02_geography_done.png)

**Departments, done**

![Departments, done](../walkthrough/output-develop/en/d08_onboarding_done/03_departments_done.png)

**Employees, done**

![Employees, done](../walkthrough/output-develop/en/d08_onboarding_done/04_employees_done.png)

**Complaints Template, done**

![Complaints Template, done](../walkthrough/output-develop/en/d08_onboarding_done/05_complaints_template_done.png)

---

## Management console · as the new founder

Every route of the develop console, opened by the account that created the workspace, after the permission fix in [finding 1](#1-the-founder-was-denied-two-console-calls--fixed-for-this-workspace). Four screens are not pictured because they render an error or operator jargon on this deployment — Notification Channels, Notification Providers, Configure Notifications ([finding 10](#10-notification-channels-and-providers-error-on-this-server)) and Boundary Hierarchies ([finding 8](#8-geography-details)).

**Console home — every registry count for the new workspace**

![Console home — every registry count for the new workspace](../walkthrough/output-develop/en/d09_manage/01_dashboard_home.png)

**Public Dashboard**

![Public Dashboard](../walkthrough/output-develop/en/d09_manage/02_public_dashboard.png)

**Tenants — the workspace's own tenant**

![Tenants — the workspace's own tenant](../walkthrough/output-develop/en/d09_manage/03_tenants.png)

**Departments — the five from onboarding**

![Departments — the five from onboarding](../walkthrough/output-develop/en/d09_manage/04_departments.png)

**Designations**

![Designations](../walkthrough/output-develop/en/d09_manage/05_designations.png)

**Boundaries — 80 (79 imported + the workspace root), 79 with map geometry**

![Boundaries — 80 (79 imported + the workspace root), 79 with map geometry](../walkthrough/output-develop/en/d09_manage/06_boundaries.png)

**Map Configuration**

![Map Configuration](../walkthrough/output-develop/en/d09_manage/07_map_configuration.png)

**Complaints — status tabs; none filed yet**

![Complaints — status tabs; none filed yet](../walkthrough/output-develop/en/d09_manage/08_complaints.png)

**Complaint Categories — the 4 categories and their subcategories, by department**

![Complaint Categories — the 4 categories and their subcategories, by department](../walkthrough/output-develop/en/d09_manage/09_complaint_types.png)

**Complaint Hierarchies — `PGR`: category → subcategory**

![Complaint Hierarchies — PGR: category → subcategory](../walkthrough/output-develop/en/d09_manage/10_complaint_hierarchies.png)

**Localization — 3,490 messages, English and Portuguese columns**

![Localization — 3,490 messages, English and Portuguese columns](../walkthrough/output-develop/en/d09_manage/11_localization.png)

**Employees — all seven**

![Employees — all seven](../walkthrough/output-develop/en/d09_manage/12_employees.png)

**Org Chart — seven employees; no reporting lines set yet**

![Org Chart — seven employees; no reporting lines set yet](../walkthrough/output-develop/en/d09_manage/13_org_chart.png)

**Users — citizen accounts; none yet**

![Users — citizen accounts; none yet](../walkthrough/output-develop/en/d09_manage/14_users.png)

**Access Roles — 27**

![Access Roles — 27](../walkthrough/output-develop/en/d09_manage/15_access_roles.png)

**Workflow Business Services**

![Workflow Business Services](../walkthrough/output-develop/en/d09_manage/16_workflows.png)

**Workflow Processes — none until a complaint is filed**

![Workflow Processes — none until a complaint is filed](../walkthrough/output-develop/en/d09_manage/17_processes.png)

**MDMS Schemas**

![MDMS Schemas](../walkthrough/output-develop/en/d09_manage/18_mdms_schemas.png)

**Analytics Providers**

![Analytics Providers](../walkthrough/output-develop/en/d09_manage/19_analytics_providers.png)

**Event Catalogue (read-only; events come from the modules)**

![Event Catalogue (read-only; events come from the modules)](../walkthrough/output-develop/en/d09_manage/20_notification_event_catalogue.png)

**Notification Routing**

![Notification Routing](../walkthrough/output-develop/en/d09_manage/21_notification_routing.png)

**Notification Templates**

![Notification Templates](../walkthrough/output-develop/en/d09_manage/22_notification_templates.png)

**Provider Templates**

![Provider Templates](../walkthrough/output-develop/en/d09_manage/23_notification_provider_templates.png)

**Notification Logs**

![Notification Logs](../walkthrough/output-develop/en/d09_manage/24_notification_logs.png)

**Notification Preferences**

![Notification Preferences](../walkthrough/output-develop/en/d09_manage/25_notification_preferences.png)

**Advanced — every MDMS master**

![Advanced — every MDMS master](../walkthrough/output-develop/en/d09_manage/26_advanced_all_masters.png)

---

## Citizen app

`/citizen`, the digit-ui-v2 citizen sign-in (mobile number + OTP; no OTP was sent). The employee app and the public dashboard URL do not load on this deployment and are described in [finding 2](#2-the-employee-app-does-not-load) instead.

**`/citizen` — the digit-ui-v2 citizen sign-in (mobile + OTP; not sent)**

![/citizen — the digit-ui-v2 citizen sign-in (mobile + OTP; not sent)](../walkthrough/output-develop/en/d10_apps/01_citizen_signin.png)

---

## What the capture found on the develop deployment

### 1. The founder was denied two console calls — fixed for this workspace

When this capture first opened the console, Kong refused two calls for the founder, and nearly every
list screen makes one of them — so most of the console read *AccessDeniedException*:

```
POST /mdms-v2/v2/_count               every list total and dashboard tile
POST /pgr-services/v2/request/_search complaint lists
```

The founder's roles (`EMPLOYEE, SUPERUSER, ACCOUNT_ADMIN, MDMS_ADMIN, LOC_ADMIN, HRMS_ADMIN,
WORKFLOW_ADMIN, INTERNAL_MICROSERVICE_ROLE`, all at the new tenant) come from the sign-up seed,
`platform-baseline-v1.json` in pgr-services. That seed had **no action at all for
`/mdms-v2/v2/_count`** (Kong lets `/mdms-v2/v2/_search` through without a role check, but not
`_count`), and granted `request/_search` only to complaint-handling roles. Older tenants never hit
this because their grants come from the full database seed.

**Status.** The seed is fixed upstream — the founder now gets every call the console makes
(301 actions / 633 grants, up from 294 / 612), merged into the identity onboarding branch behind
PR #2269, which is still open. This deployment's pgr-services (`identity-4407f9556`) predates that
fix, so **workspaces signed up here still get the old seed**; `cidadedemaputo` was patched directly
on the server, and the console screens above were re-captured after the patch. Per screen, the API
calls each made and how many were refused (26 routes):

| Screen | API calls | Refused (401/403) |
| --- | ---: | ---: |
| Console home | 30 | 0 |
| Public Dashboard | 7 | 0 |
| Tenants | 8 | 0 |
| Departments | 8 | 0 |
| Designations | 8 | 0 |
| Boundaries | 12 | 0 |
| Map Configuration | 9 | 0 |
| Complaints | 10 | 0 |
| Complaint Categories | 13 | 0 |
| Complaint Hierarchies | 8 | 0 |
| Localization | 12 | 0 |
| Employees | 15 | 0 |
| Org Chart | 9 | 0 |
| Users | 7 | 0 |
| Access Roles | 7 | 0 |
| Workflow Business Services | 7 | 0 |
| Workflow Processes | 7 | 0 |
| MDMS Schemas | 7 | 0 |
| Analytics Providers | 8 | 0 |
| Event Catalogue (read-only; events come from the modules) | 8 | 0 |
| Notification Routing | 8 | 0 |
| Notification Templates | 8 | 0 |
| Provider Templates | 8 | 0 |
| Notification Logs | 7 | 0 |
| Notification Preferences | 7 | 0 |
| Advanced | 6 | 0 |

### 2. The employee app does not load

`/kd/digit-ui/employee` returns its HTML, but the page asks for its scripts and styles at
`/digit-ui/index.js`, `/digit-ui/globalConfigs.js`, `/digit-ui/vendor/*.css` — and the vhost
answers every request that *starts* with `/digit-ui/` with 404:

```nginx
location /digit-ui/ {
  if ($request_uri ~ "^/digit-ui/") { return 404; }
  proxy_pass http://127.0.0.1:18080;
}
```

That guard is meant to force the tenant-scoped URL, but the bundle's asset paths are absolute, so it
also blocks the bundle. The employee app is blank for every tenant slug; so is
`/<slug>/digit-ui/citizen`. The digit-ui-v2 citizen app at `/citizen` is unaffected. The public
dashboard URL (`/digit-ui/public-dashboard`) is switched off on this vhost and returns 404.

### 3. Sign-up provisioning fails on a read-after-write race

Both sign-ups made for this capture hit it. The first **Create account** ended in *Setup did not
finish — MDMS_SCHEMA_NOT_VISIBLE*; a second, made to re-check it, ended in the record-level
variant, *MDMS_RECORD_NOT_VISIBLE*. Provisioning
creates the tenant's MDMS schemas and immediately searches for each one; MDMS creates schemas
asynchronously (`schema/v1/_create` → 202), so the search right after came back empty and
`OnboardingSteps.ensureSchema` gave up. Five seconds later the same search returned the schema.
The error is marked retryable and the backend finished on its own both times — after about one
and three minutes — and reloading the page then showed the workspace. But the screen in between
tells the person their setup failed and offers **Try again**.

On the same flow: the Account step checks that the *code* is free ("Available.") but not the
*name*. Organisation names are unique, so a taken name passes every step and is refused only at
**Create account** — *Could not continue — ORGANIZATION_NAME is already in use*.

### 4. Finish setup needs one GRO per department, and does not say so

**Finish setup** returned `409 WORKSPACE_PROBE_INCOMPLETE`, shown as a red toast with that code and
nothing else. The probe behind it (`WorkspaceGateway.probe`, step `COMPLAINT_TYPES`) wants every
department that handles a complaint category to have an active employee with the `GRO` role whose
**current** assignment is that department — "a department with no GRO strands its complaints in
PENDINGFORASSIGNMENT".

The Employees form invites the opposite reading: it lets you tick several departments for one GRO
("the first is their main one"). HRMS keeps one current assignment, so a GRO ticked for four
departments covers only the first. Adding one GRO per department fixed it. The form could say so,
and the toast could name the departments missing a GRO.

### 5. "Email (optional)" is required

The employee form labels email *optional*; leaving it empty fails with *Enter a valid email to
invite this employee*, because every employee is also invited to the identity service.

### 6. An expired identity session breaks writes without saying so

About an hour after signing in, the identity (BFF) session had expired while the configurator's
DIGIT token was still valid. The UI kept working until a write needed the identity service: the
invite for one employee failed with `401` — *Employee CMM-GRO-004 exists in HRMS; invitation is
unfinished. Retry with the same code and email. An identity session is required* — leaving the
employee half-created. Nothing prompted a fresh sign-in. And an account created from a sign-up
link has no password, so getting a session back meant going through **Set up or reset your
password** first.

### 7. Roles: the founder gets an internal one, and the employee form offers all of them

The founder is provisioned with `INTERNAL_MICROSERVICE_ROLE` alongside `SUPERUSER`. The Employees
form's **System roles** list offers every role in the system — `SUPERUSER`, `SYSTEM`,
`INTERNAL_MICROSERVICE_ROLE`, `QA_AUTOMATION`, `ANONYMOUS`, `CITIZEN` — to an onboarding admin.
This capture did not try granting them; whether the backend would accept them is untested.

### 8. Geography details

* The success message says *Successfully generated 79 boundaries from OSM data*; the source was
  OCHA COD-AB.
* The summary pluralises Portuguese level names in English: *7 distrito municipals · 7 posto
  administrativos*.
* After the import the configurator fires `POST /v1/tools/fix_boundary_paths` at the MCP REST shim.
  Nothing routes `/v1/tools/` on this host, so it 404s and the path repair — which keeps the
  citizen complaint form from listing a boundary twice — does not run. The configurator treats it
  as fire-and-forget; nothing on screen shows it.
* COD-AB's levels 2 and 3 are the same seven places in Maputo city (see the Geography section).
* The console's **Boundary Hierarchies** list shows its *Levels* column header as the raw
  translation key `app.fields.levels`, so that screen is not pictured.

### 9. What was changed on the server for this capture

Authorised for this walkthrough, and kept in place:

* **turbopass** — `turbopass-search:local` built from `turbopass/` at `b015ade7`, running on
  `127.0.0.1:13301`, reading the official boundary DB copied from naipepea
  (`/opt/turbopass/overture-data/boundaries.sqlite`, 12 countries, checksum-verified); and a
  `location /turbopass/` block in the vhost (backup taken first). The host's Ansible inventory does
  not set `enable_turbopass`, so a redeploy from it would remove both.
* **The Cidade de Maputo workspace** — tenant `cidadedemaputo`, 79 boundaries, 5 departments,
  3 designations, 7 employees, 4 categories / 14 subcategories at 72 h, owned by the throwaway
  account `walkthrough.maputo@example.com` (mail in Mailpit).
* **A second workspace** — *Conselho Municipal de Maputo*, code `CMM`, slug `maputo`, owned by
  `walkthrough.signup@example.com`; signed up to re-check finding 3. The first version of
  Preconfigured loaded the whole country into it (2,342 areas; the run was stopped with 2,095
  linked) before Preconfigured was changed to search instead.
* **PR #2311 (Preconfigured), deployed 2026-10-06** — configurator and turbopass only:
  * the configurator bundle in `/var/www/configurator` was rebuilt from the deployed identity source
    with the PR's configurator changes merged on top (three-way, no conflicts), and rebuilt again
    for the PR's search-based Preconfigured (`1a331f681`); the bundle from before the PR is kept in
    `/var/www/configurator.bak-pre-pr2311-*`, the first PR build in `…bak-pr2311-v1-*`;
  * `turbopass-search` now runs the PR's search-api (`turbopass-search:pr2311`, adds
    `GET /boundary/official`) against a boundary DB that carries the cross-source agreement
    (`/opt/turbopass/overture-data-preconfigured`); the previous container is kept, stopped, as
    `turbopass-search-prev-*`, and the previous DB is untouched.

No other tenant was touched.

Separately, and not changed: this host publishes several container ports straight to the internet,
including Postgres (`15432`) and Redis (`16379`).

### 10. Notification Channels and Providers error on this server

Both screens render an error for every tenant here, so they are not pictured. novu-bridge's calls to
Novu are rejected — `NB_NOVU_INTEGRATIONS_FAILED: 401 Unauthorized` — which points at a stale Novu API
key in the bridge's configuration; and the console asks for `/novu-adapter/v1/providers/catalog`,
which the deployed novu-bridge (`master-7c91934`) does not have yet — the configurator is newer than
the bridge. **Configure Notifications** loads, but a new workspace has no notification setup, so it shows a
large warning written for operators (*No notification configuration on this tenant* … `NB_NO_ROUTING`
… `./deploy.sh <tenant> --tags notifications`) above *No events declared*; it is not pictured
either.

---

## How this capture was made

Two kinds of screen are in this document, and they were made differently.

* **The sign-up and the five onboarding steps write.** They were driven once, click by click, on
  2026-10-05, against a new throwaway workspace — that was the point: the steps unlock one after
  another, so stopping before each save would have shown only Branding. Their screenshots are
  imported by [`walkthrough/import_develop_run.py`](../walkthrough/import_develop_run.py).
* **Everything else is read-only.** [`walkthrough/capture_develop.py`](../walkthrough/capture_develop.py)
  revisits the finished steps, the console and the apps behind the same request guard as the bomet
  capture; it ended with `read-only guard: no mutating requests were attempted`.

```bash
cd walkthrough
WT_HOST=https://141.94.92.163.nip.io WT_OUT=output-develop \
WT_KC_EMAIL=… WT_KC_PASS=… .venv/bin/python capture_develop.py
.venv/bin/python import_develop_run.py /path/to/run/shots     # the onboarding run's screenshots
WT_OUT=output-develop .venv/bin/python build_site_develop.py
.venv/bin/python build_doc_develop.py
```

The interactive sitemap and grid gallery for this capture are in
[`walkthrough/output-develop/`](../walkthrough/output-develop) — `index.html` and `gallery.html`.
