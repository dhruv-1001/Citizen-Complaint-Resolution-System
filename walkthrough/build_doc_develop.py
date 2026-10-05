#!/usr/bin/env python3
"""Render docs/digit-ui-walkthrough-develop.md from output-develop/.

The develop-deployment capture covers the develop-branch UI: Keycloak sign-in, the
self-serve sign-up, the five-step onboarding (done for real, for Cidade de
Maputo), and the management console as the new workspace's founder sees it.

    .venv/bin/python build_doc_develop.py
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output-develop" / "en"
DOC = HERE.parent / "docs" / "digit-ui-walkthrough-develop.md"
REL = "../walkthrough/output-develop/en"

CAPTURED = "2026-10-05"
HOST = "https://141.94.92.163.nip.io"

SECTIONS = [
    ("d01_signin", "Sign in · Keycloak",
     "`/configurator/` no longer has its own form. **Log in** hands off to Keycloak (realm "
     "`digit`, served by the same host under `/auth/`), which is username-first: email, then "
     "password, or GitHub. You pick a workspace after signing in. Accounts without a password — "
     "anyone who came in through a sign-up link — use **Set up or reset your password**. "
     "The `ADMIN / eGov@123` DIGIT account is not a Keycloak user, so it cannot sign in here."),

    ("d02_signup", "Sign up · a new workspace",
     "**Create an account** is self-serve: name and email, then a one-use sign-in link by mail. "
     "On this deployment mail lands in Mailpit (`/mailpit/`, basic auth). Then three steps — "
     "**Account** (name and a derived code), **Preferences** (country, languages, time zone, "
     "financial year, URL slug, the founder's mobile), **Review** — and a provisioning run that "
     "creates the tenant, the organisation, the founder's DIGIT login and their roles.\n\n"
     "The account below is the throwaway workspace this walkthrough onboarded: **Cidade de "
     "Maputo**, code `MZ-CDM`, tenant `cidadedemaputo`, Mozambique, English + Portuguese, "
     "`Africa/Maputo`, January–December. Provisioning failed once on a timing race and the backend "
     "finished it on retry — see [finding 3](#3-sign-up-provisioning-can-fail-on-a-read-after-write-race)."),

    ("d03_branding", "Onboarding · 1 Branding",
     "Logo, organisation name (read-only here; it lives in Workspace settings) and one of three "
     "brand themes. The logo is a generated *CM* monogram, not the municipality's crest. "
     "**Save and continue** unlocks Geography."),

    ("d04_geography", "Onboarding · 2 Geography",
     "Three sources: *Preconfigured* (coming soon), **Fetch boundaries**, and **Upload from "
     "Excel**. Fetch boundaries searches turbopass, which is now deployed on this box itself, "
     "with the same official boundary DB as naipepea.\n\n"
     "The source is **OCHA COD-AB** — the best set for Mozambique in the #1994 evaluation "
     "(COD *enhanced*, 2025). For Mozambique the default *Official* source resolves to the same "
     "set; it is picked explicitly here so the screenshots name it. COD-AB gives Cidade de Maputo "
     "four nested levels with no gaps: 1 province-level city → 7 districts → 7 administrative "
     "posts → 64 bairros, 79 areas. In Maputo city the districts and the administrative posts are "
     "the same seven places, and the level picker only accepts a contiguous range, so dropping the "
     "duplicate would also drop either the city or the bairros. All four are kept, named "
     "*Cidade → Distrito Municipal → Posto Administrativo → Bairro*.\n\n"
     "For comparison, OpenStreetMap (bomet's Overpass path) returns three levels for the same "
     "city — 1 / 6 / 63 — and misses the KaNyaka district."),

    ("d05_departments", "Onboarding · 3 Departments",
     "Departments and designations, typed in or uploaded. A new workspace starts with "
     "`ONBOARDING_ADMIN` / Administration and the founder's `ONBOARDING_FOUNDER` designation. "
     "Added: Solid Waste and Sanitation, Roads and Drainage, Markets and Fairs, Parks and Public "
     "Spaces; designations Grievance Redressal Officer and Field Officer, linked to all four. "
     "Codes are derived from the names."),

    ("d06_employees", "Onboarding · 4 Employees",
     "Add people one at a time or upload a staff list. Each employee gets departments (the first "
     "is their main one), a designation, system roles and jurisdictions; they are created in HRMS "
     "and invited to the identity service. Seven in the end: the founder, one GRO per complaint "
     "department, and two field officers (`PGR_LME`). Two things went wrong on the way — "
     "[finding 5](#5-email-optional-is-required) and "
     "[finding 6](#6-an-expired-identity-session-breaks-writes-without-saying-so)."),

    ("d07_complaints", "Onboarding · 5 Complaints Template",
     "Complaint categories, each handled by one department, with subcategories one per line, "
     "and one resolution target for all of them. Four categories, fourteen subcategories, 3 days. "
     "**Finish setup** was refused the first time — "
     "[finding 4](#4-finish-setup-needs-one-gro-per-department-and-does-not-say-so) — and went "
     "through once every complaint department had its own GRO."),

    ("d08_onboarding_done", "Onboarding · finished",
     "Each step revisited after **Finish setup**, read-only: the state an administrator comes back "
     "to."),

    ("d09_manage", "Management console · as the new founder",
     "Every route of the develop console, opened by the account that just created the workspace. "
     "The table under [finding 1](#1-the-new-workspaces-founder-is-denied-most-of-the-console) "
     "counts the API calls each screen made and how many were refused."),

    ("d10_apps", "Employee & citizen apps",
     "The other surfaces, signed out. The tenant-scoped employee app renders blank — "
     "[finding 2](#2-the-employee-app-does-not-load) — and the public dashboard URL is not served."),
]

SHOTS = {
    "configurator_landing": "`/configurator/` — one button, **Log in**; the form lives in Keycloak",
    "keycloak_email_step": "Keycloak, step one: email (or GitHub)",
    "keycloak_password_step": "Step two: password",
    "password_setup_link_form": "**Set up or reset your password** — a one-use link by mail",
    "signup_blank": "**Create an account**: name and email",

    "signup_filled": "Filled in",
    "signup_check_email": "Check your email",
    "mailpit_signin_link_email": "The sign-in link, caught by Mailpit",
    "account_email_verified": "Back from the link: email verified, now name the account",
    "account_name_and_code": "*Cidade de Maputo* — the code `CDM` is derived from the name",
    "preferences_blank": "Preferences",
    "preferences_mozambique_defaults": "Picking Mozambique pre-fills `Africa/Maputo` and the slug `cidade-de-maputo`, but not Portuguese",
    "preferences_filled": "Portuguese added, financial year January–December, founder's mobile",
    "review": "Review — the code is now `MZ-CDM`",
    "provisioning": "Provisioning",
    "provisioning_failed_mdms_schema_not_visible": "*Setup did not finish — MDMS_SCHEMA_NOT_VISIBLE*",
    "choose_workspace_after_retry": "Reloaded a minute later: the backend's own retry finished it, and the workspace is there to choose",

    "branding_blank": "Branding, 0 of 5 done, every later step locked",
    "branding_logo_uploaded": "Logo uploaded",
    "branding_green_and_gold": "Green and Gold theme selected",

    "geography_choose_source": "Geography: Preconfigured (coming soon), Fetch boundaries, Upload from Excel",
    "fetch_boundaries": "Fetch boundaries — source picker, area search, optional map provider",
    "boundary_source_options": "Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture",
    "cod_suggestions": "COD-AB suggestion: *Cidade de Maputo — Province, Moçambique · L1 · 78 sub-areas*",
    "cod_map_admin_levels": "Map Admin Levels — licence line, a data check (79 areas, every level fully nested), and the polygons on the map",
    "levels_named": "All four levels named; **Create Hierarchy & Boundaries** writes",
    "boundaries_created": "79 boundaries created — the message says *from OSM data* though the source was COD-AB",
    "geography_with_hierarchy": "Back on Geography: one hierarchy, *1 cidade · 7 distrito municipals · 7 posto administrativos · 64 bairros* (English plurals on Portuguese names)",

    "departments_seeded": "Departments as a new workspace starts",
    "departments_upload": "Upload a departments file, with a template to download",
    "add_department": "Add department — code derived from the name",
    "add_designation": "Add designation, linked to departments",
    "departments_filled": "Five departments, three designations",

    "employees_landing": "Employees: create manually or bulk upload",
    "employees_upload": "Bulk upload",
    "employee_form_blank": "Add an employee — note *Email (optional)*, and that **System roles** lists every role, `SUPERUSER` and `INTERNAL_MICROSERVICE_ROLE` included",
    "employee_form_filled": "A field officer: Roads and Drainage, `EMPLOYEE` + `PGR_LME`, jurisdiction Nhlamankulo",
    "employees_list": "Three employees plus the founder — whose roles include `SUPERUSER` and `INTERNAL_MICROSERVICE_ROLE`",
    "invite_failed_identity_session_expired": "An hour in: *Employee CMM-GRO-004 exists in HRMS; invitation is unfinished … An identity session is required*",
    "password_setup_link_sent": "Getting a session back meant setting a password first — the account only ever had the sign-up link",
    "keycloak_set_password": "Keycloak's set-password form",
    "employees_one_gro_per_department": "Signed in again; the invite retried with the same code and email. One GRO per complaint department",

    "complaints_landing": "Complaints Template: start from scratch or bulk upload",
    "complaints_upload": "Bulk upload",
    "add_category": "Add a complaint category: name, handling department, subcategories one per line",
    "four_categories_sla_3_days": "Four categories, fourteen subcategories, 3-day target",
    "finish_refused_workspace_probe_incomplete": "**Finish setup** refused: *Could not complete setup step — WORKSPACE_PROBE_INCOMPLETE*",
    "finished_lands_in_management_access_denied": "Finished — and the console it lands in opens on *AccessDeniedException*",

    "branding_done": "Branding, done",
    "geography_done": "Geography, done",
    "departments_done": "Departments, done",
    "employees_done": "Employees, done",
    "complaints_template_done": "Complaints Template, done",

    "dashboard_home": "Console home — Tenants, Departments, Designations, Complaint Categories and Complaints stay at `…` (their counts are refused); Users reads 0",
    "public_dashboard": "Public Dashboard",
    "tenants": "Tenants — *AccessDeniedException*",
    "departments": "Departments — *AccessDeniedException*, though the founder just created them",
    "designations": "Designations — *AccessDeniedException*",
    "boundary_hierarchies": "Boundary Hierarchies — `ADMIN` (the four COD levels) and the baseline `WORKSPACE`",
    "boundaries": "Boundaries — 80 (79 imported + the workspace root), 79 with map geometry",
    "map_configuration": "Map Configuration",
    "complaints": "Complaints — status tabs, no complaints yet",
    "complaint_types": "Complaint Categories — *AccessDeniedException*",
    "complaint_hierarchies": "Complaint Hierarchies — *AccessDeniedException*",
    "localization": "Localization — 3,490 messages, English and Portuguese columns",
    "employees": "Employees — all seven",
    "org_chart": "Org Chart — stuck on *Loading tenants…*",
    "users": "Users",
    "access_roles": "Access Roles — 27",
    "workflows": "Workflow Business Services — *0*, although the workflow API returns the PGR business service for this tenant",
    "processes": "Workflow Processes",
    "mdms_schemas": "MDMS Schemas",
    "analytics_providers": "Analytics Providers",
    "notification_configure": "Configure Notifications — *No events declared*",
    "notification_channels": "Notification Channels",
    "notification_event_catalogue": "Event Catalogue",
    "notification_routing": "Notification Routing",
    "notification_templates": "Notification Templates",
    "notification_provider_templates": "Provider Templates",
    "notification_providers": "Notification Providers — the request is refused",
    "notification_logs": "Notification Logs",
    "notification_preferences": "Notification Preferences",
    "advanced_all_masters": "Advanced — every MDMS master",

    "employee_ui_tenant_slug": "`/kd/digit-ui/employee` — blank: its scripts are requested from `/digit-ui/…`, which the vhost answers with 404",
    "employee_ui_bare_path": "`/digit-ui/employee` — 404 by design on this vhost",
    "citizen_signin": "`/citizen` — the digit-ui-v2 citizen sign-in (mobile + OTP; not sent)",
    "public_dashboard_url": "`/digit-ui/public-dashboard` — 404",
}

FINDINGS = """
## What the capture found on the develop deployment

