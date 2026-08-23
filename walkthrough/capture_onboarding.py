#!/usr/bin/env python3
"""Capture the configurator's 4-phase onboarding wizard, screen by screen.

Mirrors the "CMS Configurator: Onboarding UI Screens & Windows Inventory"
trigger->opens table: every screen the wizard can reach WITHOUT writing to the
deployment is walked here with real clicks and real workbook uploads.

The write boundary is hard and deliberate:

    reachable read-only          the wizard parses the workbook in the browser,
                                 so landing / upload / preview / verify screens
                                 cost the deployment nothing
    NOT captured                 anything behind "Upload to DIGIT",
                                 "Create Hierarchy", "Upload N Boundaries",
                                 "Create & Continue" or the Create-Employees
                                 confirmation — those POST to DIGIT

`lib.install_readonly_guard` is the safety net underneath, but this script also
simply never clicks those controls. Screens past the boundary are listed in the
walkthrough doc as "not captured", not faked.

Run one flow at a time with:  python3 capture_onboarding.py 03_phase2_boundary
"""
import asyncio, sys
from playwright.async_api import async_playwright
from playwright_scraper import Walker
from lib import (CONFIGURATOR, VIEWPORT, OUT, goto, login, install_readonly_guard,
                 write_guard_log, dismiss_overlays, attach, click_text, has_text,
                 FIX_TENANT, FIX_BOUNDARY, FIX_POLYGON, FIX_MASTERS, FIX_EMPLOYEES)


async def phase(page, w, n, label, *, settle=5000):
    await goto(page, f"{CONFIGURATOR}/phase/{n}", wait_ms=settle)
    await dismiss_overlays(page)
    await w.shot(label)


async def tab(page, name):
    """Click a Radix tab by its accessible name; tolerate the count suffix."""
    try:
        await page.get_by_role("tab", name=name).first.click(timeout=6000)
        await page.wait_for_timeout(1400)
        return True
    except Exception:
        print(f"[tab miss] {name}")
        return False


async def start(ctx, flow):
    page = await ctx.new_page()
    page.on("pageerror", lambda e: print(f"[pageerror] {str(e)[:160]}"))
    await login(page, shots=False, mode="onboarding")
    return page, Walker(page, OUT / "en" / flow)


# ------------------------------------------------------- Phase 1: tenant

async def f_phase1(ctx):
    page, w = await start(ctx, "02_phase1_tenant")
    await phase(page, w, 1, "p1_landing")

    # "Use existing tenant" — the skip-ahead path. Listing tenants is a read;
    # picking one only sets wizard state and jumps to Phase 2.
    if await click_text(page, "Use existing tenant", wait_ms=3200):
        await w.shot("p1_select_existing_tenant")
        await click_text(page, "← Back")

    await click_text(page, "Start Setup", wait_ms=2000)
    await w.shot("p1_upload_tenant_master")

    await attach(page, "#file-upload", FIX_TENANT, wait_ms=3500)
    await w.shot("p1_preview_tenant_info")
    if await tab(page, "Branding Details"):
        await w.shot("p1_preview_branding_details")
    await tab(page, "Tenant Info")

    # "← Change File" goes back to the dropzone; "Upload to DIGIT" would write.
    if await click_text(page, "← Change File"):
        await w.shot("p1_change_file_back_to_upload")
    await page.close()


# ------------------------------------------------------- Phase 2: boundaries

