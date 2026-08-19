#!/usr/bin/env python3
"""Render the walkthrough site into output/:

    index.html      interactive sitemap graph (one thumbnail node per screen)
    gallery.html    grouped grid gallery with a sticky flow nav
    _graph_all.png  one composite PNG of every screenshot

Run after capture_configurator.py + capture_employee.py.
"""
import os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from playwright_scraper import build_sitemap, build_flow_gallery, collect_node_assets
from playwright_scraper.gallery import build_composite

OUT = HERE / "output"

FLOWS = [
    ("01_login",                 "Configurator · Sign In"),
    ("02_onboarding",            "Configurator · Onboarding wizard (4 phases)"),
    ("03_home",                  "Configurator · Management console"),
    ("04_tenant",                "Configurator · Tenant management"),
    ("05_complaints",            "Configurator · Complaints & localization"),
    ("06_people",                "Configurator · People (employees, users, org chart)"),
    ("07_system",                "Configurator · System (roles, workflow, MDMS, boundaries)"),
    ("08_notifications",         "Configurator · Notifications"),
    ("09_dashboards",            "Configurator · Dashboards"),
    ("10_known_gaps",            "Configurator · Known gaps on this deployment"),
    ("11_employee_login",        "Employee UI · Sign In"),
    ("12_employee_inbox",        "Employee UI · Complaint inbox"),
    ("13_employee_new_complaint","Employee UI · New complaint intake"),
    ("14_employee_search",       "Employee UI · Search complaint"),
]

# ---------------------------------------------------------------- screen graph
# `level` is the vertical rank in the sitemap graph. vis-network's hierarchical
# layout lays every node of one level out on a single row at fixed spacing, so
# levels are balanced to <=8 nodes — a 20-wide row zooms the whole graph out
# until the thumbnails are unreadable.

NODES = [
    # configurator
    ("login",            "Configurator Sign In",              0, "auth"),
    ("onb_p1",           "Phase 1 · Tenant & Branding",       1, "onboard"),
    ("onb_p2",           "Phase 2 · Boundary Setup",          2, "onboard"),
    ("onb_p3",           "Phase 3 · Common Masters",          3, "onboard"),
    ("onb_p4",           "Phase 4 · Employee Onboarding",     4, "onboard"),
    ("onb_done",         "Setup Complete",                    5, "onboard"),
    ("mgmt_home",        "Management Dashboard",              1, "manage"),
    ("mgmt_advanced",    "Advanced · all MDMS masters",       2, "manage"),
    ("pgr_dash",         "PGR Dashboard",                     2, "dash"),
    ("public_dash",      "Public Dashboard config",           2, "dash"),
    ("tenants",          "Tenants",                           3, "masters"),
    ("bnd_hier",         "Boundary Hierarchies",              3, "masters"),
    ("complaints",       "Complaints (empty)",                3, "masters"),
    ("localization",     "Localization Messages",             3, "masters"),
    ("employees",        "Employees",                         3, "masters"),
    ("org_chart",        "Org Chart",                         3, "masters"),
    ("users",            "Users",                             4, "masters"),
    ("access_roles",     "Access Roles",                      4, "masters"),
    ("workflows",        "Workflow Business Services",        4, "masters"),
    ("processes",        "Workflow Processes (empty)",        4, "masters"),
    ("mdms_schemas",     "MDMS Schemas",                      4, "masters"),
    ("boundaries",       "Boundaries",                        4, "masters"),
    ("notif_configure",  "Notifications · Configure",         5, "notify"),
    ("notif_templates",  "Notification Templates",            5, "notify"),
    ("notif_logs",       "Notification Logs",                 5, "notify"),
    ("notif_providers",  "Notification Providers",            5, "notify"),
    ("notif_prefs",      "User Preferences",                  5, "notify"),
    ("dept_create",      "Create Department (form only)",     6, "forms"),
    ("emp_create",       "Create Employee (form only)",       6, "forms"),
    ("bnd_create",       "Create Boundary (form only)",       6, "forms"),
    ("emp_bulk",         "Employees · Bulk import",           6, "forms"),
    ("loc_bulk",         "Localization · Bulk import",        6, "forms"),
    ("gap_departments",  "Departments — load error",          7, "gaps"),
    ("gap_designations", "Designations — load error",         7, "gaps"),
    ("gap_types",        "Complaint Types — load error",      7, "gaps"),
    ("gap_hierarchies",  "Complaint Hierarchies — load error", 7, "gaps"),
    ("gap_mapconfig",    "Map Configuration — load error",    7, "gaps"),
    ("gap_routing",      "Notification Routing — load error", 7, "gaps"),
    ("gap_provtpl",      "Provider Templates — load error",   7, "gaps"),
    # employee UI
    ("emp_login",        "Employee Sign In",                  0, "emp"),
    ("emp_home",         "Employee Home",                     1, "emp"),
    ("emp_inbox_v2",     "PGR Inbox v2 (search + filters)",   2, "emp"),
    ("emp_inbox_v1",     "PGR Inbox (legacy)",                2, "emp"),
    ("emp_search",       "Search Complaint",                  2, "emp"),
    ("emp_new",          "New Complaint intake (not submitted)", 3, "emp"),
]