### 1. The new workspace's founder is denied most of the console

Onboarding goes through `pgr-services`' own onboarding API, so it works end to end. The console it
lands in calls DIGIT directly — and Kong refuses a large share of those calls for the founder, with
`AccessDeniedException`, even though the request carries `SUPERUSER` and `MDMS_ADMIN`:

```
POST /mdms-v2/v2/_count   tenantId=cidadedemaputo
  userInfo.roles: EMPLOYEE, LOC_ADMIN, SUPERUSER, MDMS_ADMIN, HRMS_ADMIN, WORKFLOW_ADMIN,
                  ACCOUNT_ADMIN, INTERNAL_MICROSERVICE_ROLE   (all @ cidadedemaputo)
  → 403 AccessDeniedException
```

The same read as `ADMIN@kd` succeeds (`totalCount: 5` departments), so the data is there and the
endpoint is allowed in general. What differs is the tenant the roles are scoped to: the founder's are
all `@cidadedemaputo`, a new **root** tenant. The likely cause — not confirmed here, because this
capture did not read the access-control tables — is that Kong's RBAC has few or no role → action
grants under that root: the same gap the maputo deployment showed, where fresh tenants got only a
fraction of the role-actions.

Per screen, the API calls each route made and how many were refused ({ROUTES} routes):

