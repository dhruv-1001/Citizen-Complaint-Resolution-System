#!/usr/bin/env python3
"""Reconnaissance: log into both apps and dump their real navigation so the
capture scripts target routes that exist on THIS deployment rather than routes
guessed from the source tree. Kept in the repo for the same reason the upstream
examples keep theirs — re-run it when bomet changes.
"""
import asyncio, json, sys
from playwright.async_api import async_playwright
from lib import (CONFIGURATOR, EMPLOYEE, VIEWPORT, OUT, goto, login,
                 install_readonly_guard, write_guard_log)

RECON = OUT / "_recon"


async def dump(page, name):
    RECON.mkdir(parents=True, exist_ok=True)
    await page.screenshot(path=str(RECON / f"{name}.png"), full_page=True)
    info = await page.evaluate("""() => ({
        url: location.href,
        title: document.title,
        links: [...document.querySelectorAll('a[href]')].map(a => [a.getAttribute('href'), a.innerText.trim().slice(0,60)]),
        buttons: [...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b => b.innerText.trim().slice(0,50)).filter(Boolean),
        text: document.body.innerText.slice(0, 4000),
    })""")
    (RECON / f"{name}.json").write_text(json.dumps(info, indent=2))
    print(f"\n===== {name}  url={info['url']}")
    print("LINKS:", json.dumps(info["links"][:120], indent=1))
    print("BUTTONS:", info["buttons"][:40])
    return info


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport=VIEWPORT)
        await install_readonly_guard(ctx)
        page = await ctx.new_page()
        page.on("pageerror", lambda e: print(f"[pageerror] {e}"))

        await login(page, shots=False, mode="management")
        await dump(page, "01_manage_home")

        # employee UI
        await goto(page, EMPLOYEE, wait_ms=4000)
        await dump(page, "02_employee_login")

        await browser.close()
    write_guard_log()

asyncio.run(main())
