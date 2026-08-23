#!/usr/bin/env python3
"""Capture the digit-ui employee app on bometfeedbackhub.digit.org.

READ-ONLY, same contract as capture_configurator.py: the New Complaint wizard
is filled in but SUBMIT is never clicked, and `lib.install_readonly_guard`
aborts anything that would write.

What bomet actually serves: PGR only. /dss/*, /hrms/* and /workbench/* all fall
back to the home screen — those modules are not enabled on this deployment (see
output/_recon/employee_routes.json). The deployment now carries real complaints,
so the inbox opens onto a complaint detail + workflow timeline; opening one is a
read, and none of the action buttons on it are ever clicked.
"""
import asyncio, sys
from playwright.async_api import async_playwright
from playwright_scraper import Walker
from lib import (EMPLOYEE, VIEWPORT, OUT, goto, employee_login,
                 install_readonly_guard, write_guard_log)


async def f14_login(ctx):
    page = await ctx.new_page()
    page.on("pageerror", lambda e: print(f"[pageerror] {str(e)[:140]}"))
    w = Walker(page, OUT / "en" / "14_employee_login")
    await employee_login(page, w, shots=True)
    await w.shot("employee_home")
    return page


async def f15_inbox(ctx, page=None):
    page = page or await ctx.new_page()
    if "/user/login" in page.url or page.url.rstrip("/").endswith("/employee") is False:
        pass
    w = Walker(page, OUT / "en" / "15_employee_inbox")
    await goto(page, f"{EMPLOYEE}/pgr/inbox-v2", wait_ms=7000)
    await w.shot("inbox_v2_my_complaints")

    # The inbox opens on "My Complaints", which is empty for ADMIN — the
    # deployment's 5k complaints are owned by other employees. "All Complaints"
    # is the tab with rows; switching tabs only re-runs `_search`.
    if await switch_to_all_complaints(page):
        await w.shot("inbox_v2_all_complaints")

    await goto(page, f"{EMPLOYEE}/pgr/inbox", wait_ms=6000)
    await w.shot("inbox_v1_legacy")
    return page


async def switch_to_all_complaints(page) -> bool:
    try:
        await page.get_by_text("All Complaints", exact=True).first.click(timeout=8000)
        await page.wait_for_timeout(6000)
        return True
    except Exception as e:
        print(f"[skip] All Complaints tab: {str(e)[:90]}")
        return False


async def f16_complaint_detail(ctx, page=None):
    """Open one complaint from the inbox: detail card + workflow timeline."""
    page = page or await ctx.new_page()
    w = Walker(page, OUT / "en" / "16_employee_complaint_detail")
    await goto(page, f"{EMPLOYEE}/pgr/inbox-v2", wait_ms=8000)
    await switch_to_all_complaints(page)
    # rows are div-based; the complaint number is the only link out
    rows = page.locator("a[href*='/pgr/complaint-details/']")
    try:
        if not await rows.count():
            print("[skip] no complaint row to open")
            return page
        await rows.first.click(timeout=8000)
        await page.wait_for_timeout(7000)
    except Exception as e:
        print(f"[skip] opening complaint: {str(e)[:90]}")
        return page
    await w.shot("complaint_detail")
    # the workflow history sits below the fold on a 900px viewport
    await page.mouse.wheel(0, 1600)
    await page.wait_for_timeout(1500)
    await w.shot("complaint_workflow_timeline")
    return page


async def f17_new_complaint(ctx, page=None):
    page = page or await ctx.new_page()
    w = Walker(page, OUT / "en" / "17_employee_new_complaint")
    await goto(page, f"{EMPLOYEE}/pgr/create-complaint", wait_ms=7000)
    await w.shot("create_complaint_blank")

    await w.smart_fill(overrides={"phone": "712345678", "name": "Demo Complainant",
                                  "description": "Captured for the walkthrough — never submitted"})
    await page.wait_for_timeout(600)

    # the cascading Category -> Sub-Type selects are custom dropdowns
    for label in ("Select Category", "Select County"):
        try:
            await page.get_by_text(label, exact=True).first.click(timeout=5000)
            await page.wait_for_timeout(1200)
            await w.shot(f"dropdown_{label.split()[-1].lower()}_open")
            opt = page.locator("li[role=option], [role=option]").first
            if await opt.count():
                await opt.click(timeout=4000)
                await page.wait_for_timeout(1200)
        except Exception as e:
            print(f"[skip] {label}: {str(e)[:90]}")

    await w.shot("create_complaint_filled_not_submitted")
    return page


async def f18_home_cards(ctx, page=None):
    page = page or await ctx.new_page()
    w = Walker(page, OUT / "en" / "18_employee_search")
    await goto(page, EMPLOYEE, wait_ms=6000)
    try:
        await page.get_by_text("Search Complaint", exact=True).first.click(timeout=8000)
        await page.wait_for_timeout(6000)
        await w.shot("search_complaint_entry")
    except Exception as e:
        print(f"[skip] search card: {str(e)[:90]}")
    return page


FLOWS = {"14_employee_login": f14_login, "15_employee_inbox": f15_inbox,
         "16_employee_complaint_detail": f16_complaint_detail,
         "17_employee_new_complaint": f17_new_complaint,
         "18_employee_search": f18_home_cards}


async def main():
    want = sys.argv[1:] or list(FLOWS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport=VIEWPORT)
        await install_readonly_guard(ctx)
        page = None
        for name in want:
            print(f"\n########## {name}")
            try:
                if name == "14_employee_login":
                    page = await FLOWS[name](ctx)
                else:
                    if page is None:          # flows after login reuse the session
                        page = await ctx.new_page()
                        page.on("pageerror", lambda e: print(f"[pageerror] {str(e)[:140]}"))
                        await employee_login(page, shots=False)
                    page = await FLOWS[name](ctx, page)
            except Exception as e:
                print(f"!! flow {name} failed: {type(e).__name__}: {str(e)[:300]}")
        await browser.close()
    write_guard_log()


asyncio.run(main())
