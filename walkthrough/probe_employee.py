"""Probe employee-UI routes and record what each renders."""
import asyncio, json
from playwright.async_api import async_playwright
from lib import EMPLOYEE, VIEWPORT, OUT, goto, install_readonly_guard, employee_login

ROUTES = ["", "/pgr/inbox-v2", "/pgr/inbox", "/pgr/complaint/create", "/pgr/response",
          "/dss/home", "/dss/landing/PGR", "/hrms/inbox", "/workbench/mdms-search"]

async def main():
    res = {}
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True); ctx=await b.new_context(viewport=VIEWPORT)
        await install_readonly_guard(ctx); page=await ctx.new_page()
        page.on("pageerror", lambda e: print("[pageerror]", str(e)[:110]))
        await employee_login(page, shots=False)
        (OUT/"_recon").mkdir(parents=True, exist_ok=True)
        for r in ROUTES:
            try:
                await goto(page, f"{EMPLOYEE}{r}", wait_ms=6000)
                t = await page.evaluate("()=>document.body.innerText.replace(/\\n{2,}/g,'\\n')")
                rows = await page.evaluate("()=>document.querySelectorAll('table tbody tr').length")
                res[r] = {"url": page.url, "rows": rows, "head": t[:260].replace("\n"," | ")}
                print(f"\n--- {r or '/'}  url={page.url}  rows={rows}\n{t[:400]}")
                await page.screenshot(path=str(OUT/"_recon"/f"emp{r.replace('/','_') or '_home'}.png"), full_page=True)
            except Exception as e:
                res[r]={"err":str(e)[:100]}; print(f"--- {r} FAIL {str(e)[:100]}")
        (OUT/"_recon"/"employee_routes.json").write_text(json.dumps(res,indent=2))
        await b.close()
asyncio.run(main())