async def f_phase2(ctx):
    page, w = await start(ctx, "03_phase2_boundary")
    await phase(page, w, 2, "p2_landing_choose_source")

    # ---- Excel path
    await click_text(page, "Upload from Excel")
    await w.shot("p2_excel_choose_path")

    await click_text(page, "Option 1: Create New Hierarchy")
    await w.shot("p2_create_hierarchy_blank")
    try:                                   # fill it, never submit it
        await page.locator("input[placeholder='ADMIN']").first.fill("WALKTHROUGH_DEMO")
        levels = page.locator("input[placeholder*='Level'], input[placeholder*='level']")
        for i in range(min(await levels.count(), 3)):
            await levels.nth(i).fill(["County", "Sub-County", "Ward"][i])
        await page.wait_for_timeout(600)
        await w.shot("p2_create_hierarchy_filled")
    except Exception as e:
        print(f"[fill skip] create-hierarchy: {str(e)[:90]}")
    await click_text(page, "← Back")

    await click_text(page, "Option 2: Use Existing Hierarchy", wait_ms=3500)
    await w.shot("p2_select_existing_hierarchy")

    # pick the first hierarchy card, then continue to the template screen
    picked = False
    for sel in ("div:has-text('ADMIN') >> nth=-1", "[class*=cursor-pointer]"):
        try:
            await page.locator(sel).first.click(timeout=4000)
            picked = True
            break
        except Exception:
            continue
    await page.wait_for_timeout(800)
    if picked:
        await w.shot("p2_hierarchy_selected")
    await click_text(page, "Use Selected Hierarchy", wait_ms=3000)
    if await has_text(page, "Boundary Data Upload"):
        await w.shot("p2_download_template")

        await attach(page, "#boundary-file-upload", FIX_BOUNDARY, wait_ms=6000)
        if await has_text(page, "Verify Boundary Data", timeout=8000):
            await w.shot("p2_verify_all")
            if await tab(page, "Valid"):
                await w.shot("p2_verify_valid")
            if await tab(page, "Errors"):
                await w.shot("p2_verify_errors")
            try:                            # the optional GeoJSON sidecar slot
                await attach(page, "#boundary-polygon-upload", FIX_POLYGON, wait_ms=5000)
                await w.shot("p2_verify_with_geojson")
            except Exception as e:
                print(f"[geojson skip] {str(e)[:90]}")
        else:
            await w.shot("p2_boundary_upload_rejected")
    else:
        await w.shot("p2_hierarchy_path_stalled")

    # ---- OSM path (back to the landing, no second shot of it)
    await goto(page, f"{CONFIGURATOR}/phase/2", wait_ms=4000)
    await click_text(page, "Fetch from OpenStreetMap")
    await w.shot("p2_osm_search")
    try:
        await page.locator("input[placeholder*='Maputo']").first.fill("Bomet")
        await page.wait_for_timeout(500)
        await w.shot("p2_osm_search_typed")
        await page.locator("button:has-text('Search')").first.click(timeout=6000)
        await page.wait_for_timeout(30000)          # Nominatim + Overpass are slow
        if await has_text(page, "Create Hierarchy & Boundaries", timeout=15000):
            await w.shot("p2_osm_map_levels")       # STOP: the next click writes
        else:
            await w.shot("p2_osm_search_result")
    except Exception as e:
        print(f"[osm skip] {str(e)[:120]}")
    await page.close()


# ------------------------------------------------------- Phase 3: masters

async def f_phase3(ctx):
    page, w = await start(ctx, "04_phase3_masters")
    await phase(page, w, 3, "p3_landing")
    await click_text(page, "Start Setup", wait_ms=2000)
    await w.shot("p3_upload_common_master")

    await attach(page, "#common-master-upload", FIX_MASTERS, wait_ms=4000)
    await w.shot("p3_preview_departments_designations")
    # "Create & Continue" writes departments + designations — stop here.
    await page.close()


# ------------------------------------------------------- Phase 4: employees

async def f_phase4(ctx):
    page, w = await start(ctx, "05_phase4_employees")
    await phase(page, w, 4, "p4_landing")
    # "Start Phase 4" is disabled={... || !!refsError}. On bomet the reference
    # load reports "No boundaries found for tenant ke", so the template screen
    # is unreachable here — see the walkthrough doc for why that happens.
    if await click_text(page, "Start Phase 4", wait_ms=6000) and await has_text(page, "Download Template"):
        await w.shot("p4_generate_template")
    else:
        print("[blocked] Start Phase 4 disabled — reference data has no boundaries")

    await attach(page, "#employee-file-upload", FIX_EMPLOYEES, wait_ms=6000)
    await w.shot("p4_preview_validation")

    # The Create button only opens a confirmation dialog; the dialog's own
    # button is the one that POSTs. Shoot the dialog, then dismiss it.
    btn = page.locator("button:has-text('Employees')").first
    try:
        if await btn.is_enabled(timeout=4000):
            await btn.click(timeout=6000)
            await page.wait_for_timeout(1500)
            if await page.locator("[role=dialog]").count():
                await w.shot("p4_confirm_dialog")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(800)
        else:
            print("[blocked] Create Employees disabled — 0 valid rows, so the "
                  "confirmation dialog cannot be reached read-only")
    except Exception as e:
        print(f"[dialog skip] {str(e)[:120]}")
    await page.close()


# ------------------------------------------------------- Complete

async def f_complete(ctx):
    page, w = await start(ctx, "06_onboarding_complete")
    await goto(page, f"{CONFIGURATOR}/complete", wait_ms=5000)
    await dismiss_overlays(page)
    await w.shot("complete_summary")
    await page.close()


FLOWS = {
    "02_phase1_tenant": f_phase1,
    "03_phase2_boundary": f_phase2,
    "04_phase3_masters": f_phase3,
    "05_phase4_employees": f_phase4,
    "06_onboarding_complete": f_complete,
}


async def main():
    want = sys.argv[1:] or list(FLOWS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport=VIEWPORT, ignore_https_errors=True,
                                        accept_downloads=False)
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
