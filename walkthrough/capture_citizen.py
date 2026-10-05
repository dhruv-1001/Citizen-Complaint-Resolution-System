#!/usr/bin/env python3
"""Capture the citizen-facing surfaces: both citizen apps and the public dashboard.

READ-ONLY. Everything here is reachable without signing in. The capture goes up
to each sign-in screen and stops: "Send OTP" would text a real phone number and
create an OTP record, so it is never pressed (the guard would also abort the
`user-otp/v1/_send` call).

    .venv/bin/python capture_citizen.py            # all three flows
"""
import asyncio, sys
from playwright.async_api import async_playwright
from playwright_scraper import Walker
from lib import (HOST, CITIZEN, VIEWPORT, OUT, goto, install_readonly_guard, write_guard_log)


async def f20_citizen_v2(ctx):
    """/citizen — the digit-ui-v2 citizen SPA. Sign-in only without an account."""
    page = await ctx.new_page()
    w = Walker(page, OUT / "en" / "20_citizen_v2")
    await goto(page, f"{HOST}/citizen/", wait_ms=8000)
    await w.shot("citizen_v2_signin", full_page=False)
    try:
        await page.get_by_label("Mobile number").fill("712345678")
    except Exception:
        await page.locator("input[type=tel], input[inputmode=numeric], input").first.fill("712345678")
    await page.wait_for_timeout(600)
    await w.shot("citizen_v2_signin_number_entered_not_sent", full_page=False)
    await page.close()


async def f21_citizen_classic(ctx):
    """/digit-ui/citizen — the classic citizen app in the new shell (#2038), signed out."""
    page = await ctx.new_page()
    w = Walker(page, OUT / "en" / "21_citizen_classic")
    await goto(page, CITIZEN, wait_ms=8000)
    await w.shot("citizen_all_services", full_page=False)
    for text, label in (("File a Complaint", "file_a_complaint_signed_out"),
                        ("My Complaints", "my_complaints_signed_out")):
        await goto(page, CITIZEN, wait_ms=6000)
        try:
            await page.get_by_text(text, exact=True).first.click(timeout=8000)
            await page.wait_for_timeout(6000)
            await w.shot(label, full_page=False)
        except Exception as e:
            print(f"[skip] {text}: {str(e)[:90]}")
    await goto(page, f"{CITIZEN}/login", wait_ms=7000)
    await w.shot("citizen_classic_login", full_page=False)
    await page.close()


async def f22_public_dashboard(ctx):
    """The anonymous public dashboard — what anyone on the internet can see."""
    page = await ctx.new_page()
    w = Walker(page, OUT / "en" / "22_public_dashboard")
    await goto(page, f"{HOST}/digit-ui/public-dashboard", wait_ms=12000)
    await w.shot("public_dashboard_top", full_page=False)
    await w.shot("public_dashboard_full_page")
    try:
        await page.get_by_text("Filters", exact=True).first.click(timeout=5000)
        await page.wait_for_timeout(1500)
        await w.shot("public_dashboard_filters_open", full_page=False)
    except Exception as e:
        print(f"[skip] filters: {str(e)[:90]}")
    await page.close()


FLOWS = {"20_citizen_v2": f20_citizen_v2, "21_citizen_classic": f21_citizen_classic,
         "22_public_dashboard": f22_public_dashboard}


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