{STATUS_TABLE}

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
`/<slug>/digit-ui/citizen`. The digit-ui-v2 citizen app at `/citizen` is unaffected.

### 3. Sign-up provisioning can fail on a read-after-write race

The first **Create account** ended in *Setup did not finish — MDMS_SCHEMA_NOT_VISIBLE*. Provisioning
creates the tenant's MDMS schemas and immediately searches for each one; MDMS creates schemas
asynchronously (`schema/v1/_create` → 202), so the search right after came back empty and
`OnboardingSteps.ensureSchema` gave up. Five seconds later the same search returned the schema.
The error is marked retryable and the backend finished on its own — reloading the page a minute
later showed the workspace — but the screen in between tells the person their setup failed.

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

### 9. What was changed on the server for this capture

Authorised for this walkthrough, and kept in place:

* **turbopass** — `turbopass-search:local` built from `turbopass/` at `b015ade7`, running on
  `127.0.0.1:13301`, reading the official boundary DB copied from naipepea
  (`/opt/turbopass/overture-data/boundaries.sqlite`, 12 countries, checksum-verified); and a
  `location /turbopass/` block in the vhost (backup taken first). The host's Ansible inventory does
  not set `enable_turbopass`, so a redeploy from it would remove both.
* **The Cidade de Maputo workspace** — tenant `cidadedemaputo`, 79 boundaries, 5 departments,
  3 designations, 7 employees, 4 categories / 14 subcategories at 72 h, owned by the throwaway
  account `walkthrough.maputo@example.com` (mail in Mailpit). No other tenant was touched.

