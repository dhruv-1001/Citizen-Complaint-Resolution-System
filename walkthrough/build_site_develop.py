#!/usr/bin/env python3
"""Render output-develop/index.html (sitemap graph) and gallery.html (grid) for the develop capture.

Same renderer as build_site.py, with the develop capture's own flows and screen graph.

    .venv/bin/python build_site_develop.py
"""
import json
from pathlib import Path

import build_site as bs
from playwright_scraper import build_sitemap, build_flow_gallery, collect_node_assets

OUT = Path(__file__).resolve().parent / "output-develop"
bs.OUT = OUT                       # make_thumbs / use_thumbs_in read the module global

FLOWS = [
    ("d01_signin",          "Sign in · Keycloak"),
    ("d02_signup",          "Sign up · a new workspace"),
    ("d03_branding",        "Onboarding · 1 Branding"),
    ("d04_geography",       "Onboarding · 2 Geography (OCHA COD-AB)"),
    ("d04b_preconfigured",  "Onboarding · 2b Geography — Preconfigured"),
    ("d05_departments",     "Onboarding · 3 Departments"),
    ("d06_employees",       "Onboarding · 4 Employees"),
    ("d07_complaints",      "Onboarding · 5 Complaints Template"),
    ("d08_onboarding_done", "Onboarding · finished"),
    ("d09_manage",          "Management console · as the new founder"),
    ("d10_apps",            "Citizen app"),
]

NODES = [
    ("landing",   "Configurator · Log in",           0, "auth"),
    ("kc",        "Keycloak sign-in",                1, "auth"),
    ("pwsetup",   "Set up / reset password",         1, "auth"),
    ("signup",    "Create an account",               1, "auth"),
    ("mail",      "Mailpit · sign-in link",          2, "auth"),
    ("account",   "Account · name + code",           2, "signup"),
    ("prefs",     "Preferences",                     2, "signup"),
    ("review",    "Review + provisioning",           3, "signup"),
    ("workspace", "Choose a workspace",              3, "signup"),
    ("branding",  "1 · Branding",                    4, "onboard"),
    ("geo",       "2 · Geography",                   4, "onboard"),
    ("geo_fetch", "Fetch boundaries (COD-AB)",       5, "onboard"),
    ("geo_levels","Map Admin Levels",                5, "onboard"),
    ("geo_preconf","Preconfigured (official set)",   5, "onboard"),
    ("depts",     "3 · Departments",                 4, "onboard"),
    ("emps",      "4 · Employees",                   4, "onboard"),
    ("cats",      "5 · Complaints Template",         4, "onboard"),
    ("done",      "Onboarding finished",             5, "onboard"),
    ("manage",    "Management console",              6, "manage"),
    ("citizen",   "Citizen /citizen",                0, "apps"),
]

EDGES = [
    ("landing", "kc", "Log in"), ("landing", "pwsetup", ""), ("landing", "signup", "Create an account"),
    ("signup", "mail", "link by mail"), ("mail", "account", "open link"),
    ("account", "prefs", "Continue"), ("prefs", "review", "Continue"),
    ("review", "workspace", "write: Create account"), ("kc", "workspace", "Sign In"),
    ("workspace", "branding", ""), ("branding", "geo", "write: Save"),
    ("geo", "geo_fetch", "Search boundaries"), ("geo", "geo_preconf", "Use these boundaries"), ("geo_fetch", "geo_levels", "Search"),
    ("geo_levels", "depts", "write: Create + Save"), ("depts", "emps", "write: Save"),
    ("emps", "cats", "write: Save"), ("cats", "done", "write: Finish setup"),
    ("done", "manage", "lands in"),
]

GROUP_COLOR = {"auth": "#d8973c", "signup": "#e0672b", "onboard": "#8b5cf6",
               "manage": "#2f6fdb", "apps": "#3fae6b"}
LEGEND = [("Sign in", "#d8973c"), ("Sign up", "#e0672b"), ("Onboarding", "#8b5cf6"),
          ("Management console", "#2f6fdb"), ("Citizen app", "#3fae6b")]

