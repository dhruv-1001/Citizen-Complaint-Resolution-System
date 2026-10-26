#!/usr/bin/env python3
"""Render output-develop/index.html (sitemap graph) and gallery.html (grid) for the configurator capture.

Same renderer as build_site.py, with this capture's own flows and screen graph. The capture
keeps its "develop" file names; since 2026-10-26 it is taken on a local master stack.

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
    ("d02b_home",           "Onboarding · Home and welcome tour"),
    ("d03_branding",        "Onboarding · 1 Branding"),
    ("d04_geography",       "Onboarding · 2 Geography"),
    ("d04b_preconfigured",  "Onboarding · 2b Geography — Preconfigured"),
    ("d05_departments",     "Onboarding · 3 Departments"),
    ("d06_employees",       "Onboarding · 4 Employees"),
    ("d07_complaints",      "Onboarding · 5 Complaints Template"),
    ("d08_account",         "Account menu"),
    ("d09_manage",          "Management console"),
]

NODES = [
    ("landing",    "Configurator · Log in",           0, "auth"),
    ("kc",         "Keycloak sign-in",                1, "auth"),
    ("pwsetup",    "Set up / reset password",         1, "auth"),
    ("signup",     "Create an account",               1, "auth"),
    ("account",    "Account · name + code",           2, "signup"),
    ("prefs",      "Preferences",                     2, "signup"),
    ("review",     "Review + provisioning",           3, "signup"),
    ("home",       "Onboarding Home + tour",          3, "onboard"),
    ("branding",   "1 · Branding",                    4, "onboard"),
    ("geo",        "2 · Geography",                   4, "onboard"),
    ("geo_fetch",  "Fetch boundaries",                5, "onboard"),
    ("geo_excel",  "Upload from Excel",               5, "onboard"),
    ("geo_preconf","Preconfigured (official set)",    5, "onboard"),
    ("depts",      "3 · Departments",                 4, "onboard"),
    ("emps",       "4 · Employees",                   4, "onboard"),
    ("cats",       "5 · Complaints Template",         4, "onboard"),
    ("manage",     "Management console",              6, "manage"),
    ("acct",       "Account menu",                    6, "manage"),
]

EDGES = [
    ("landing", "kc", "Log in"), ("landing", "pwsetup", ""), ("landing", "signup", "Create an account"),
    ("signup", "account", "emailed sign-in link"),
    ("account", "prefs", "Continue"), ("prefs", "review", "Continue"),
    ("review", "home", "write: Create account"), ("home", "branding", "Set Up Branding"),
    ("branding", "geo", "write: Save"),
    ("geo", "geo_preconf", "Use these boundaries"), ("geo", "geo_fetch", "Search boundaries"),
    ("geo", "geo_excel", "Upload a file"),
    ("geo_preconf", "depts", "list, then write: Save and continue"), ("depts", "emps", "write: Save"),
    ("emps", "cats", "write: Save"), ("cats", "manage", "write: Finish setup"),
    ("manage", "acct", "account menu"), ("kc", "manage", "Sign In"),
]

GROUP_COLOR = {"auth": "#d8973c", "signup": "#e0672b", "onboard": "#8b5cf6", "manage": "#2f6fdb"}
LEGEND = [("Sign in", "#d8973c"), ("Sign up", "#e0672b"), ("Onboarding", "#8b5cf6"),
          ("Management console + account", "#2f6fdb")]

CAPTIONS = {
    "landing": "/configurator/ — a single Log in button; sign-in lives in Keycloak",
    "kc": "Keycloak, username-first: username or email, then password",
    "pwsetup": "One-use password set-up link by mail",
    "signup": "Self-serve sign-up: name and email",
    "account": "Account name and a code derived from it",
    "prefs": "Country, languages, time zone, financial year, slug, founder mobile",
    "review": "Review, then provisioning",
    "home": "Onboarding Home: welcome tour, next step, Learn the basics videos, documentation",
    "branding": "Logo, name, brand theme",
    "geo": "Preconfigured boundaries (with a confidence tag), Fetch boundaries, Upload from Excel",
    "geo_fetch": "Search official boundaries or OpenStreetMap — read-only here",
    "geo_excel": "Define the hierarchy's levels, then upload",
    "geo_preconf": "Search Mozambique's official set (Medium confidence) → a list of 79 areas, saved after a confirmation",
    "depts": "4 departments, 2 designations",
    "emps": "6 employees: a GRO per department, 2 field officers",
    "cats": "4 categories, 14 subcategories, 3-day default",
    "manage": "Workspace links, then every console route pictured — no refused calls",
    "acct": "Your account, Members, Workspace settings",
}

# (flow, filename marker) -> node; first match wins
MARKERS = [
    ("d01_signin", "configurator_landing", "landing"), ("d01_signin", "keycloak", "kc"),
    ("d01_signin", "password_setup", "pwsetup"), ("d01_signin", "signup", "signup"),
    ("d02_signup", "signup_", "signup"),
    ("d02_signup", "account_", "account"), ("d02_signup", "preferences", "prefs"),
    ("d02_signup", "review", "review"), ("d02_signup", "provisioning", "review"),
    ("d02b_home", "", "home"),
    ("d03_branding", "", "branding"),
    ("d04_geography", "geography_choose", "geo"), ("d04_geography", "excel", "geo_excel"),
    ("d04_geography", "", "geo_fetch"),
    ("d04b_preconfigured", "", "geo_preconf"),
    ("d05_departments", "", "depts"), ("d06_employees", "", "emps"),
    ("d07_complaints", "finished_lands", "manage"), ("d07_complaints", "", "cats"),
    ("d08_account", "", "acct"), ("d09_manage", "", "manage"),
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
        title="Sitemap · DIGIT configurator on master — walkthrough (2026-10-26)",
        heading='DIGIT configurator <span style="color:var(--mut)">· master 5dc402e09, local stack</span>',
        links=[("gallery.html", "Grid gallery →")],
        accent="#2f6fdb",
    )
    assets = json.loads((OUT / "node_assets.json").read_text())
    bs.make_thumbs({a["en"][0] for a in assets.values() if a.get("en")})
    bs.use_thumbs_in(("index.html", "sitemap.html"))
    build_flow_gallery(
        OUT, FLOWS, langs=(("en", "EN"),),
        title="DIGIT configurator on master — walkthrough (2026-10-26)",
        intro=("The configurator on master (5dc402e09): Keycloak sign-in, self-serve sign-up, the "
               "onboarding Home and tour, the five steps done for Cidade de Maputo with Mozambique's "
               "official boundaries, the account pages, and the management console."),
        links=[("index.html", "&#9783; Open the sitemap graph &rarr;")],
        footer=("Click any screenshot to zoom · captured on a local master stack on 2026-10-26; the "
                "sign-up and onboarding steps wrote to a throwaway workspace there, everything else is read-only."),
        accent="#2f6fdb",
    )