MASTERS = ["tenants", "bnd_hier", "complaints", "localization", "employees", "org_chart",
           "users", "access_roles", "workflows", "processes", "mdms_schemas", "boundaries"]
NOTIFS = ["notif_configure", "notif_templates", "notif_logs", "notif_providers", "notif_prefs"]
GAPS = ["gap_departments", "gap_designations", "gap_types", "gap_hierarchies",
        "gap_mapconfig", "gap_routing", "gap_provtpl"]

EDGES = (
    [("login", "onb_p1", "Onboarding mode"), ("login", "mgmt_home", "Management mode"),
     ("onb_p1", "onb_p2", ""), ("onb_p2", "onb_p3", ""), ("onb_p3", "onb_p4", ""),
     ("onb_p4", "onb_done", ""),
     ("mgmt_home", "mgmt_advanced", "Advanced"),
     ("mgmt_home", "pgr_dash", ""), ("mgmt_home", "public_dash", ""),
     ("employees", "emp_create", "Create"), ("employees", "emp_bulk", "Bulk import"),
     ("boundaries", "bnd_create", "Create"), ("localization", "loc_bulk", "Bulk import"),
     ("gap_departments", "dept_create", "Create"),
     ("emp_login", "emp_home", "Login"),
     ("emp_home", "emp_inbox_v2", "Search Complaint"), ("emp_home", "emp_inbox_v1", ""),
     ("emp_home", "emp_search", ""), ("emp_inbox_v2", "emp_new", "New Complaint")]
    + [("mgmt_home", n, "") for n in MASTERS]
    + [("mgmt_home", n, "") for n in NOTIFS]
    + [("mgmt_home", n, "") for n in GAPS]
)

GROUP_COLOR = {
    "auth": "#d8973c", "onboard": "#8b5cf6", "manage": "#2f6fdb", "masters": "#3f7fae",
    "notify": "#2bb3a3", "dash": "#c2477f", "forms": "#5fa8d3", "gaps": "#c0392b",
    "emp": "#3fae6b",
}
LEGEND = [
    ("Sign In", "#d8973c"), ("Onboarding wizard", "#8b5cf6"), ("Management console", "#2f6fdb"),
    ("Masters & registries", "#3f7fae"), ("Notifications", "#2bb3a3"), ("Dashboards", "#c2477f"),
    ("Forms & bulk import", "#5fa8d3"), ("Known gaps", "#c0392b"), ("Employee UI", "#3fae6b"),
]

CAPTIONS = {
    "login": "/configurator/login — username, password, root tenant, and the Onboarding/Management mode switch",
    "onb_p1": "Phase 1: create the tenant and upload branding (100 tenants already exist under ke)",
    "onb_p2": "Phase 2: boundary hierarchy — view-only for this operator's roles",
    "onb_p3": "Phase 3: departments, designations and complaint types",
    "onb_p4": "Phase 4: bulk employee creation with roles and jurisdictions",
    "onb_done": "Completion summary: 33 departments, 46 designations, 685 complaint types at ke",
    "mgmt_home": "Management console home — record counts per registry",
    "mgmt_advanced": "Advanced: every generic MDMS master the data provider exposes",
    "pgr_dash": "PGR operational dashboard",
    "public_dash": "Public dashboard configuration",
    "tenants": "Tenant registry",
    "bnd_hier": "Boundary hierarchy definitions (ADMIN hierarchy shown)",
    "complaints": "Complaint registry — bomet currently holds zero PGR complaints",
    "localization": "Localization messages (14,258 on this deployment)",
    "employees": "HRMS employees, list and detail",
    "org_chart": "Department/designation org chart",
    "users": "User accounts, list and detail",
    "access_roles": "Access roles (49 on this deployment)",
    "workflows": "Workflow business services — the PGR state machine",
    "processes": "Workflow process instances — empty, no complaints exist",
    "mdms_schemas": "MDMS v2 schema definitions",
    "boundaries": "Boundary records (BOMET shown)",
    "notif_configure": "Notification routing configuration surface",
    "notif_templates": "Notification templates",
    "notif_logs": "Notification delivery log (Novu bridge)",
    "notif_providers": "Configured notification providers",
    "notif_prefs": "Per-user notification preferences",
    "dept_create": "Department create form, blank and filled — never submitted",
    "emp_create": "Employee create form, blank and filled — never submitted",
    "bnd_create": "Boundary create form, blank and filled — never submitted",
    "emp_bulk": "Employee bulk import (XLSX upload)",
    "loc_bulk": "Localization bulk import",
    "emp_login": "/digit-ui/employee — city picker, credentials, privacy consent",
    "emp_home": "Employee home. Only PGR is enabled on bomet; DSS/HRMS/Workbench fall back here",
    "emp_inbox_v2": "PGR inbox v2: complaint no / mobile / date search, subtype + county + status filters",
    "emp_inbox_v1": "Legacy PGR inbox",
    "emp_search": "Search Complaint — no results, the deployment has no complaints",
    "emp_new": "New complaint intake: complainant, type/category/sub-type, map pin, description",
}
CAPTIONS.update({
    "gap_departments": "Departments list — 'Error loading data: No static resource v2/_count'",
    "gap_designations": "Designations list — same missing MDMS v2/_count endpoint",
    "gap_types": "Complaint Types list — same missing MDMS v2/_count endpoint",
    "gap_hierarchies": "Complaint Hierarchies list — same missing MDMS v2/_count endpoint",
    "gap_mapconfig": "Map Configuration — same missing MDMS v2/_count endpoint",
    "gap_routing": "Notification Routing — same missing MDMS v2/_count endpoint",
    "gap_provtpl": "Provider Templates (WhatsApp) — same missing MDMS v2/_count endpoint",
})

