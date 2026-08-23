#!/usr/bin/env python3
"""Render the walkthrough site into output/:

    index.html      interactive sitemap graph (one thumbnail node per screen)
    gallery.html    grouped grid gallery with a sticky flow nav
    _graph_all.png  one composite PNG of every screenshot

Run after capture_configurator.py + capture_onboarding.py + capture_employee.py.
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
    ("02_phase1_tenant",         "Onboarding · Phase 1 — Tenant & Branding"),
    ("03_phase2_boundary",       "Onboarding · Phase 2 — Boundary Setup"),
    ("04_phase3_masters",        "Onboarding · Phase 3 — Common Masters"),
    ("05_phase4_employees",      "Onboarding · Phase 4 — Employee Onboarding"),
    ("06_onboarding_complete",   "Onboarding · Complete"),
    ("07_home",                  "Configurator · Management console"),
    ("08_tenant",                "Configurator · Tenant, boundaries & map"),
    ("09_complaints",            "Configurator · Complaints & localization"),
    ("10_people",                "Configurator · People & org structure"),
    ("11_system",                "Configurator · System (roles, workflow, MDMS)"),
    ("12_notifications",         "Configurator · Notifications"),
    ("13_dashboards",            "Configurator · Public dashboard"),
    ("14_employee_login",        "Employee UI · Sign In"),
    ("15_employee_inbox",        "Employee UI · Complaint inbox"),
    ("16_employee_complaint_detail","Employee UI · Complaint detail & workflow"),
    ("17_employee_new_complaint","Employee UI · New complaint intake"),
    ("18_employee_search",       "Employee UI · Search complaint"),
]

# ---------------------------------------------------------------- screen graph
# `level` is the vertical rank in the sitemap graph. vis-network's hierarchical
# layout lays every node of one level out on a single row at fixed spacing, so
# levels are balanced to <=8 nodes — a 20-wide row zooms the whole graph out
# until the thumbnails are unreadable.

NODES = [
    # entry points
    ("login",            "Configurator Sign In",                 0, "auth"),
    ("emp_login",        "Employee Sign In",                     0, "emp"),
    ("onb_p1_landing",   "Phase 1 · Tenant & Branding",          1, "onboard"),
    ("mgmt_home",        "Management Dashboard",                 1, "manage"),
    ("emp_home",         "Employee Home",                        1, "emp"),
    # onboarding wizard
    ("onb_p1_existing",  "Phase 1 · Use Existing Tenant",        2, "onboard"),
    ("onb_p1_upload",    "Phase 1 · Upload Tenant Master",       2, "onboard"),
    ("onb_p1_preview",   "Phase 1 · Preview (Tenant/Branding)",  2, "onboard"),
    ("onb_p2_landing",   "Phase 2 · Choose Data Source",         3, "onboard"),
    ("onb_p2_excel",     "Phase 2 · Excel: choose path",         3, "onboard"),
    ("onb_p2_create_hier","Phase 2 · Create Hierarchy",          3, "onboard"),
    ("onb_p2_select_hier","Phase 2 · Select Existing Hierarchy", 3, "onboard"),
    ("onb_p2_template",  "Phase 2 · Download Template",          3, "onboard"),
    ("onb_p2_verify",    "Phase 2 · Verify Boundary Data",       3, "onboard"),
    ("onb_p2_osm_search","Phase 2 · OSM Search",                 4, "onboard"),
    ("onb_p2_osm_levels","Phase 2 · Map Admin Levels",           4, "onboard"),
    ("onb_p3_landing",   "Phase 3 · Common Masters",             4, "onboard"),
    ("onb_p3_upload",    "Phase 3 · Upload Master Excel",        4, "onboard"),
    ("onb_p3_preview",   "Phase 3 · Preview depts & designations", 4, "onboard"),
    ("onb_p4_landing",   "Phase 4 · Employee Onboarding",        4, "onboard"),
    ("onb_p4_preview",   "Phase 4 · Employee row validation",    4, "onboard"),
    ("onb_done",         "Onboarding Complete",                  4, "onboard"),
    # management console
    ("mgmt_advanced",    "Advanced · all MDMS masters",          2, "manage"),
    ("public_dash",      "Public Dashboard config",              8, "dash"),
    ("tenants",          "Tenants",                              5, "masters"),
    ("bnd_hier",         "Boundary Hierarchies",                 5, "masters"),
    ("boundaries",       "Boundaries",                           5, "masters"),
    ("map_config",       "Map Configuration",                    5, "masters"),
    ("complaints",       "Complaints",                           5, "masters"),
    ("complaint_types",  "Complaint Types",                      5, "masters"),
    ("complaint_hier",   "Complaint Hierarchies",                5, "masters"),
    ("localization",     "Localization Messages",                5, "masters"),
    ("departments",      "Departments",                          6, "masters"),
    ("designations",     "Designations",                         6, "masters"),
    ("employees",        "Employees",                            6, "masters"),
    ("org_chart",        "Org Chart",                            6, "masters"),
    ("users",            "Users",                                6, "masters"),
    ("access_roles",     "Access Roles",                         6, "masters"),
    ("workflows",        "Workflow Business Services",           6, "masters"),
    ("processes",        "Workflow Processes",                   6, "masters"),
    ("mdms_schemas",     "MDMS Schemas",                         7, "masters"),
    ("notif_configure",  "Notifications · Configure",            7, "notify"),
    ("notif_routing",    "Notification Routing",                 7, "notify"),
    ("notif_templates",  "Notification Templates",               7, "notify"),
    ("notif_provtpl",    "Provider Templates (WhatsApp)",        7, "notify"),
    ("notif_logs",       "Notification Logs",                    7, "notify"),
    ("notif_providers",  "Notification Providers",               7, "notify"),
    ("notif_prefs",      "User Preferences",                     7, "notify"),
    ("dept_create",      "Create Department (form only)",        8, "forms"),
    ("emp_create",       "Create Employee (form only)",          8, "forms"),
    ("bnd_create",       "Create Boundary (form only)",          8, "forms"),
    ("emp_bulk",         "Employees · Bulk import",              8, "forms"),
    ("loc_bulk",         "Localization · Bulk import",           8, "forms"),
    # employee UI
    ("emp_inbox_v2",     "PGR Inbox v2 (search + filters)",      2, "emp"),
    ("emp_inbox_v1",     "PGR Inbox (legacy)",                   2, "emp"),
    ("emp_search",       "Search Complaint",                     2, "emp"),
    ("emp_detail",       "Complaint detail + workflow timeline",  3, "emp"),
    ("emp_new",          "New Complaint intake (not submitted)", 3, "emp"),
]

MASTERS = ["tenants", "bnd_hier", "boundaries", "map_config", "complaints",
           "complaint_types", "complaint_hier", "localization", "departments",
           "designations", "employees", "org_chart", "users", "access_roles",
           "workflows", "processes", "mdms_schemas"]
NOTIFS = ["notif_configure", "notif_routing", "notif_templates", "notif_provtpl",
          "notif_logs", "notif_providers", "notif_prefs"]

# "write" on an edge = the wizard POSTs to DIGIT there, so the capture stops and
# the next screen was reached by direct URL instead of by clicking through.
EDGES = (
    [("login", "onb_p1_landing", "Onboarding mode"), ("login", "mgmt_home", "Management mode"),
     ("onb_p1_landing", "onb_p1_existing", "Use existing tenant"),
     ("onb_p1_landing", "onb_p1_upload", "Start Setup"),
     ("onb_p1_upload", "onb_p1_preview", "file parsed in-browser"),
     ("onb_p1_existing", "onb_p2_landing", "Use this"),
     ("onb_p1_preview", "onb_p2_landing", "write"),
     ("onb_p2_landing", "onb_p2_excel", "Upload from Excel"),
     ("onb_p2_landing", "onb_p2_osm_search", "Fetch from OSM"),
     ("onb_p2_excel", "onb_p2_create_hier", "Option 1"),
     ("onb_p2_excel", "onb_p2_select_hier", "Option 2"),
     ("onb_p2_select_hier", "onb_p2_template", "Use Selected"),
     ("onb_p2_template", "onb_p2_verify", "file parsed in-browser"),
     ("onb_p2_osm_search", "onb_p2_osm_levels", "Search"),
     ("onb_p2_verify", "onb_p3_landing", "write"),
     ("onb_p2_osm_levels", "onb_p3_landing", "write"),
     ("onb_p3_landing", "onb_p3_upload", "Start Setup"),
     ("onb_p3_upload", "onb_p3_preview", "file parsed in-browser"),
     ("onb_p3_preview", "onb_p4_landing", "write"),
     ("onb_p4_landing", "onb_p4_preview", "file parsed in-browser"),
     ("onb_p4_preview", "onb_done", "write"),
     ("mgmt_home", "mgmt_advanced", "Advanced"),
     ("mgmt_home", "public_dash", ""),
     ("employees", "emp_create", "Create"), ("employees", "emp_bulk", "Bulk import"),
     ("boundaries", "bnd_create", "Create"), ("localization", "loc_bulk", "Bulk import"),
     ("departments", "dept_create", "Create"),
     ("emp_login", "emp_home", "Login"),
     ("emp_home", "emp_inbox_v2", ""), ("emp_home", "emp_inbox_v1", ""),
     ("emp_home", "emp_search", ""), ("emp_inbox_v2", "emp_new", "New Complaint"),
     ("emp_inbox_v2", "emp_detail", "open a complaint")]
    + [("mgmt_home", n, "") for n in MASTERS]
    + [("mgmt_home", n, "") for n in NOTIFS]
)

GROUP_COLOR = {
    "auth": "#d8973c", "onboard": "#8b5cf6", "manage": "#2f6fdb", "masters": "#3f7fae",
    "notify": "#2bb3a3", "dash": "#c2477f", "forms": "#5fa8d3", "emp": "#3fae6b",
}
LEGEND = [
    ("Sign In", "#d8973c"), ("Onboarding wizard", "#8b5cf6"), ("Management console", "#2f6fdb"),
    ("Masters & registries", "#3f7fae"), ("Notifications", "#2bb3a3"), ("Public dashboard", "#c2477f"),
    ("Forms & bulk import", "#5fa8d3"), ("Employee UI", "#3fae6b"),
]

CAPTIONS = {
    "login": "/configurator/login — username, password, root tenant, and the Onboarding/Management mode switch",
    "onb_p1_landing": "Phase 1 landing. 100 tenants already exist under ke, so the skip-ahead banner is shown",
    "onb_p1_existing": "Use Existing Tenant — picking a row skips to Phase 2 without creating anything",
    "onb_p1_upload": "Step 1.1: the Tenant Master dropzone",
    "onb_p1_preview": "Preview of a sample workbook, parsed in the browser: Tenant Info and Branding Details tabs",
    "onb_p2_landing": "Phase 2: OpenStreetMap or Excel as the boundary source",
    "onb_p2_excel": "Excel path: create a new hierarchy or reuse an existing one",
    "onb_p2_create_hier": "Define Hierarchy — name plus an ordered level list. Filled here, never submitted",
    "onb_p2_select_hier": "Select Existing Hierarchy — bomet returns 100 PW_* test hierarchies and no ADMIN",
    "onb_p2_template": "Boundary Data Upload: a template generated for the chosen hierarchy's levels",
    "onb_p2_verify": "Verify Boundary Data — All/Valid/Errors tabs plus the optional GeoJSON outline slot",
    "onb_p2_osm_search": "OSM Search: look the area up on Nominatim before importing",
    "onb_p2_osm_levels": "Map Admin Levels — OSM levels found for Bomet, each mapped to a hierarchy level",
    "onb_p3_landing": "Phase 3 landing: departments, designations and complaint types",
    "onb_p3_upload": "Common Master dropzone",
    "onb_p3_preview": "Parsed departments and designations with per-row validation",
    "onb_p4_landing": "Phase 4 landing — blocked on bomet: the reference load finds no boundaries for ke",
    "onb_p4_preview": "Per-row employee validation, with the Re-upload Fixed File escape hatch",
    "onb_done": "Completion summary — live tenant totals, portal links, and the dead View Setup History button",
    "mgmt_home": "Management console home — record counts per registry",
    "mgmt_advanced": "Advanced: every generic MDMS master the data provider exposes",
    "public_dash": "Public dashboard configuration",
    "tenants": "Tenant registry",
    "bnd_hier": "Boundary hierarchy definitions",
    "boundaries": "Boundary records (BOMET shown)",
    "map_config": "Map Configuration — centre, zoom and tile settings per tenant",
    "complaints": "Complaint registry",
    "complaint_types": "Complaint Types (service definitions)",
    "complaint_hier": "Complaint Hierarchies — category / sub-category tree",
    "localization": "Localization messages",
    "departments": "Departments master",
    "designations": "Designations master",
    "employees": "HRMS employees, list and detail",
    "org_chart": "Department/designation org chart",
    "users": "User accounts, list and detail",
    "access_roles": "Access roles",
    "workflows": "Workflow business services — the PGR state machine",
    "processes": "Workflow process instances",
    "mdms_schemas": "MDMS v2 schema definitions",
    "notif_configure": "Notification routing configuration surface",
    "notif_routing": "Notification Routing rules",
    "notif_templates": "Notification templates",
    "notif_provtpl": "Provider templates (WhatsApp)",
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
    "emp_search": "Search Complaint",
    "emp_detail": "One complaint opened from the inbox, with its workflow history below the fold",
    "emp_new": "New complaint intake: complainant, type/category/sub-type, map pin, description",
}

# filename marker -> node id, checked in order
# NOTE: order matters — the first marker that appears in the filename wins, so
# specific markers must precede the ones they'd collide with ("employee_signin"
# would otherwise be eaten by "signin", "p1_upload" by "upload").
MARKERS = [
    # onboarding wizard
    ("p1_landing", "onb_p1_landing"), ("p1_select_existing", "onb_p1_existing"),
    ("p1_upload", "onb_p1_upload"), ("p1_change_file", "onb_p1_upload"),
    ("p1_preview", "onb_p1_preview"),
    ("p2_landing", "onb_p2_landing"), ("p2_excel", "onb_p2_excel"),
    ("p2_create_hierarchy", "onb_p2_create_hier"),
    ("p2_select_existing_hierarchy", "onb_p2_select_hier"),
    ("p2_hierarchy_selected", "onb_p2_select_hier"),
    ("p2_hierarchy_path_stalled", "onb_p2_select_hier"),
    ("p2_download_template", "onb_p2_template"),
    ("p2_verify", "onb_p2_verify"), ("p2_boundary_upload_rejected", "onb_p2_verify"),
    ("p2_osm_map_levels", "onb_p2_osm_levels"), ("p2_osm", "onb_p2_osm_search"),
    ("p3_landing", "onb_p3_landing"), ("p3_upload", "onb_p3_upload"),
    ("p3_preview", "onb_p3_preview"),
    ("p4_landing", "onb_p4_landing"), ("p4_generate", "onb_p4_landing"),
    ("p4_preview", "onb_p4_preview"), ("p4_confirm", "onb_p4_preview"),
    ("complete_summary", "onb_done"),
    # employee UI (before the configurator markers they collide with)
    ("employee_signin", "emp_login"), ("employee_city", "emp_login"),
    ("employee_home", "emp_home"),
    ("inbox_v2", "emp_inbox_v2"), ("inbox_v1", "emp_inbox_v1"),
    ("complaint_detail", "emp_detail"), ("complaint_workflow", "emp_detail"),
    ("create_complaint", "emp_new"), ("dropdown_", "emp_new"),
    ("search_complaint", "emp_search"),
    # configurator sign-in + console
    ("signin", "login"),
    ("dashboard_home", "mgmt_home"), ("advanced", "mgmt_advanced"),
    ("public_dashboard", "public_dash"),
    ("tenants_list", "tenants"), ("boundary_hierarchies", "bnd_hier"),
    ("map_configuration", "map_config"),
    ("complaint_types", "complaint_types"), ("complaint_hierarchies", "complaint_hier"),
    ("complaints_list", "complaints"),
    ("localization_bulk", "loc_bulk"), ("localization_messages", "localization"),
    ("department_create", "dept_create"), ("departments_", "departments"),
    ("designations_", "designations"),
    ("employees_bulk", "emp_bulk"), ("employee_create", "emp_create"),
    ("employees_", "employees"),
    ("org_chart", "org_chart"), ("users_", "users"),
    ("access_roles", "access_roles"), ("workflows", "workflows"),
    ("processes_list", "processes"), ("mdms_schemas", "mdms_schemas"),
    ("boundary_create", "bnd_create"), ("boundaries_", "boundaries"),
    ("notification_configure", "notif_configure"), ("notification_routing", "notif_routing"),
    ("notification_templates", "notif_templates"),
    ("provider_templates", "notif_provtpl"),
    ("notification_logs", "notif_logs"), ("notification_providers", "notif_providers"),
    ("user_preferences", "notif_prefs"),
]


def classify(flow, fn):
    f = fn.lower()
    for marker, node in MARKERS:
        if marker in f:
            return node
    print(f"  [unclassified] {flow}/{fn}")
    return None


# vis-network draws an image node at a fixed WIDTH and lets the height follow
# the image's aspect ratio. A full-page screenshot of a long wizard screen is
# several thousand pixels tall, so its node grows into a sliver that overlaps
# the rows above and below. Give the graph short, top-cropped thumbnails; the
# lightbox keeps reading the full-resolution shots (a separate field).
THUMB_W, THUMB_RATIO = 400, 10 / 16


def make_thumbs(node_images) -> None:
    from PIL import Image
    made = 0
    for rel in sorted(node_images):
        src = OUT / rel
        dst = OUT / "_thumbs" / rel
        if not src.exists():
            continue
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(src).convert("RGB")
        keep = min(im.height, int(im.width * THUMB_RATIO))
        im = im.crop((0, 0, im.width, keep))
        im.thumbnail((THUMB_W, THUMB_W), Image.LANCZOS)
        im.save(dst, "PNG", optimize=True)
        made += 1
    print(f"_thumbs: {made} regenerated, {len(node_images)} node images")


def use_thumbs_in(pages) -> None:
    old = 'function imgFor(n){ return n.imgs[lang] || GRAY; }'
    new = 'function imgFor(n){ const p=n.imgs[lang]; return p ? "_thumbs/"+p : GRAY; }'
    for page in pages:
        f = OUT / page
        t = f.read_text()
        if old not in t:
            print(f"!! {page}: imgFor() not found — node images left uncropped")
            continue
        f.write_text(t.replace(old, new))


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
    import json
    assets = json.loads((OUT / "node_assets.json").read_text())
    make_thumbs({a["en"][0] for a in assets.values() if a.get("en")})
    use_thumbs_in(("index.html", "sitemap.html"))

    build_flow_gallery(
        OUT, FLOWS, langs=(("en", "EN"),),
        title="DIGIT Configurator & Employee UI — bomet walkthrough",
        intro=("Read-only capture of bometfeedbackhub.digit.org: the configurator's 4-phase "
               "onboarding wizard walked screen by screen, the management console, and the "
               "digit-ui employee app."),
        links=[("index.html", "&#9783; Open the sitemap graph &rarr;")],
        footer=("Click any screenshot to zoom · captured read-only as ADMIN on tenant ke — "
                "no record was created, updated or deleted."),
        accent="#2f6fdb",
    )
    shots = sorted(Path(OUT, "en").glob("*/*.png"))
    build_composite(shots, Path(OUT, "_graph_all.png"),
                    title="DIGIT Configurator + Employee UI — bomet walkthrough", cols=6, thumb_w=420)
    print(f"_graph_all.png: {len(shots)} shots composited")
