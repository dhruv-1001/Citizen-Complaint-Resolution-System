#!/usr/bin/env python3
"""Render docs/digit-ui-walkthrough-develop.md from output-develop/.

The develop capture covers the configurator as it is on the `develop` branch:
Keycloak sign-in, the self-serve sign-up, the onboarding Home and welcome tour,
the five onboarding steps (done for real, for Cidade de Maputo), the account
pages, and the management console as the new workspace's founder sees it.

    .venv/bin/python build_doc_develop.py
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output-develop" / "en"
DOC = HERE.parent / "docs" / "digit-ui-walkthrough-develop.md"
REL = "../walkthrough/output-develop/en"

CAPTURED = "2026-10-21"
COMMIT = "f713f9e6c"

# Console screens captured but not pictured, and why (see "What is not pictured").
NOT_PICTURED = {
    "boundary_hierarchies": "its Levels column header is the raw translation key `app.fields.levels`",
    "workflows": "it lists 0 business services although the PGR workflow exists for the tenant",
    "public_dashboard": "its preview shows grey placeholder tiles until complaints are filed",
    "localization": "most Portuguese messages read “— missing —”, and inherited platform messages include India-specific ones (Aadhaar)",
    "notification_configure": "notifications are not deployed on this local stack",
    "notification_channels": "notifications are not deployed on this local stack",
    "notification_providers": "notifications are not deployed on this local stack",
    "notification_logs": "notifications are not deployed on this local stack",
    "notification_preferences": "notifications are not deployed on this local stack",
}

SECTIONS = [
    ("d01_signin", "Sign in · Keycloak",
     "`/configurator/` has no form of its own. **Log in** hands off to Keycloak, which asks for the "
     "email first, then the password; you choose a workspace after signing in. Accounts that came "
     "in through a sign-up link have no password until they use **Set up or reset your password**."),

    ("d02_signup", "Sign up · a new workspace",
     "**Create an account** is self-serve: name and email, then a one-use sign-in link by mail "
     "(on this stack the mail lands in Mailpit). Then three steps — **Account** (name and a code "
     "derived from it), **Preferences** (country, languages, time zone, financial year, URL slug, "
     "the founder's mobile), **Review** — and the provisioning screen while the workspace, its "
     "basics, the founder's employee record, account, membership and sign-in are created.\n\n"
     "The workspace onboarded in this walkthrough is a throwaway: **Cidade de Maputo**, Mozambique, "
     "English + Portuguese, `Africa/Maputo`, January–December."),

    ("d02b_home", "Onboarding · Home and welcome tour",
     "Provisioning lands on the onboarding **Home**. A six-slide tour explains what onboarding is "
     "and what each step is for; it can be reopened with **Take a tour**. Home shows the next step "
     "to do, short **Learn the basics** videos, and a **Documentation** panel that every step "
     "carries on its right-hand side."),

    ("d03_branding", "Onboarding · 1 Branding",
     "Logo, account name (changed in Workspace settings) and one of three brand themes. The logo "
     "is a generated *CM* monogram, not the municipality's crest. **Save and continue** unlocks "
     "Geography."),

    ("d04_geography", "Onboarding · 2 Geography",
     "Three sources. **Preconfigured boundaries** already knows the country — Mozambique, from "
     "sign-up — and offers its official boundary set with a confidence tag and the source line. "
     "**Fetch boundaries** searches the boundary service with a choice of source. **Upload from "
     "Excel** starts by defining the hierarchy's levels.\n\n"
     "The Fetch and Excel screens below are read-only: nothing was created from them. The "
     "boundaries were brought in through Preconfigured, in the next section."),

    ("d04b_preconfigured", "Onboarding · 2b Geography — Preconfigured",
     "**Use these boundaries** opens the Fetch search with the source **fixed** to the country's "
     "official set — here OCHA COD-AB — and suggestions limited to the country. The tag reads how "
     "far a second, independently drawn source (geoBoundaries) agrees, level by level: *High* when "
     "every level it has is confirmed, *Medium* when some only partly match or the other source is "
     "years older, *Low* when nothing could be cross-checked. Mozambique is **Medium**: provinces "
     "confirmed, districts and administrative posts partly match an older source, localities exist "
     "in one source only. *One source only* means a level could not be checked, not that it is "
     "wrong.\n\n"
     "For Cidade de Maputo the set has four nested levels — 1 city, 7 districts, 7 administrative "
     "posts, 64 bairros (the districts and posts are the same seven places in Maputo city) — "
     "named here in the local terms *Cidade → Distrito Municipal → Posto Administrativo → Bairro*: "
     "79 areas in all."),

    ("d05_departments", "Onboarding · 3 Departments",
     "Departments and designations, typed in or uploaded; codes are derived from the names. Four "
     "municipal departments, and two designations — Grievance Redressal Officer and Field Officer "
     "— linked to all four."),

    ("d06_employees", "Onboarding · 4 Employees",
     "People added one at a time or from a staff list. Each gets a department, a designation, "
     "system roles and jurisdictions. Six here: one grievance officer (GRO) for each complaint "
     "department, so every complaint has someone to assign it, and two field officers "
     "(`PGR_LME`) for their districts."),

    ("d07_complaints", "Onboarding · 5 Complaints Template",
     "Complaint categories, each handled by one department, with subcategories one per line and "
     "an optional resolution time of their own; the default for every category is set below the "
     "list (3 days here). Four categories, fourteen subcategories. **Finish setup** opens the "
     "management console — its first screen is the console home below."),

    ("d08_account", "Account menu",
     "The header's account menu: **Your account** (password, authenticator, email, signed-in "
     "sessions), **Members** (the people in the workspace, with invite and remove), and "
     "**Workspace settings** (the workspace name and how long invitations stay valid). Once "
     "onboarding is finished its steps aren't reachable again; these pages and the console are "
     "what an administrator comes back to."),

    ("d09_manage", "Management console",
     "The console for the new workspace, route by route, as its founder sees it. Every screen "
     "pictured loaded without a refused or failed call. A few routes are not pictured; "
     "[What is not pictured](#what-is-not-pictured) says which and why."),
]

SHOTS = {
    "configurator_landing": "`/configurator/` — one button, **Log in**; the form lives in Keycloak",
    "keycloak_email_step": "Keycloak, step one: email (or GitHub)",
    "keycloak_password_step": "Step two: password",
    "password_setup_link_form": "**Set up or reset your password** — a one-use link by mail",
    "signup_blank": "**Create an account**: name and email",

    "signup_filled": "Filled in",
    "signup_check_email": "Check your email",
    "mailpit_signin_link_email": "The sign-in link, as it arrives (Mailpit on this stack)",
    "account_email_verified": "Back from the link: email verified, now name the account",
    "account_name_and_code": "*Cidade de Maputo* — the code is derived from the name and checked as you type",
    "preferences_blank": "Preferences",
    "preferences_mozambique_defaults": "Picking Mozambique fills in the time zone and the URL slug",
    "preferences_filled": "Portuguese added, financial year January–December, founder's mobile",
    "review": "Review",
    "provisioning": "Setting up Cidade de Maputo",

    "tour_1_what_onboarding_is": "Welcome tour 1 of 6 — what onboarding is for",
    "tour_2_complaints_template": "2 — Complaints Template: what citizens can report, and who handles it",
    "tour_3_branding": "3 — Branding",
    "tour_4_geography": "4 — Geography",
    "tour_5_departments_employees": "5 — Departments and Employees",
    "tour_6_reopen": "6 — reopen the tour any time; every step has documentation",
    "onboarding_home": "Onboarding Home: the next step, **Learn the basics** videos, documentation",

    "branding_blank": "Branding, with every later step still locked",
    "branding_logo_uploaded": "Logo uploaded",
    "branding_green_and_gold": "Green and Gold theme selected",

    "geography_choose_source": "Geography: **Preconfigured boundaries** (Mozambique, Medium confidence, OCHA COD-AB · Jan 2025), Fetch boundaries, Upload from Excel",
    "fetch_boundaries": "Fetch boundaries — source, area search, optional map provider",
    "boundary_source_options": "Sources: Official (best per country), OCHA COD-AB, geoBoundaries, Overture",
    "fetch_suggestions": "Typing a place: suggestions with level and number of areas inside",
    "fetch_map_admin_levels": "The level screen Fetch opens — not created from here",
    "excel_define_hierarchy": "Upload from Excel starts by defining the hierarchy's levels",

    "preconfigured_search": "Use these boundaries → the search, with the source fixed to Mozambique's official set: *Medium confidence*, OCHA COD-AB · Jan 2025, and the headline",
    "preconfigured_suggestions": "Suggestions come only from Mozambique's official set",
    "preconfigured_levels": "The level screen for Cidade de Maputo: summary, data check (every level fully nested), polygons",
    "per_level_confidence": "Each level with its status against the second source — *Confirmed*, *Partly confirmed · n%*, *One source only*",
    "levels_named": "The four levels named in local terms",
    "boundaries_created": "Boundaries created — 79 areas in four levels, with the licence line",
    "geography_with_hierarchy": "Back on Geography: the hierarchy, ready to save",

    "departments_landing": "Departments: create manually or bulk upload",
    "departments_upload": "Bulk upload, with a template to download",
    "add_department": "Add department — code derived from the name",
    "add_designation": "Add designation, linked to departments",
    "departments_filled": "Four departments, two designations",

    "employees_landing": "Employees: create manually or bulk upload",
    "employees_upload": "Bulk upload",
    "employee_form_blank": "Add an employee",
    "employee_form_filled": "A field officer: Solid Waste and Sanitation, Field Officer, `EMPLOYEE` + `PGR_LME`, jurisdiction KaMpfumo",
    "employees_list": "Six employees: a GRO for each department, two field officers",

    "complaints_landing": "Complaints Template: start from scratch or bulk upload",
    "complaints_upload": "Bulk upload",
    "add_category": "Add a complaint category: name, handling department, subcategories, resolution time",
    "categories_added": "Four categories, fourteen subcategories",
    "default_resolution_time": "The default resolution time — a target, not a legal SLA",
    "finished_lands_in_management": "**Finish setup** — the management console, every count filled in",

    "account_menu": "The account menu",
    "your_account": "Your account — password, authenticator, email, signed-in sessions",
    "members": "Members — everyone in the workspace",
    "workspace_settings": "Workspace settings — name, invitation expiry",

    "dashboard_home": "Console home: tenants, departments, designations, complaint categories, employees, boundaries, localization messages, access roles",
    "public_dashboard": "Public Dashboard — anonymous access, off until published",
    "branding": "Branding, editable after onboarding",
    "tenants": "Tenants — the workspace's own tenant",
    "departments": "Departments",
    "designations": "Designations",
    "boundaries": "Boundaries — 80 (79 imported + the workspace root), on the map",
    "map_configuration": "Map Configuration",
    "complaints": "Complaints — status tabs; none filed yet",
    "complaint_types": "Complaint Categories — the 4 categories and their subcategories, by department",
    "complaint_hierarchies": "Complaint Hierarchies — category → subcategory",
    "escalation_policy": "PGR Escalation Policy — levels, ladder, automatic scan every 5 minutes",
    "localization": "Localization — English and Portuguese columns",
    "employees": "Employees — all seven, founder included",
    "org_chart": "Org Chart — seven employees; no reporting lines set yet",
    "users": "Users — citizen accounts; none yet",
    "access_roles": "Access Roles — 27",
    "processes": "Workflow Processes — none until a complaint is filed",
    "mdms_schemas": "MDMS Schemas",
    "analytics_providers": "Analytics Providers — nothing is sent until a destination is switched on",
    "notification_event_catalogue": "Notification Event Catalogue (read-only; events come from the modules)",
    "notification_routing": "Notification Routing",
    "notification_templates": "Notification Templates",
    "notification_provider_templates": "Provider Templates",
    "advanced_all_masters": "Advanced — every MDMS master",
}

NOTES = """
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