# filename marker -> node id, checked in order
# NOTE: order matters — the first marker that appears in the filename wins, so
# the employee-UI markers must precede the configurator ones they'd collide
# with ("employee_signin" would otherwise be eaten by "signin").
MARKERS = [
    ("employee_signin", "emp_login"), ("employee_city", "emp_login"),
    ("employee_home", "emp_home"),
    ("signin", "login"), ("phase1", "onb_p1"), ("phase2", "onb_p2"), ("phase3", "onb_p3"),
    ("phase4", "onb_p4"), ("complete", "onb_done"),
    ("dashboard_home", "mgmt_home"), ("advanced", "mgmt_advanced"),
    ("pgr_dashboard", "pgr_dash"), ("public_dashboard", "public_dash"),
    ("tenants_list", "tenants"), ("boundary_hierarchies", "bnd_hier"),
    ("complaints_list", "complaints"),
    ("localization_bulk", "loc_bulk"), ("localization_messages", "localization"),
    ("employees_bulk", "emp_bulk"), ("employee_create", "emp_create"),
    ("employees_list", "employees"), ("employees_detail", "employees"),
    ("org_chart", "org_chart"), ("users_", "users"),
    ("access_roles", "access_roles"), ("workflows", "workflows"),
    ("processes_list", "processes"), ("mdms_schemas", "mdms_schemas"),
    ("boundary_create", "bnd_create"), ("boundaries_", "boundaries"),
    ("department_create", "dept_create"),
    ("notification_configure", "notif_configure"), ("notification_templates", "notif_templates"),
    ("notification_logs", "notif_logs"), ("notification_providers", "notif_providers"),
    ("user_preferences", "notif_prefs"),
    ("departments_list_error", "gap_departments"), ("designations_list_error", "gap_designations"),
    ("complaint_types_list_error", "gap_types"),
    ("complaint_hierarchies_list_error", "gap_hierarchies"),
    ("map_configuration_error", "gap_mapconfig"),
    ("notification_routing_error", "gap_routing"),
    ("provider_templates_whatsapp_error", "gap_provtpl"),
    ("inbox_v2", "emp_inbox_v2"), ("inbox_v1", "emp_inbox_v1"),
    ("create_complaint", "emp_new"), ("dropdown_", "emp_new"),
    ("search_complaint", "emp_search"),
]


def classify(flow, fn):
    f = fn.lower()
    for marker, node in MARKERS:
        if marker in f:
            return node
    print(f"  [unclassified] {flow}/{fn}")
    return None


if __name__ == "__main__":
    collect_node_assets(OUT, [f for f, _ in FLOWS], classify, langs=("en",), captions=CAPTIONS)
    build_sitemap(
        OUT, NODES, EDGES,
        group_colors=GROUP_COLOR, legend=LEGEND, langs=(("en", "EN"),),
        title="Sitemap · DIGIT Configurator + Employee UI — bomet walkthrough",
        heading='DIGIT Configurator &amp; Employee UI <span style="color:var(--mut)">· bometfeedbackhub.digit.org</span>',
        links=[("gallery.html", "Grid gallery →")],
        accent="#2f6fdb",
    )
    build_flow_gallery(
        OUT, FLOWS, langs=(("en", "EN"),),
        title="DIGIT Configurator & Employee UI — bomet walkthrough",
        intro="Read-only capture of bometfeedbackhub.digit.org: the configurator's onboarding wizard and management console, plus the digit-ui employee app.",
        links=[("index.html", "&#9783; Open the sitemap graph &rarr;")],
        footer=("Click any screenshot to zoom · captured read-only as ADMIN on tenant ke — "
                "no record was created, updated or deleted."),
        accent="#2f6fdb",
    )
    shots = sorted(Path(OUT, "en").glob("*/*.png"))
    build_composite(shots, Path(OUT, "_graph_all.png"),
                    title="DIGIT Configurator + Employee UI — bomet walkthrough", cols=6, thumb_w=420)
    print(f"_graph_all.png: {len(shots)} shots composited")
