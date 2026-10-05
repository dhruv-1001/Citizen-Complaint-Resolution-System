#!/usr/bin/env python3
"""Import the screenshots of the one-off onboarding run into output-develop/.

The sign-up and the five onboarding steps WRITE (a Keycloak user, a tenant,
boundaries, departments, employees, complaint types), so they were driven once,
step by step, on 2026-10-05 — not by a re-runnable capture. Their screenshots
live wherever that run kept them; this script copies the chosen ones into
numbered flow directories so build_site / build_doc_develop treat them like any
other capture.

    .venv/bin/python import_develop_run.py /path/to/run/shots
"""
import shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EN = HERE / "output-develop" / "en"

# flow -> [(source file in the run's shots dir, label)]
RUN = {
    "d02_signup": [
        ("s02_signup_submit_01_signup_filled.png", "signup_filled"),
        ("s02_signup_submit_02_signup_link_sent.png", "signup_check_email"),
        ("s03_mailpit_message.png", "mailpit_signin_link_email"),
        ("s04_account_01_account_blank.png", "account_email_verified"),
        ("s04_account_02_account_filled.png", "account_name_and_code"),
        ("s05_prefs_01_preferences_blank.png", "preferences_blank"),
        ("s06_prefs_fill_01_preferences_country_mozambique.png", "preferences_mozambique_defaults"),
        ("s07_review_01_preferences_filled.png", "preferences_filled"),
        ("s07_review_02_review.png", "review"),
        ("s08_create_02_creating_0.png", "provisioning"),
        ("s10_workspace_01_choose_workspace.png", "choose_workspace"),
    ],
    "d03_branding": [
        ("s11_branding_01_branding_blank.png", "branding_blank"),
        ("s11_branding_02_branding_logo_uploaded.png", "branding_logo_uploaded"),
        ("s11_branding_03_branding_green_gold.png", "branding_green_and_gold"),
    ],
    "d04_geography": [
        ("s12_geo_fetch_01_geography_landing.png", "geography_choose_source"),
        ("s12_geo_fetch_02_fetch_open.png", "fetch_boundaries"),
        ("s13_geo_search_01_source_options_open.png", "boundary_source_options"),
        ("s16_geo_create_01_cod_suggestions.png", "cod_suggestions"),
        ("s16_geo_create_03_cod_map_levels.png", "cod_map_admin_levels"),
        ("s16_geo_create_04_levels_named.png", "levels_named"),
        ("s16_geo_create_07_after_create.png", "boundaries_created"),
        ("s17_geo_save_01_geography_with_hierarchy.png", "geography_with_hierarchy"),
    ],
    "d05_departments": [
        ("s18_dept_forms_01_departments_seeded.png", "departments_seeded"),
        ("s18_dept_forms_04_departments_upload.png", "departments_upload"),
        ("s19_dept_add_01_add_department_filled.png", "add_department"),
        ("s19_dept_add_02_add_designation_filled.png", "add_designation"),
        ("s19_dept_add_03_departments_filled.png", "departments_filled"),
    ],
    "d06_employees": [
        ("s20_dept_save_01_employees_landing.png", "employees_landing"),
        ("s21_emp_form_01_employees_upload.png", "employees_upload"),
        ("s21_emp_form_02_employee_form_blank.png", "employee_form_blank"),
        ("s22_emp_add_01_employee_form_filled.png", "employee_form_filled"),
        ("s22_emp_add_02_employees_list.png", "employees_list"),
        ("s33_relogin_finish_03_employees_list.png", "employees_one_gro_per_department"),
    ],
    "d07_complaints": [
        ("s23_emp_save_01_complaints_landing.png", "complaints_landing"),
        ("s24_cat_form_01_complaints_upload.png", "complaints_upload"),
        ("s25_cat_add_01_category_form_filled.png", "add_category"),
        ("s27_finish_01_complaints_sla_3_days.png", "four_categories_sla_3_days"),
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
