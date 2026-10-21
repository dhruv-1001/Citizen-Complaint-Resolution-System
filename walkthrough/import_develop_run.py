#!/usr/bin/env python3
"""Import the screenshots of the onboarding run into output-develop/.

The sign-up and the five onboarding steps WRITE (a Keycloak user, a tenant,
boundaries, departments, employees, complaint types), so they are driven once,
step by step, against a throwaway workspace — on 2026-10-21 against the local
develop stack (develop f713f9e6c) — not by a re-runnable capture. This script
copies the chosen screenshots into numbered flow directories so build_site /
build_doc_develop treat them like any other capture.

    .venv/bin/python import_develop_run.py /path/to/run/shots
"""
import shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EN = HERE / "output-develop" / "en"

# flow -> [(source file in the run's shots dir, label)]
RUN = {
    "d02_signup": [
        ("a03_signup_filled.png", "signup_filled"),
        ("a04_check_email.png", "signup_check_email"),
        ("a06_account_verified.png", "account_email_verified"),
        ("a07_account_name_code.png", "account_name_and_code"),
        ("a08_preferences_blank.png", "preferences_blank"),
        ("a09_preferences_mozambique.png", "preferences_mozambique_defaults"),
        ("a10_preferences_filled.png", "preferences_filled"),
        ("a11_review.png", "review"),
        ("a12_provisioning.png", "provisioning"),
    ],
    "d02b_home": [
        ("a13_tour_1.png", "tour_1_what_onboarding_is"),
        ("a13_tour_2.png", "tour_2_complaints_template"),
        ("a13_tour_3.png", "tour_3_branding"),
        ("a13_tour_4.png", "tour_4_geography"),
        ("a13_tour_5.png", "tour_5_departments_employees"),
        ("a13_tour_6.png", "tour_6_reopen"),
        ("a14_onboarding_home.png", "onboarding_home"),
    ],
    "d03_branding": [
        ("b01_branding_blank.png", "branding_blank"),
        ("b02_branding_logo_uploaded.png", "branding_logo_uploaded"),
        ("b03_branding_green_and_gold.png", "branding_green_and_gold"),
    ],
    "d04_geography": [
        ("c01_geography_landing.png", "geography_choose_source"),
        ("c02_fetch_search.png", "fetch_boundaries"),
        ("c03_fetch_source_options.png", "boundary_source_options"),
        ("c04_fetch_suggestions.png", "fetch_suggestions"),
        ("c05_fetch_levels.png", "fetch_map_admin_levels"),
        ("c06_excel_landing.png", "excel_define_hierarchy"),
    ],
    "d04b_preconfigured": [
        ("d01_preconf_search.png", "preconfigured_search"),
        ("d02_preconf_suggestions.png", "preconfigured_suggestions"),
        ("d03_preconf_levels.png", "preconfigured_levels"),
        ("d04_preconf_per_level.png", "per_level_confidence"),
        ("d05_preconf_levels_named.png", "levels_named"),
        ("d06_boundaries_created.png", "boundaries_created"),
        ("d07_geography_with_hierarchy.png", "geography_with_hierarchy"),
    ],
    "d05_departments": [
        ("e01_departments_landing.png", "departments_landing"),
        ("e02_departments_upload.png", "departments_upload"),
        ("e03_add_department.png", "add_department"),
        ("e04_add_designation.png", "add_designation"),
        ("e05_departments_filled.png", "departments_filled"),
    ],
    "d06_employees": [
        ("f01_employees_landing.png", "employees_landing"),
        ("f02_employees_upload.png", "employees_upload"),
        ("f04_employee_form_filled.png", "employee_form_filled"),
        ("f05_employees_list.png", "employees_list"),
    ],
    "d07_complaints": [
        ("g01_complaints_landing.png", "complaints_landing"),
        ("g02_complaints_upload.png", "complaints_upload"),
        ("g03_add_category.png", "add_category"),
        ("g04_categories_added.png", "categories_added"),
        ("g05_default_resolution_time.png", "default_resolution_time"),
    ],
}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__); return 2
    src = Path(sys.argv[1])
    missing = 0
    for flow, shots in RUN.items():
        d = EN / flow
        shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
        for i, (name, label) in enumerate(shots, 1):
            f = src / name
            if not f.exists():
                print(f"!! missing {f}"); missing += 1; continue
            shutil.copy2(f, d / f"{i:02d}_{label}.png")
        print(f"{flow}: {len(shots)} shots")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
