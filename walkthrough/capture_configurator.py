#!/usr/bin/env python3
"""Capture the DIGIT configurator on bometfeedbackhub.digit.org.

Sign-in plus the management console. The 4-phase onboarding wizard lives in
`capture_onboarding.py`.

READ-ONLY. Every screen is reached by direct URL navigation (the route table is
`configurator/src/admin/DigitLayout.tsx`), create/edit forms are screenshotted
blank and smart-filled but NEVER submitted, and `lib.install_readonly_guard`
aborts any request that would mutate the deployment.

Run one flow at a time with:  python3 capture_configurator.py 08_tenant
"""
import asyncio, sys
from playwright.async_api import async_playwright
from playwright_scraper import Walker
from lib import (CONFIGURATOR, VIEWPORT, OUT, TENANT, goto, login,
                 install_readonly_guard, write_guard_log, dismiss_overlays)

SETTLE = 3200          # react-admin lists fetch after mount; give them time


async def screen(w, path, label, *, settle=SETTLE):
    """Navigate to a configurator route and shoot it."""
    await goto(w.page, f"{CONFIGURATOR}{path}", wait_ms=settle)
    await dismiss_overlays(w.page)
    await w.shot(label)


async def open_first_row(w, label, *, settle=2800):
    """Click into the first list row to capture a detail/show screen."""
    page = w.page
    try:                       # the datagrid fetches after mount
        await page.wait_for_selector("table tbody tr", state="visible", timeout=12000)
    except Exception:
        pass
    for sel in ("table tbody tr", "[role=row]:not(:first-child)", "[data-testid=row]"):
        rows = page.locator(sel)
        try:
            if await rows.count() > 1 or (await rows.count() == 1 and sel != "[role=row]:not(:first-child)"):
                before = page.url
                await rows.first.click(timeout=4000)
                await page.wait_for_timeout(settle)
                if page.url != before:
                    await dismiss_overlays(page)
                    await w.shot(label)
                    return True
        except Exception:
            continue
    print(f"[skip] no clickable row for {label}")
    return False


async def form(w, path, label, *, fill=True):
    """Blank + smart-filled shot of a create form. Never submitted."""
    await screen(w, path, f"{label}_blank")
    if fill:
        try:
            await w.smart_fill(overrides={"tenant": TENANT, "code": "DEMO_ONLY",
                                          "name": "Demo (not saved)"})
            await w.page.wait_for_timeout(700)
            await w.shot(f"{label}_filled")
        except Exception as e:
            print(f"[fill skip] {label}: {str(e)[:80]}")


# --------------------------------------------------------------------- flows

async def f01_login(ctx):
    page = await ctx.new_page()
    w = Walker(page, OUT / "en" / "01_login")
    await goto(page, f"{CONFIGURATOR}/login", wait_ms=2500)
    await w.shot("signin_blank")
    await page.click("button:has-text('Onboarding')")
    await page.fill("#username", "ADMIN"); await page.fill("#password", "eGov@123")
    await page.fill("#tenantCode", TENANT)
    await w.shot("signin_filled_onboarding_mode")
    await page.click("button:has-text('Management')")
    await w.shot("signin_filled_management_mode")
    await page.close()


async def f07_home(ctx):
    page = await ctx.new_page(); await install_page_hooks(page)
    await login(page, shots=False, mode="management")
    w = Walker(page, OUT / "en" / "07_home")
    await screen(w, "/manage", "dashboard_home", settle=4500)
    await screen(w, "/manage/advanced", "advanced_all_masters", settle=4000)
    await page.close()


