"""Visit every management route once and record whether it renders data,
an error state, or an empty state. Drives what the capture is worth doing."""
import asyncio, json
from playwright.async_api import async_playwright
from lib import CONFIGURATOR, VIEWPORT, OUT, goto, login, install_readonly_guard

ROUTES = ["/manage","/manage/advanced","/manage/pgr-dashboard","/manage/public-dashboard",
 "/manage/notification-configure","/manage/notification-routing","/manage/notification-template",
 "/manage/notification-provider-template","/manage/notification-log","/manage/notification-provider",
 "/manage/notification-preference","/manage/tenants","/manage/departments","/manage/designations",
 "/manage/boundary-hierarchies","/manage/map-config","/manage/complaint-hierarchies",
 "/manage/complaint-hierarchy","/manage/complaints","/manage/localization","/manage/employees",
 "/manage/org-chart","/manage/users","/manage/access-roles","/manage/workflow-business-services",
 "/manage/workflow-processes","/manage/mdms-schemas","/manage/boundaries",
 "/manage/employees/bulk","/manage/departments/bulk","/manage/designations/bulk","/manage/localization/bulk"]

async def main():
    res={}
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True); ctx=await b.new_context(viewport=VIEWPORT)
        await install_readonly_guard(ctx); page=await ctx.new_page()
        await login(page, shots=False, mode="management")
        for r in ROUTES:
            try:
                await goto(page, f"{CONFIGURATOR}{r}", wait_ms=3500)
                t = await page.evaluate("()=>document.body.innerText")
                rows = await page.evaluate("()=>document.querySelectorAll('table tbody tr').length")
                state = ("ERROR" if "Error loading data" in t else
                         "EMPTY" if ("No records" in t or "No data" in t or "no results" in t.lower()) else
                         f"OK rows={rows}")
                res[r]=state
                print(f"{r:44} {state}")
            except Exception as e:
                res[r]=f"FAIL {str(e)[:60]}"; print(f"{r:44} FAIL {str(e)[:60]}")
        await b.close()
    (OUT/"_recon").mkdir(parents=True, exist_ok=True)
    (OUT/"_recon"/"route_states.json").write_text(json.dumps(res, indent=2))
asyncio.run(main())
