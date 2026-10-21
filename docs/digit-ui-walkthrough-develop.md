# DIGIT configurator on `develop` — visual walkthrough

A screen-by-screen capture of the DIGIT configurator as it is on the `develop` branch
(`f713f9e6c`): Keycloak sign-in, self-serve sign-up, the onboarding Home and tour, the five
onboarding steps carried out for **Cidade de Maputo** with Mozambique's official boundaries, the
account pages, and the management console.

**78 screens · 11 flows · captured 2026-10-21 on a local develop stack.** The sign-up
and onboarding steps created a throwaway workspace on that local stack; everything else was
captured read-only. See [How this capture was made](#how-this-capture-was-made).

The `master`-branch UI on bomet is in [`digit-ui-walkthrough.md`](digit-ui-walkthrough.md).

---

## Contents

- [Sign in · Keycloak](#sign-in--keycloak)
- [Sign up · a new workspace](#sign-up--a-new-workspace)
- [Onboarding · Home and welcome tour](#onboarding--home-and-welcome-tour)
- [Onboarding · 1 Branding](#onboarding--1-branding)
- [Onboarding · 2 Geography](#onboarding--2-geography)
- [Onboarding · 2b Geography — Preconfigured](#onboarding--2b-geography--preconfigured)
- [Onboarding · 3 Departments](#onboarding--3-departments)
- [Onboarding · 4 Employees](#onboarding--4-employees)
- [Onboarding · 5 Complaints Template](#onboarding--5-complaints-template)
- [Account menu](#account-menu)
- [Management console](#management-console)
- [API calls per console screen](#api-calls-per-console-screen)
- [What changed since the 2026-10-05 capture](#what-changed-since-the-2026-10-05-capture)
- [What is not pictured](#what-is-not-pictured)
- [How this capture was made](#how-this-capture-was-made)

---

## Sign in · Keycloak

`/configurator/` has no form of its own. **Log in** hands off to Keycloak, which asks for the email first, then the password; you choose a workspace after signing in. Accounts that came in through a sign-up link have no password until they use **Set up or reset your password**.

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

**Create an account** is self-serve: name and email, then a one-use sign-in link by mail (on this stack the mail lands in Mailpit). Then three steps — **Account** (name and a code derived from it), **Preferences** (country, languages, time zone, financial year, URL slug, the founder's mobile), **Review** — and the provisioning screen while the workspace, its basics, the founder's employee record, account, membership and sign-in are created.

The workspace onboarded in this walkthrough is a throwaway: **Cidade de Maputo**, Mozambique, English + Portuguese, `Africa/Maputo`, January–December.

**Filled in**

![Filled in](../walkthrough/output-develop/en/d02_signup/01_signup_filled.png)

**Check your email**

![Check your email](../walkthrough/output-develop/en/d02_signup/02_signup_check_email.png)

**Back from the link: email verified, now name the account**

![Back from the link: email verified, now name the account](../walkthrough/output-develop/en/d02_signup/03_account_email_verified.png)

***Cidade de Maputo* — the code is derived from the name and checked as you type**

![Cidade de Maputo — the code is derived from the name and checked as you type](../walkthrough/output-develop/en/d02_signup/04_account_name_and_code.png)

**Preferences**

![Preferences](../walkthrough/output-develop/en/d02_signup/05_preferences_blank.png)

**Picking Mozambique fills in the time zone and the URL slug**

![Picking Mozambique fills in the time zone and the URL slug](../walkthrough/output-develop/en/d02_signup/06_preferences_mozambique_defaults.png)

**Portuguese added, financial year January–December, founder's mobile**

![Portuguese added, financial year January–December, founder's mobile](../walkthrough/output-develop/en/d02_signup/07_preferences_filled.png)

**Review**

![Review](../walkthrough/output-develop/en/d02_signup/08_review.png)

**Setting up Cidade de Maputo**

![Setting up Cidade de Maputo](../walkthrough/output-develop/en/d02_signup/09_provisioning.png)

---

## Onboarding · Home and welcome tour

Provisioning lands on the onboarding **Home**. A six-slide tour explains what onboarding is and what each step is for; it can be reopened with **Take a tour**. Home shows the next step to do, short **Learn the basics** videos, and a **Documentation** panel that every step carries on its right-hand side.

**Welcome tour 1 of 6 — what onboarding is for**

![Welcome tour 1 of 6 — what onboarding is for](../walkthrough/output-develop/en/d02b_home/01_tour_1_what_onboarding_is.png)

**2 — Complaints Template: what citizens can report, and who handles it**

![2 — Complaints Template: what citizens can report, and who handles it](../walkthrough/output-develop/en/d02b_home/02_tour_2_complaints_template.png)

**3 — Branding**

![3 — Branding](../walkthrough/output-develop/en/d02b_home/03_tour_3_branding.png)

**4 — Geography**

![4 — Geography](../walkthrough/output-develop/en/d02b_home/04_tour_4_geography.png)

**5 — Departments and Employees**

![5 — Departments and Employees](../walkthrough/output-develop/en/d02b_home/05_tour_5_departments_employees.png)

**6 — reopen the tour any time; every step has documentation**

![6 — reopen the tour any time; every step has documentation](../walkthrough/output-develop/en/d02b_home/06_tour_6_reopen.png)

**Onboarding Home: the next step, *Learn the basics* videos, documentation**

![Onboarding Home: the next step, Learn the basics videos, documentation](../walkthrough/output-develop/en/d02b_home/07_onboarding_home.png)

---

## Onboarding · 1 Branding

Logo, account name (changed in Workspace settings) and one of three brand themes. The logo is a generated *CM* monogram, not the municipality's crest. **Save and continue** unlocks Geography.

**Branding, with every later step still locked**

![Branding, with every later step still locked](../walkthrough/output-develop/en/d03_branding/01_branding_blank.png)

**Logo uploaded**

![Logo uploaded](../walkthrough/output-develop/en/d03_branding/02_branding_logo_uploaded.png)

**Green and Gold theme selected**

![Green and Gold theme selected](../walkthrough/output-develop/en/d03_branding/03_branding_green_and_gold.png)

---

## Onboarding · 2 Geography

Three sources. **Preconfigured boundaries** already knows the country — Mozambique, from sign-up — and offers its official boundary set with a confidence tag and the source line. **Fetch boundaries** searches the boundary service with a choice of source. **Upload from Excel** starts by defining the hierarchy's levels.

The Fetch and Excel screens below are read-only: nothing was created from them. The boundaries were brought in through Preconfigured, in the next section.

**Geography: *Preconfigured boundaries* (Mozambique, Medium confidence, OCHA COD-AB · Jan 2025), Fetch boundaries, Upload from Excel**

![Geography: Preconfigured boundaries (Mozambique, Medium confidence, OCHA COD-AB · Jan 2025), Fetch boundaries, Upload from Excel](../walkthrough/output-develop/en/d04_geography/01_geography_choose_source.png)

**Fetch boundaries — source, area search, optional map provider**

![Fetch boundaries — source, area search, optional map provider](../walkthrough/output-develop/en/d04_geography/02_fetch_boundaries.png)

**Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture**

![Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture](../walkthrough/output-develop/en/d04_geography/03_boundary_source_options.png)

**Typing a place: suggestions with level and number of areas inside**

![Typing a place: suggestions with level and number of areas inside](../walkthrough/output-develop/en/d04_geography/04_fetch_suggestions.png)

**The level screen Fetch opens — not created from here**

![The level screen Fetch opens — not created from here](../walkthrough/output-develop/en/d04_geography/05_fetch_map_admin_levels.png)

**Upload from Excel starts by defining the hierarchy's levels**

![Upload from Excel starts by defining the hierarchy's levels](../walkthrough/output-develop/en/d04_geography/06_excel_define_hierarchy.png)

---

## Onboarding · 2b Geography — Preconfigured

**Use these boundaries** opens the Fetch search with the source **fixed** to the country's official set — here OCHA COD-AB — and suggestions limited to the country. The tag reads how far a second, independently drawn source (geoBoundaries) agrees, level by level: *High* when every level it has is confirmed, *Medium* when some only partly match or the other source is years older, *Low* when nothing could be cross-checked. Mozambique is **Medium**: provinces confirmed, districts and administrative posts partly match an older source, localities exist in one source only. *One source only* means a level could not be checked, not that it is wrong.

For Cidade de Maputo the set has four nested levels — 1 city, 7 districts, 7 administrative posts, 64 bairros (the districts and posts are the same seven places in Maputo city) — named here in the local terms *Cidade → Distrito Municipal → Posto Administrativo → Bairro*: 79 areas in all.

**Use these boundaries → the search, with the source fixed to Mozambique's official set: *Medium confidence*, OCHA COD-AB · Jan 2025, and the headline**

![Use these boundaries → the search, with the source fixed to Mozambique's official set: Medium confidence, OCHA COD-AB · Jan 2025, and the headline](../walkthrough/output-develop/en/d04b_preconfigured/01_preconfigured_search.png)

**Suggestions come only from Mozambique's official set**

![Suggestions come only from Mozambique's official set](../walkthrough/output-develop/en/d04b_preconfigured/02_preconfigured_suggestions.png)

**The level screen for Cidade de Maputo: summary, data check (every level fully nested), polygons**

![The level screen for Cidade de Maputo: summary, data check (every level fully nested), polygons](../walkthrough/output-develop/en/d04b_preconfigured/03_preconfigured_levels.png)

**Each level with its status against the second source — *Confirmed*, *Partly confirmed · n%*, *One source only***

![Each level with its status against the second source — Confirmed, Partly confirmed · n%, One source only](../walkthrough/output-develop/en/d04b_preconfigured/04_per_level_confidence.png)

**The four levels named in local terms**

![The four levels named in local terms](../walkthrough/output-develop/en/d04b_preconfigured/05_levels_named.png)

**Boundaries created — 79 areas in four levels, with the licence line**

![Boundaries created — 79 areas in four levels, with the licence line](../walkthrough/output-develop/en/d04b_preconfigured/06_boundaries_created.png)

**Back on Geography: the hierarchy, ready to save**

![Back on Geography: the hierarchy, ready to save](../walkthrough/output-develop/en/d04b_preconfigured/07_geography_with_hierarchy.png)

---

## Onboarding · 3 Departments

Departments and designations, typed in or uploaded; codes are derived from the names. Four municipal departments, and two designations — Grievance Redressal Officer and Field Officer — linked to all four.

**Departments: create manually or bulk upload**

![Departments: create manually or bulk upload](../walkthrough/output-develop/en/d05_departments/01_departments_landing.png)

**Bulk upload, with a template to download**

![Bulk upload, with a template to download](../walkthrough/output-develop/en/d05_departments/02_departments_upload.png)

**Add department — code derived from the name**

![Add department — code derived from the name](../walkthrough/output-develop/en/d05_departments/03_add_department.png)

**Add designation, linked to departments**

![Add designation, linked to departments](../walkthrough/output-develop/en/d05_departments/04_add_designation.png)

**Four departments, two designations**

![Four departments, two designations](../walkthrough/output-develop/en/d05_departments/05_departments_filled.png)

---

## Onboarding · 4 Employees

People added one at a time or from a staff list. Each gets a department, a designation, system roles and jurisdictions. Six here: one grievance officer (GRO) for each complaint department, so every complaint has someone to assign it, and two field officers (`PGR_LME`) for their districts.

**Employees: create manually or bulk upload**

![Employees: create manually or bulk upload](../walkthrough/output-develop/en/d06_employees/01_employees_landing.png)

**Bulk upload**

![Bulk upload](../walkthrough/output-develop/en/d06_employees/02_employees_upload.png)

**A field officer: Solid Waste and Sanitation, Field Officer, `EMPLOYEE` + `PGR_LME`, jurisdiction KaMpfumo**

![A field officer: Solid Waste and Sanitation, Field Officer, EMPLOYEE + PGR_LME, jurisdiction KaMpfumo](../walkthrough/output-develop/en/d06_employees/03_employee_form_filled.png)

**Six employees: a GRO for each department, two field officers**

![Six employees: a GRO for each department, two field officers](../walkthrough/output-develop/en/d06_employees/04_employees_list.png)

---

## Onboarding · 5 Complaints Template

Complaint categories, each handled by one department, with subcategories one per line and an optional resolution time of their own; the default for every category is set below the list (3 days here). Four categories, fourteen subcategories. **Finish setup** opens the management console — its first screen is the console home below.

**Complaints Template: start from scratch or bulk upload**

![Complaints Template: start from scratch or bulk upload](../walkthrough/output-develop/en/d07_complaints/01_complaints_landing.png)

**Bulk upload**

![Bulk upload](../walkthrough/output-develop/en/d07_complaints/02_complaints_upload.png)

**Add a complaint category: name, handling department, subcategories, resolution time**

![Add a complaint category: name, handling department, subcategories, resolution time](../walkthrough/output-develop/en/d07_complaints/03_add_category.png)

**Four categories, fourteen subcategories**

![Four categories, fourteen subcategories](../walkthrough/output-develop/en/d07_complaints/04_categories_added.png)

**The default resolution time — a target, not a legal SLA**

![The default resolution time — a target, not a legal SLA](../walkthrough/output-develop/en/d07_complaints/05_default_resolution_time.png)

---

## Account menu

The header's account menu: **Your account** (password, authenticator, email, signed-in sessions), **Members** (the people in the workspace, with invite and remove), and **Workspace settings** (the workspace name and how long invitations stay valid). Once onboarding is finished its steps aren't reachable again; these pages and the console are what an administrator comes back to.

**The account menu**

![The account menu](../walkthrough/output-develop/en/d08_account/01_account_menu.png)

**Your account — password, authenticator, email, signed-in sessions**

![Your account — password, authenticator, email, signed-in sessions](../walkthrough/output-develop/en/d08_account/02_your_account.png)

**Members — everyone in the workspace**

![Members — everyone in the workspace](../walkthrough/output-develop/en/d08_account/03_members.png)

**Workspace settings — name, invitation expiry**

![Workspace settings — name, invitation expiry](../walkthrough/output-develop/en/d08_account/04_workspace_settings.png)

---

## Management console

The console for the new workspace, route by route, as its founder sees it. Every screen pictured loaded without a refused or failed call. A few routes are not pictured; [What is not pictured](#what-is-not-pictured) says which and why.

**Console home: tenants, departments, designations, complaint categories, employees, boundaries, localization messages, access roles**

![Console home: tenants, departments, designations, complaint categories, employees, boundaries, localization messages, access roles](../walkthrough/output-develop/en/d09_manage/01_dashboard_home.png)

**Branding, editable after onboarding**

![Branding, editable after onboarding](../walkthrough/output-develop/en/d09_manage/03_branding.png)

**Tenants — the workspace's own tenant**

![Tenants — the workspace's own tenant](../walkthrough/output-develop/en/d09_manage/04_tenants.png)

**Departments**

![Departments](../walkthrough/output-develop/en/d09_manage/05_departments.png)

**Designations**

![Designations](../walkthrough/output-develop/en/d09_manage/06_designations.png)

**Boundaries — 80 (79 imported + the workspace root), on the map**

![Boundaries — 80 (79 imported + the workspace root), on the map](../walkthrough/output-develop/en/d09_manage/08_boundaries.png)

**Map Configuration**

![Map Configuration](../walkthrough/output-develop/en/d09_manage/09_map_configuration.png)

**Complaints — status tabs; none filed yet**

![Complaints — status tabs; none filed yet](../walkthrough/output-develop/en/d09_manage/10_complaints.png)

**Complaint Categories — the 4 categories and their subcategories, by department**

![Complaint Categories — the 4 categories and their subcategories, by department](../walkthrough/output-develop/en/d09_manage/11_complaint_types.png)

**Complaint Hierarchies — category → subcategory**

![Complaint Hierarchies — category → subcategory](../walkthrough/output-develop/en/d09_manage/12_complaint_hierarchies.png)

**PGR Escalation Policy — levels, ladder, automatic scan every 5 minutes**

![PGR Escalation Policy — levels, ladder, automatic scan every 5 minutes](../walkthrough/output-develop/en/d09_manage/13_escalation_policy.png)

**Employees — all seven, founder included**

![Employees — all seven, founder included](../walkthrough/output-develop/en/d09_manage/15_employees.png)

**Org Chart — seven employees; no reporting lines set yet**

![Org Chart — seven employees; no reporting lines set yet](../walkthrough/output-develop/en/d09_manage/16_org_chart.png)

**Users — citizen accounts; none yet**

![Users — citizen accounts; none yet](../walkthrough/output-develop/en/d09_manage/17_users.png)

**Access Roles — 27**

![Access Roles — 27](../walkthrough/output-develop/en/d09_manage/18_access_roles.png)

**Workflow Processes — none until a complaint is filed**

![Workflow Processes — none until a complaint is filed](../walkthrough/output-develop/en/d09_manage/20_processes.png)

**MDMS Schemas**

![MDMS Schemas](../walkthrough/output-develop/en/d09_manage/21_mdms_schemas.png)

**Analytics Providers — nothing is sent until a destination is switched on**

![Analytics Providers — nothing is sent until a destination is switched on](../walkthrough/output-develop/en/d09_manage/22_analytics_providers.png)

**Notification Event Catalogue (read-only; events come from the modules)**

![Notification Event Catalogue (read-only; events come from the modules)](../walkthrough/output-develop/en/d09_manage/25_notification_event_catalogue.png)

**Notification Routing**

![Notification Routing](../walkthrough/output-develop/en/d09_manage/26_notification_routing.png)

**Notification Templates**

![Notification Templates](../walkthrough/output-develop/en/d09_manage/27_notification_templates.png)

**Provider Templates**

![Provider Templates](../walkthrough/output-develop/en/d09_manage/28_notification_provider_templates.png)

**Advanced — every MDMS master**

![Advanced — every MDMS master](../walkthrough/output-develop/en/d09_manage/32_advanced_all_masters.png)

---

## API calls per console screen

Every console screen pictured above, with the API calls it made while loading and how many were refused or failed.

| Screen | API calls | Refused (401/403) | Failed (5xx) |
| --- | ---: | ---: | ---: |
| Console home | 35 | 0 | 0 |
| Branding, editable after onboarding | 13 | 0 | 0 |
| Tenants | 12 | 0 | 0 |
| Departments | 12 | 0 | 0 |
| Designations | 12 | 0 | 0 |
| Boundaries | 16 | 0 | 0 |
| Map Configuration | 13 | 0 | 0 |
| Complaints | 14 | 0 | 0 |
| Complaint Categories | 14 | 0 | 0 |
| Complaint Hierarchies | 12 | 0 | 0 |
| PGR Escalation Policy | 13 | 0 | 0 |
| Employees | 19 | 0 | 0 |
| Org Chart | 13 | 0 | 0 |
| Users | 11 | 0 | 0 |
| Access Roles | 12 | 0 | 0 |
| Workflow Processes | 11 | 0 | 0 |
| MDMS Schemas | 11 | 0 | 0 |
| Analytics Providers | 12 | 0 | 0 |
| Notification Event Catalogue (read-only; events come from the modules) | 12 | 0 | 0 |
| Notification Routing | 12 | 0 | 0 |
| Notification Templates | 12 | 0 | 0 |
| Provider Templates | 12 | 0 | 0 |
| Advanced | 10 | 0 | 0 |

---

## What changed since the 2026-10-05 capture

The earlier walkthrough of the develop UI was captured on a remote develop deployment on
2026-10-05. Since then:

* **The onboarding Home and welcome tour** are new: sign-up lands on Home, not on Branding, with
  a six-slide tour, the next step, *Learn the basics* videos and a documentation panel on every
  step.
* **Preconfigured boundaries** is live in Geography: the country's official boundary set with a
  High / Medium / Low confidence tag, searched like Fetch with the source fixed.
* **The founder's console permissions are fixed** in the sign-up seed. Every console screen
  pictured here loaded without a refused call (in the earlier capture most of the console read
  *AccessDeniedException*).
* **Complaint categories** can each have their own resolution time, with a default for the rest.
* **The account menu** has *Your account*, *Members* and *Workspace settings*; the console has
  **Branding** and **Escalation Policy**; and once onboarding is finished its steps redirect to
  the console instead of offering *Switch to Onboarding*.
* Sign-up and onboarding ran end to end without an error: no provisioning race, no refused
  finish, no expired session.

## What is not pictured

These console routes were captured but are left out, because each shows something that isn't a
fair picture of the product:

* **Boundary hierarchies** — its Levels column header is the raw translation key `app.fields.levels`
* **Workflows** — it lists 0 business services although the PGR workflow exists for the tenant
* **Public Dashboard — anonymous access, off until published** — its preview shows grey placeholder tiles until complaints are filed
* **Localization — English and Portuguese columns** — most Portuguese messages read “— missing —”, and inherited platform messages include India-specific ones (Aadhaar)
* **Notification configure** — notifications are not deployed on this local stack
* **Notification channels** — notifications are not deployed on this local stack
* **Notification providers** — notifications are not deployed on this local stack
* **Notification logs** — notifications are not deployed on this local stack
* **Notification preferences** — notifications are not deployed on this local stack

Boundary Hierarchies, Workflow Business Services and the Localization gaps are still on `develop`;
the Public Dashboard preview fills in once complaints exist. The notification screens only fail
because this local stack is deployed without notifications (Novu); on a deployment with them they
load.

---

## How this capture was made

Against the **local** DIGIT stack, deployed from `develop` at `f713f9e6c` on 2026-10-21 with
`local-setup/ansible/deploy.sh maputo` (images `develop-f713f9e6`; the configurator built from the
same commit). Nothing was written to any shared server.

* **The sign-up and the five onboarding steps write.** They were driven once, click by click,
  against a new throwaway workspace — the steps unlock one after another, so stopping before each
  save would show only Branding. Their screenshots are imported by
  [`walkthrough/import_develop_run.py`](../walkthrough/import_develop_run.py).
* **Everything else is read-only.** [`walkthrough/capture_develop.py`](../walkthrough/capture_develop.py)
  captures the sign-in screens, the account pages and every console route behind the request
  guard (it ended with `read-only guard: no mutating requests were attempted`), recording the API
  calls each console screen made.

```bash
cd walkthrough
WT_HOST=http://localhost WT_OUT=output-develop \
WT_KC_EMAIL=… WT_STORAGE_STATE=/path/to/signed-in-state.json .venv/bin/python capture_develop.py
.venv/bin/python import_develop_run.py /path/to/run/shots
WT_OUT=output-develop .venv/bin/python build_site_develop.py
.venv/bin/python build_doc_develop.py
```

The interactive sitemap and grid gallery are in
[`walkthrough/output-develop/`](../walkthrough/output-develop) — `index.html` and `gallery.html`.