Separately, and not changed: this host publishes several container ports straight to the internet,
including Postgres (`15432`) and Redis (`16379`).
"""

METHOD = """
## How this capture was made

Two kinds of screen are in this document, and they were made differently.

* **The sign-up and the five onboarding steps write.** They were driven once, click by click, on
  {CAPTURED}, against a new throwaway workspace — that was the point: the steps unlock one after
  another, so stopping before each save would have shown only Branding. Their screenshots are
  imported by [`walkthrough/import_develop_run.py`](../walkthrough/import_develop_run.py).
* **Everything else is read-only.** [`walkthrough/capture_develop.py`](../walkthrough/capture_develop.py)
  revisits the finished steps, the console and the apps behind the same request guard as the bomet
  capture; it ended with `read-only guard: no mutating requests were attempted`.

```bash
cd walkthrough
WT_HOST={HOST} WT_OUT=output-develop \\
WT_KC_EMAIL=… WT_KC_PASS=… .venv/bin/python capture_develop.py
.venv/bin/python import_develop_run.py /path/to/run/shots     # the onboarding run's screenshots
WT_OUT=output-develop .venv/bin/python build_site_develop.py
.venv/bin/python build_doc_develop.py
```

The interactive sitemap and grid gallery for this capture are in
[`walkthrough/output-develop/`](../walkthrough/output-develop) — `index.html` and `gallery.html`.
"""


def slug(heading: str) -> str:
    s = heading.lower()
    s = re.sub(r"[^a-z0-9 _-]", "", s)
    return s.replace(" ", "-")


def label_of(png: Path) -> str:
    return re.sub(r"^\d+_", "", png.stem)


def flow_shots(flow: str) -> list[Path]:
    d = OUT / flow
    return sorted(d.glob("*.png")) if d.exists() else []


def status_table() -> tuple[str, int]:
    f = OUT / "d09_manage" / "_api_status.json"
    if not f.exists():
        return "_(no API status recorded)_", 0
    data = json.loads(f.read_text())
    rows = ["| Screen | API calls | Refused (401/403) |", "| --- | ---: | ---: |"]
    for label, v in data.items():
        cap = SHOTS.get(label, label).split(" — ")[0]
        mark = " **all-or-most**" if v["requests"] and v["denied"] * 2 >= v["requests"] else ""
        rows.append(f"| {cap} | {v['requests']} | {v['denied']}{mark} |")
    return "\n".join(rows), len(data)


def main() -> int:
    total = sum(len(flow_shots(f)) for f, _, _ in SECTIONS)
    parts = [f"""# DIGIT develop UI — visual walkthrough