CAPTIONS = {
    "landing": "/configurator/ — a single Log in button; sign-in lives in Keycloak",
    "kc": "Keycloak, username-first: email, then password (or GitHub)",
    "pwsetup": "One-use password set-up link by mail",
    "signup": "Self-serve sign-up: name and email",
    "mail": "The sign-in link in Mailpit",
    "account": "Account name and derived code (CDM → MZ-CDM)",
    "prefs": "Country, languages, time zone, financial year, slug, founder mobile",
    "review": "Review, then provisioning — failed once on MDMS_SCHEMA_NOT_VISIBLE, finished on retry",
    "workspace": "Choose a workspace",
    "branding": "Logo, name, brand theme",
    "geo": "Preconfigured (soon), Fetch boundaries, Upload from Excel",
    "geo_fetch": "turbopass search — OCHA COD-AB for Cidade de Maputo",
    "geo_levels": "4 COD levels, 79 areas, named Cidade → Distrito Municipal → Posto Administrativo → Bairro",
    "geo_preconf": "Preconfigured: the country's official set with per-level confidence, no search",
    "depts": "Departments + designations",
    "emps": "Employees — one GRO per complaint department",
    "cats": "4 categories, 14 subcategories, 3-day target; Finish refused until every department had a GRO",
    "done": "Each step after Finish setup",
    "manage": "Every console route as the founder — many API calls refused (403)",
    "citizen": "/citizen — digit-ui-v2 sign-in",
}

# (flow, filename marker) -> node; first match wins
MARKERS = [
    ("d01_signin", "configurator_landing", "landing"), ("d01_signin", "keycloak", "kc"),
    ("d01_signin", "password_setup", "pwsetup"), ("d01_signin", "signup", "signup"),
    ("d02_signup", "signup_", "signup"), ("d02_signup", "mailpit", "mail"),
    ("d02_signup", "account_", "account"), ("d02_signup", "preferences", "prefs"),
    ("d02_signup", "review", "review"), ("d02_signup", "provisioning", "review"),
    ("d02_signup", "choose_workspace", "workspace"),
    ("d03_branding", "", "branding"),
    ("d04_geography", "geography_choose", "geo"), ("d04_geography", "geography_with", "geo"),
    ("d04_geography", "fetch_", "geo_fetch"), ("d04_geography", "source_options", "geo_fetch"),
    ("d04_geography", "cod_suggestions", "geo_fetch"), ("d04_geography", "", "geo_levels"),
    ("d04b_preconfigured", "", "geo_preconf"),
    ("d05_departments", "", "depts"), ("d06_employees", "", "emps"),
    ("d07_complaints", "finished_lands", "manage"), ("d07_complaints", "", "cats"),
    ("d08_onboarding_done", "", "done"), ("d09_manage", "", "manage"),
    ("d10_apps", "citizen", "citizen"),
]


def classify(flow, fn):
    f = fn.lower()
    for fl, marker, node in MARKERS:
        if fl == flow and marker in f:
            return node
    print(f"  [unclassified] {flow}/{fn}")
    return None


if __name__ == "__main__":
    collect_node_assets(OUT, [f for f, _ in FLOWS], classify, langs=("en",), captions=CAPTIONS)
    build_sitemap(
        OUT, NODES, EDGES,
        group_colors=GROUP_COLOR, legend=LEGEND, langs=(("en", "EN"),),
        title="Sitemap · DIGIT develop UI walkthrough · 141.94.92.163.nip.io (2026-10-05)",
        heading='DIGIT develop UI <span style="color:var(--mut)">· 141.94.92.163.nip.io</span>',
        links=[("gallery.html", "Grid gallery →")],
        accent="#2f6fdb",
    )
    assets = json.loads((OUT / "node_assets.json").read_text())
    bs.make_thumbs({a["en"][0] for a in assets.values() if a.get("en")})
    bs.use_thumbs_in(("index.html", "sitemap.html"))
    build_flow_gallery(
        OUT, FLOWS, langs=(("en", "EN"),),
        title="DIGIT develop UI walkthrough · 141.94.92.163.nip.io (2026-10-05)",
        intro=("Keycloak sign-in, self-serve sign-up, the five-step onboarding done for Cidade de "
               "Maputo with OCHA COD-AB boundaries, and the management console as the new "
               "workspace's founder sees it."),
        links=[("index.html", "&#9783; Open the sitemap graph &rarr;")],
        footer=("Click any screenshot to zoom · the sign-up and onboarding steps wrote to a "
                "throwaway workspace (cidadedemaputo); everything else was captured read-only."),
        accent="#2f6fdb",
    )
