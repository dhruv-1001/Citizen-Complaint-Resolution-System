"""Shared helpers for the bomet walkthrough capture.

Two things live here that every capture script needs:

1. `install_readonly_guard()` — a Playwright route handler that aborts any
   request that would MUTATE the deployment. The capture runs against a live
   shared server (bometfeedbackhub.digit.org) as ADMIN, and ADMIN carries
   SUPERUSER + MDMS_ADMIN, so a stray "Save" click would write real config to
   tenant `ke`. The guard is the safety net; the capture scripts additionally
   never click a save/submit control.

2. `login()` — the configurator sign-in, driven explicitly (the password is
   never left to smart_fill).
"""
from __future__ import annotations

import os
from pathlib import Path

HOST = os.environ.get("WT_HOST", "https://bometfeedbackhub.digit.org")
TENANT = os.environ.get("WT_TENANT", "ke")
USERNAME = os.environ.get("WT_USER", "ADMIN")
PASSWORD = os.environ.get("WT_PASS", "eGov@123")

CONFIGURATOR = f"{HOST}/configurator"
EMPLOYEE = f"{HOST}/digit-ui/employee"

VIEWPORT = {"width": 1440, "height": 900}
HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

# ---------------------------------------------------------------- read-only guard

# DIGIT reads are POSTs (`_search`), so the guard cannot simply block POST.
# It matches the write verbs that appear in DIGIT endpoint paths instead, and
# blocks the genuinely-mutating HTTP methods outright.
WRITE_MARKERS = (
    "_create", "_update", "_delete", "_upsert", "_transition", "_apply",
    "_activate", "_deactivate", "_publish", "_import", "_bulk", "_assign",
    "_close", "_reopen", "_reject", "_add", "_remove", "_send",
    "filestore/v1/files",
)
WRITE_METHODS = {"PUT", "PATCH", "DELETE"}

# Endpoints that look like writes but are not, or that we must let through.
ALLOW = ("oauth/token",)

_blocked: list[str] = []


def blocked_requests() -> list[str]:
    return list(_blocked)


async def install_readonly_guard(context) -> None:
    """Abort every mutating request on this browser context."""

    async def handler(route):
        req = route.request
        url = req.url
        low = url.lower()
        if any(a in low for a in ALLOW):
            await route.continue_()
            return
        if req.method in WRITE_METHODS or any(m in low for m in WRITE_MARKERS):
            entry = f"{req.method} {url}"
            _blocked.append(entry)
            print(f"[READ-ONLY GUARD] blocked {entry}")
            await route.abort()
            return
        await route.continue_()

    await context.route("**/*", handler)


def write_guard_log() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / "_guard.log"
    if _blocked:
        log.write_text("\n".join(_blocked) + "\n")
        print(f"\n!! read-only guard blocked {len(_blocked)} request(s) — see {log}")
    else:
        log.write_text("no mutating requests were attempted\n")
        print("\nread-only guard: no mutating requests were attempted")


# ---------------------------------------------------------------- login

async def goto(page, url: str, *, wait_ms: int = 1800, retries: int = 3) -> None:
    """Navigate and settle.

    `networkidle` is unreliable on these SPAs (polling dashboards never go
    idle), so use domcontentloaded + a fixed settle. Retries on transient
    transport errors — a long capture run over a home connection WILL hit
    ERR_NETWORK_CHANGED at least once, and losing a whole flow to it is worse
    than waiting a few seconds.
    """
    last = None
    for attempt in range(retries):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(wait_ms)
            return
        except Exception as e:
            last = e
            if "ERR_NETWORK_CHANGED" in str(e) or "ERR_CONNECTION" in str(e) or "Timeout" in str(e):
                print(f"[retry {attempt + 1}/{retries}] {url}: {str(e)[:60]}")
                await page.wait_for_timeout(4000)
                continue
            raise
    raise last


async def login(page, walker=None, *, mode: str = "management", shots: bool = True):
    """Sign into the configurator. `mode` is 'management' or 'onboarding'."""
    # The SPA can take a while to hydrate on a cold cache, and a dropped asset
    # request leaves a permanently blank #root — so reload rather than waiting
    # forever on a page that will never render.
    for attempt in range(4):
        await goto(page, f"{CONFIGURATOR}/login", wait_ms=2500)
        try:
            await page.wait_for_selector("#username", state="visible", timeout=20000)
            break
        except Exception:
            print(f"[login retry {attempt + 1}/4] login form never rendered — reloading")
    else:
        raise RuntimeError("configurator login form never rendered")
    if shots and walker:
        await walker.shot("login_blank")

    await page.click(f"button:has-text('{'Management' if mode == 'management' else 'Onboarding'}')")
    await page.fill("#username", USERNAME)
    await page.fill("#password", PASSWORD)      # never smart_fill a password
    await page.fill("#tenantCode", TENANT)
    if shots and walker:
        await walker.shot(f"login_filled_{mode}")

    await page.click("button[type=submit]:has-text('Sign In')")
    await page.wait_for_timeout(4000)
    print(f"[login] mode={mode} -> {page.url}")
    return page.url


async def dismiss_overlays(page) -> None:
    """Close any toast/dialog that would otherwise sit on top of a screenshot."""
    for sel in ("button[aria-label='Close']", "[data-radix-toast-close]"):
        try:
            for el in await page.query_selector_all(sel):
                if await el.is_visible():
                    await el.click()
                    await page.wait_for_timeout(200)
        except Exception:
            pass


# ---------------------------------------------------------------- employee UI

EMP_CITY = os.environ.get("WT_EMP_CITY", "Bomet County")   # the display name of tenant `ke`


async def employee_login(page, walker=None, *, city: str = EMP_CITY, shots: bool = True):
    """Sign into the digit-ui employee app.

    Three non-obvious bits, all learned from the live page:
      * the city combobox filters through a "Search" box and renders
        `li[role=option]` — matching on page text alone hits the "Bomet County"
        banner heading instead of the option;
      * the privacy `<input type=checkbox>` has `pointer-events: none`, so the
        styled `<label for=...>` is what toggles it;
      * Login stays disabled until city + consent are both set.
    """
    await goto(page, EMPLOYEE, wait_ms=5000)
    await page.wait_for_selector("#emp-username", state="visible", timeout=45000)
    if shots and walker:
        await walker.shot("employee_signin_blank")

    await page.click("button:has-text('Select city')", timeout=15000)
    await page.wait_for_timeout(800)
    search = page.locator("input[placeholder='Search']")
    if await search.count():
        await search.first.fill(city.split()[0])
        await page.wait_for_timeout(1000)
    if shots and walker:
        await walker.shot("employee_city_picker")
    await page.get_by_role("option", name=city).first.click(timeout=10000)
    await page.wait_for_timeout(700)

    await page.fill("#emp-username", USERNAME)
    await page.fill("#emp-password", PASSWORD)
    await page.click("label[for=privacy-component-check]", timeout=5000)
    await page.wait_for_timeout(500)
    if shots and walker:
        await walker.shot("employee_signin_filled")

    await page.get_by_role("button", name="Login", exact=True).click(timeout=15000)
    await page.wait_for_url(lambda u: "/user/login" not in u, timeout=45000)
    await page.wait_for_timeout(5000)
    print(f"[employee login] -> {page.url}")
    return page.url