{NOT_PICTURED}

Boundary Hierarchies, Workflow Business Services and the Localization gaps are still on `develop`;
the Public Dashboard preview fills in once complaints exist. The notification screens only fail
because this local stack is deployed without notifications (Novu); on a deployment with them they
load.
"""

METHOD = """
## How this capture was made

Against the **local** DIGIT stack, deployed from `develop` at `{COMMIT}` on {CAPTURED} with
`local-setup/ansible/deploy.sh maputo` (images `develop-{SHORT}`; the configurator built from the
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
WT_HOST=http://localhost WT_OUT=output-develop \\
WT_KC_EMAIL=… WT_STORAGE_STATE=/path/to/signed-in-state.json .venv/bin/python capture_develop.py
.venv/bin/python import_develop_run.py /path/to/run/shots
WT_OUT=output-develop .venv/bin/python build_site_develop.py
.venv/bin/python build_doc_develop.py
```

The interactive sitemap and grid gallery are in
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


def status_table() -> str:
    f = OUT / "d09_manage" / "_api_status.json"
    if not f.exists():
        return "_(no API status recorded)_"
    data = json.loads(f.read_text())
    rows = ["| Screen | API calls | Refused (401/403) | Failed (5xx) |", "| --- | ---: | ---: | ---: |"]
    for label, v in data.items():
        if label in NOT_PICTURED:
            continue
        cap = SHOTS.get(label, label).split(" — ")[0].split(":")[0]
        rows.append(f"| {cap} | {v['requests']} | {v['denied']} | {v['errors']} |")
    return "\n".join(rows)


def main() -> int:
    total = sum(len(flow_shots(f)) for f, _, _ in SECTIONS)
    parts = [f"""# DIGIT configurator on `develop` — visual walkthrough

A screen-by-screen capture of the DIGIT configurator as it is on the `develop` branch
(`{COMMIT}`): Keycloak sign-in, self-serve sign-up, the onboarding Home and tour, the five
onboarding steps carried out for **Cidade de Maputo** with Mozambique's official boundaries, the
account pages, and the management console.

**{total} screens · {len(SECTIONS)} flows · captured {CAPTURED} on a local develop stack.** The sign-up
and onboarding steps created a throwaway workspace on that local stack; everything else was
captured read-only. See [How this capture was made](#how-this-capture-was-made).

The `master`-branch UI on bomet is in [`digit-ui-walkthrough.md`](digit-ui-walkthrough.md).

---

## Contents
"""]
    toc = [f"- [{h}](#{slug(h)})" for _, h, _ in SECTIONS]
    toc += [f"- [{h}](#{slug(h)})" for h in ("API calls per console screen", "What changed since the 2026-10-05 capture",
                                              "What is not pictured", "How this capture was made")]
    parts.append("\n".join(toc) + "\n\n---\n")

    missing_caps = []
    for flow, heading, intro in SECTIONS:
        shots = [p for p in flow_shots(flow) if label_of(p) not in NOT_PICTURED]
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

    parts.append("## API calls per console screen\n\nEvery console screen pictured above, with the API "
                 "calls it made while loading and how many were refused or failed.\n\n" + status_table() + "\n")
    parts.append("---\n")
    not_pictured = "\n".join(f"* **{SHOTS.get(k, k.replace('_', ' ').title())}** — {why}" if k in SHOTS
                             else f"* **{k.replace('_', ' ').capitalize()}** — {why}" for k, why in NOT_PICTURED.items())
    parts.append(NOTES.strip().replace("{NOT_PICTURED}", not_pictured) + "\n")
    parts.append("---\n")
    parts.append(METHOD.strip().replace("{CAPTURED}", CAPTURED).replace("{COMMIT}", COMMIT)
                 .replace("{SHORT}", COMMIT[:8]) + "\n")
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