# Route -> (label, capture a detail row?)  ------------------------------------
# Reflects what bometfeedbackhub.digit.org actually renders: see
# `probe_routes.py` / output/_recon/route_states.json. The seven MDMS-backed
# lists that used to 500 here (Departments, Designations, Complaint Types,
# Complaint Hierarchies, Map Configuration, Notification Routing, Provider
# Templates) load since the deployment picked up an egov-mdms image that serves
# `v2/_count`, so they sit in their natural sections again instead of in a
# separate "known gaps" flow.
MANAGE_FLOWS = {
    "08_tenant": [
        ("/manage/tenants", "tenants_list", None),
        ("/manage/boundary-hierarchies", "boundary_hierarchies_list", "row"),
        ("/manage/boundaries", "boundaries_list", "row"),
        ("/manage/map-config", "map_configuration", None),
    ],
    "09_complaints": [
        ("/manage/complaints", "complaints_list", None),
        ("/manage/complaint-hierarchy", "complaint_types_list", "row"),
        ("/manage/complaint-hierarchies", "complaint_hierarchies_list", "row"),
        ("/manage/localization", "localization_messages_list", "row"),
    ],
    "10_people": [
        ("/manage/departments", "departments_list", "row"),
        ("/manage/designations", "designations_list", "row"),
        ("/manage/employees", "employees_list", "row"),
        ("/manage/org-chart", "org_chart", None),
        ("/manage/users", "users_list", "row"),
        ("/manage/employees/bulk", "employees_bulk_import", None),
        ("/manage/localization/bulk", "localization_bulk_import", None),
    ],
    "11_system": [
        ("/manage/access-roles", "access_roles_list", "row"),
        ("/manage/workflow-business-services", "workflows_list", "row"),
        ("/manage/workflow-processes", "processes_list", None),
        ("/manage/mdms-schemas", "mdms_schemas_list", "row"),
    ],
    "12_notifications": [
        ("/manage/notification-configure", "notification_configure", None),
        ("/manage/notification-routing", "notification_routing", None),
        ("/manage/notification-template", "notification_templates", None),
        ("/manage/notification-provider-template", "provider_templates_whatsapp", None),
        ("/manage/notification-log", "notification_logs", None),
        ("/manage/notification-provider", "notification_providers", "row"),
        ("/manage/notification-preference", "user_preferences", None),
    ],
    # /manage/pgr-dashboard exists in configurator/src/App.tsx but not in the
    # bundle bomet serves — react-admin falls back to the console home, so
    # capturing it would just duplicate 07_home.
    "13_dashboards": [
        ("/manage/public-dashboard", "public_dashboard_configure", None),
    ],
}

# Create forms: captured blank and smart-filled, NEVER submitted.
CREATE_FORMS = {
    "10_people": [("/manage/departments/create", "department_create"),
                  ("/manage/employees/create", "employee_create")],
    "08_tenant": [("/manage/boundaries/create", "boundary_create")],
}


async def manage_flow(ctx, flow):
    page = await ctx.new_page(); await install_page_hooks(page)
    await login(page, shots=False, mode="management")
    w = Walker(page, OUT / "en" / flow)
    for path, label, detail in MANAGE_FLOWS[flow]:
        settle = 5000 if "dashboard" in label or "org_chart" in label else SETTLE
        await screen(w, path, label, settle=settle)
        if detail == "row":
            await open_first_row(w, label.replace("_list", "") + "_detail")
    for path, label in CREATE_FORMS.get(flow, []):
        await form(w, path, label)
    await page.close()


async def install_page_hooks(page):
    page.on("pageerror", lambda e: print(f"[pageerror] {str(e)[:160]}"))


FLOWS = {
    "01_login": f01_login,
    "07_home": f07_home,
    **{k: (lambda ctx, k=k: manage_flow(ctx, k)) for k in MANAGE_FLOWS},
}


async def main():
    want = sys.argv[1:] or list(FLOWS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport=VIEWPORT, ignore_https_errors=True)
        await install_readonly_guard(ctx)
        for name in want:
            print(f"\n########## {name}")
            try:
                await FLOWS[name](ctx)
            except Exception as e:
                print(f"!! flow {name} failed: {type(e).__name__}: {str(e)[:300]}")
        await browser.close()
    write_guard_log()


asyncio.run(main())
