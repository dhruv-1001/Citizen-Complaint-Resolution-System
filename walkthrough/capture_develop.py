#!/usr/bin/env python3
"""Capture the develop-branch UI on the develop deployment (https://141.94.92.163.nip.io).

Unlike bomet, this deployment signs in through Keycloak + the Identity BFF, so
the capture needs a Keycloak account, not a DIGIT one:

    WT_KC_EMAIL=you@example.com WT_KC_PASS=... .venv/bin/python capture_develop.py

READ-ONLY. The onboarding writes (sign-up, Branding -> Complaints Template)
were done once, by hand-driven clicks, and their screenshots are imported by
`import_develop_run.py`; this script only revisits finished screens and the
management console, behind the same request guard as the bomet capture.

Run one flow with:  .venv/bin/python capture_develop.py d09_manage
"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright
from playwright_scraper import Walker
from lib import (HOST, VIEWPORT, OUT, goto, install_readonly_guard, write_guard_log,
                 dismiss_overlays)

CONF = f"{HOST}/configurator"
EMAIL = os.environ.get("WT_KC_EMAIL", "")
PASS = os.environ.get("WT_KC_PASS", "")
WORKSPACE = os.environ.get("WT_KC_WORKSPACE", "Cidade de Maputo")
SLUG = os.environ.get("WT_KC_SLUG", "kd")         # tenant slug for /<slug>/digit-ui
EN = OUT / "en"


BROKEN_IMGS = "() => [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src).map(i => i.src)"


async def images_ready(page, *, timeout_ms: int = 10000) -> None:
    """Wait for every <img> to finish; reload once if any is broken.

    The workspace logo comes from filestore and can land after the page has
    otherwise settled — a screenshot taken then shows a broken-image icon.
    """
    for attempt in range(2):
        try:
            await page.wait_for_function("() => [...document.images].every(i => i.complete)", timeout=timeout_ms)
        except Exception:
            pass
        broken = await page.evaluate(BROKEN_IMGS)
        if not broken:
            return
        print(f"[images] broken on {page.url}: {broken[:2]} — reloading")
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
    raise RuntimeError(f"images still broken on {page.url}: {broken[:2]}")


async def kc_login(page, w=None):
    """Keycloak is username-first: email -> Sign In -> password -> Sign In -> workspace."""
    await goto(page, f"{CONF}/", wait_ms=4000)
    if not await page.locator("button:has-text('Log in')").count():
        await choose_workspace(page)
        print(f"[kc login] already signed in -> {page.url}")      # earlier flow or WT_STORAGE_STATE
        return
    if not (EMAIL and PASS):
        raise RuntimeError("not signed in: set WT_KC_EMAIL + WT_KC_PASS, or WT_STORAGE_STATE")
    await page.click("button:has-text('Log in')")
    await page.wait_for_selector("#username", timeout=30000)
    await page.fill("#username", EMAIL)
    await page.click("#kc-login")
    await page.wait_for_selector("#password", timeout=30000)
    if w:
        await w.shot("keycloak_password_step", full_page=False)
    await page.fill("#password", PASS)                 # never smart_fill a password
    await page.click("#kc-login")
    await page.wait_for_timeout(6000)
    await choose_workspace(page, w)
    print(f"[kc login] -> {page.url}")


async def choose_workspace(page, w=None):
    """Pick WORKSPACE on the chooser, if it is showing. The entry is not always a
    <button> (its markup differs between the sign-up and the sign-in chooser),
    so match on its text and then require that we actually left the chooser."""
    if "Choose a workspace" not in await page.inner_text("body"):
        return
    if w:
        await w.shot("choose_workspace", full_page=False)
    await page.get_by_text(WORKSPACE, exact=True).first.click()
    await page.wait_for_timeout(8000)
    if "Choose a workspace" in await page.inner_text("body"):
        raise RuntimeError(f"still on the workspace chooser after picking {WORKSPACE!r}")


# --------------------------------------------------------------------- flows

async def d01_signin(browser):
    """The pre-sign-in surfaces, from a clean browser. Nothing is submitted."""
    ctx = await browser.new_context(viewport=VIEWPORT, ignore_https_errors=True)
    await install_readonly_guard(ctx)
    page = await ctx.new_page()
    w = Walker(page, EN / "d01_signin")
    await goto(page, f"{CONF}/", wait_ms=4000)
    await w.shot("configurator_landing", full_page=False)
    await page.click("button:has-text('Log in')")
    await page.wait_for_selector("#username", timeout=30000)
    await w.shot("keycloak_email_step", full_page=False)
    if EMAIL:
        await page.fill("#username", EMAIL)
        await page.click("#kc-login")
        await page.wait_for_selector("#password", timeout=30000)
        await w.shot("keycloak_password_step", full_page=False)
    await goto(page, f"{CONF}/", wait_ms=4000)
    await page.click("text=Set up or reset your password")
    await page.wait_for_timeout(5000)          # the brand panel's quote fades in; don't catch it mid-fade
    await w.shot("password_setup_link_form", full_page=False)
    await goto(page, f"{CONF}/signup", wait_ms=4000)
    await w.shot("signup_blank", full_page=False)
    await ctx.close()


ACCOUNT_PAGES = [
    ("/account", "your_account"),
    ("/members", "members"),
    ("/workspace-settings", "workspace_settings"),
]


async def d08_account(ctx):
    """The account menu and its three pages. Once onboarding is finished the
    /onboarding/* routes redirect to the console, so there is no "finished
    steps" view any more; these are what an admin reaches from the header."""
    page = await ctx.new_page()
    await kc_login(page)
    w = Walker(page, EN / "d08_account")
    await goto(page, f"{CONF}/manage", wait_ms=5000)
    await page.locator("button[aria-haspopup=menu]").last.click()
    await page.wait_for_timeout(1200)
    await w.shot("account_menu", full_page=False)
    await page.keyboard.press("Escape")
    for path, label in ACCOUNT_PAGES:
        await goto(page, f"{CONF}{path}", wait_ms=5000)
        await dismiss_overlays(page)
        await images_ready(page)
        await w.shot(label)
    await page.close()


# The develop route table (configurator/src/admin/navGroups.ts).
MANAGE = [
    ("/manage", "dashboard_home"),
    ("/manage/public-dashboard", "public_dashboard"),
    ("/manage/branding", "branding"),
    ("/manage/tenants", "tenants"),
    ("/manage/departments", "departments"),
    ("/manage/designations", "designations"),
    ("/manage/boundary-hierarchies", "boundary_hierarchies"),
    ("/manage/boundaries", "boundaries"),
    ("/manage/map-config", "map_configuration"),
    ("/manage/complaints", "complaints"),
    ("/manage/complaint-hierarchy", "complaint_types"),
    ("/manage/complaint-hierarchies", "complaint_hierarchies"),
    ("/manage/escalation-policy", "escalation_policy"),
    ("/manage/localization", "localization"),
    ("/manage/employees", "employees"),
    ("/manage/org-chart", "org_chart"),
    ("/manage/users", "users"),
    ("/manage/access-roles", "access_roles"),
    ("/manage/workflow-business-services", "workflows"),
    ("/manage/workflow-processes", "processes"),
    ("/manage/mdms-schemas", "mdms_schemas"),
    ("/manage/analytics-providers", "analytics_providers"),
    ("/manage/notification-configure", "notification_configure"),
    ("/manage/notifications-channel", "notification_channels"),
    ("/manage/notifications-event-catalogue", "notification_event_catalogue"),
    ("/manage/notifications-routing", "notification_routing"),
    ("/manage/notifications-template", "notification_templates"),
    ("/manage/notifications-provider-template", "notification_provider_templates"),
    ("/manage/notification-provider", "notification_providers"),
    ("/manage/notification-log", "notification_logs"),
    ("/manage/notification-preference", "notification_preferences"),
    ("/manage/advanced", "advanced_all_masters"),
]


async def d09_manage(ctx):
    """Every console route as the founder sees it, with the API status codes behind it."""
    page = await ctx.new_page()
    await kc_login(page)
    w = Walker(page, EN / "d09_manage")
    statuses: dict[str, list[int]] = {}
    current = {"label": None}

    def on_resp(r):
        if current["label"] and r.request.resource_type in ("xhr", "fetch") \
                and "sentry" not in r.url and "posthog" not in r.url and "/identity/" not in r.url:
            statuses.setdefault(current["label"], []).append(r.status)
    page.on("response", on_resp)

    for path, label in MANAGE:
        current["label"] = label
        await goto(page, f"{CONF}{path}", wait_ms=5000)
        await dismiss_overlays(page)
        if "Choose a workspace" in await page.inner_text("body"):
            raise RuntimeError(f"{path} rendered the workspace chooser, not the console")
        if "/configurator/manage" not in page.url:      # e.g. still in Onboarding mode
            await page.get_by_text("Go to Management").first.click()
            await page.wait_for_timeout(4000)
            await goto(page, f"{CONF}{path}", wait_ms=5000)
            if "/configurator/manage" not in page.url:
                raise RuntimeError(f"{path} redirected to {page.url}")
        await images_ready(page)
        await w.shot(label)
    current["label"] = None
    summary = {lbl: {"requests": len(s), "denied": sum(1 for x in s if x in (401, 403)),
                     "errors": sum(1 for x in s if x >= 500)} for lbl, s in statuses.items()}
    (EN / "d09_manage" / "_api_status.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=1))
    await page.close()


async def d10_apps(browser):
    """The employee and citizen apps and the public dashboard, unauthenticated."""
    ctx = await browser.new_context(viewport=VIEWPORT, ignore_https_errors=True)
    await install_readonly_guard(ctx)
    page = await ctx.new_page()
    w = Walker(page, EN / "d10_apps")
    # The employee app (/<slug>/digit-ui/employee) renders blank and the public
    # dashboard URL is a 404 on this vhost; both are described in the doc's
    # findings rather than pictured.
    for url, label in [
        (f"{HOST}/citizen/", "citizen_signin"),
    ]:
        await goto(page, url, wait_ms=9000)
        await w.shot(label, full_page=False)
    await ctx.close()


FLOWS_BROWSER = {"d01_signin": d01_signin, "d10_apps": d10_apps}
FLOWS_CTX = {"d08_account": d08_account, "d09_manage": d09_manage}
DEFAULT = ["d01_signin", "d08_account", "d09_manage"]      # configurator only


async def main():
    want = sys.argv[1:] or DEFAULT
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # WT_STORAGE_STATE: a saved signed-in session — a magic-link account has no password.
        state = os.environ.get("WT_STORAGE_STATE") or None
        ctx = await browser.new_context(viewport=VIEWPORT, ignore_https_errors=True, storage_state=state)
        await install_readonly_guard(ctx)
        for name in want:
            print(f"\n########## {name}")
            try:
                if name in FLOWS_BROWSER:
                    await FLOWS_BROWSER[name](browser)
                else:
                    await FLOWS_CTX[name](ctx)
            except Exception as e:
                print(f"!! flow {name} failed: {type(e).__name__}: {str(e)[:300]}")
        await browser.close()
    write_guard_log()


asyncio.run(main())