A screen-by-screen capture of **[141.94.92.163.nip.io]({HOST}/configurator/)** — the develop-branch
DIGIT configurator: Keycloak sign-in, self-serve sign-up, the five-step onboarding carried out for
**Cidade de Maputo** with OCHA COD-AB boundaries, and the management console as the new workspace's
founder sees it; plus the employee and citizen apps.

**{total} screens · {len(SECTIONS)} flows · captured {CAPTURED}.** Unlike the bomet walkthrough this one
**writes**: the sign-up and the onboarding steps created a throwaway workspace (authorised for this
capture; see [What was changed on the server](#9-what-was-changed-on-the-server-for-this-capture)).
Everything else was captured read-only.

The `master`-branch UI on bomet — the 4-phase wizard, the employee app's new shell, the citizen apps —
is in [`digit-ui-walkthrough.md`](digit-ui-walkthrough.md).

---

## Contents
"""]
    toc = [f"- [{h}](#{slug(h)})" for _, h, _ in SECTIONS]
    toc += [f"- [{h}](#{slug(h)})" for h in ("What the capture found on the develop deployment",
                                              "How this capture was made")]
    parts.append("\n".join(toc) + "\n\n---\n")

    missing_caps = []
    for flow, heading, intro in SECTIONS:
        shots = flow_shots(flow)
        if not shots:
            print(f"!! no screenshots for {flow}")
            continue
        parts.append(f"## {heading}\n\n{intro}\n")
        for png in shots:
            label = label_of(png)
            cap = SHOTS.get(label)
            if cap is None:
                missing_caps.append(f"{flow}/{png.name}")
                cap = label.replace("_", " ")
            alt = re.sub(r"[*`\[\]]", "", cap)
            parts.append(f"**{cap.replace('**', '*')}**\n\n![{alt}]({REL}/{flow}/{png.name})\n")
        parts.append("---\n")

    table, n = status_table()
    parts.append(FINDINGS.strip().replace("{STATUS_TABLE}", table).replace("{ROUTES}", str(n)) + "\n")
    parts.append("---\n")
    parts.append(METHOD.strip().replace("{CAPTURED}", CAPTURED).replace("{HOST}", HOST) + "\n")
    DOC.write_text("\n".join(parts))
    print(f"{DOC}: {total} images, {len(SECTIONS)} flows")
    if missing_caps:
        print(f"  [no caption] {missing_caps}")

    text = DOC.read_text()
    broken = [m for m in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
              if not (DOC.parent / m).resolve().exists()]
    heads = {slug(h.lstrip("#").strip()) for h in text.splitlines() if h.startswith("##")}
    anchors = [a for a in re.findall(r"\]\(#([^)]+)\)", text) if a not in heads]
    print(f"broken images: {len(broken)}{' ' + str(broken[:3]) if broken else ''}")
    print(f"broken anchors: {len(anchors)}{' ' + str(anchors) if anchors else ''}")
    return 1 if (broken or anchors or missing_caps) else 0


if __name__ == "__main__":
    sys.exit(main())
