from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8060/index.html"
QA_DIR = Path(r"D:\claude\rainbow\qa")
SHOTS = QA_DIR / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
evidence_path = QA_DIR / f"evidence-final-{stamp}.json"


def read_debug(page, names):
    return page.evaluate(
        """
        (names) => {
          const d = window.__dbg || {};
          const result = {};
          for (const name of names) {
            try { result[name] = typeof d[name] === 'function' ? d[name]() : d[name]; }
            catch (error) { result[name] = {error: String(error)}; }
          }
          return result;
        }
        """,
        names,
    )


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    console_errors = []
    page_errors = []
    page.on(
        "console",
        lambda msg: console_errors.append({"type": msg.type, "text": msg.text})
        if msg.type == "error"
        else None,
    )
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))

    response = page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2500)
    page.screenshot(path=str(SHOTS / "STABILITY-01-entry.png"), full_page=True)

    baseline = read_debug(
        page,
        [
            "tableSupportInfo",
            "slideInfo",
            "treeBuildingClearance",
            "transportCount",
            "transportLabels",
            "transportTypes",
            "riverTransportInfo",
            "playKidInfo",
            "petShelterInfo",
            "nightInfo",
            "floorOccupancy",
            "shopLabels",
        ],
    )

    labels = baseline.get("shopLabels", [])
    restaurant_index = next((i for i, x in enumerate(labels) if "餐" in str(x)), 1)
    indoor_play_index = next((i for i, x in enumerate(labels) if "游乐" in str(x)), 0)

    page.evaluate("i => window.__dbg.shopView(i)", restaurant_index)
    page.wait_for_timeout(1500)
    page.screenshot(path=str(SHOTS / "GEOM-01-restaurant-tables.png"))

    page.evaluate("i => window.__dbg.shopView(i)", indoor_play_index)
    page.wait_for_timeout(1500)
    page.screenshot(path=str(SHOTS / "PLAY-02-indoor-slide.png"))

    page.evaluate("() => window.__dbg.setView(-112, 35, 105, -112, 3, 45)")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(SHOTS / "PLAY-02-outdoor-slide.png"))

    page.evaluate("() => window.__dbg.setView(-100, 42, 5, -102, 2, -52)")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "LAYOUT-03-tree-house-clearance.png"))

    page.evaluate("() => window.__dbg.transportView(0)")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "TRANSPORT-01-plane-only.png"))

    page.evaluate("() => window.__dbg.submarineView()")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "TRANSPORT-02-river-submarine.png"))

    # Observe river craft again after motion to establish that they remain attached to the river.
    page.wait_for_timeout(3500)
    transport_later = read_debug(page, ["riverTransportInfo"])

    page.locator("#btn-rain").click()
    rain_trajectory = []
    for seconds in (0, 5, 10, 15, 25, 35, 45):
        if seconds:
            previous = rain_trajectory[-1]["seconds"]
            page.wait_for_timeout((seconds - previous) * 1000)
        rain_trajectory.append(
            {
                "seconds": seconds,
                "playKids": read_debug(page, ["playKidInfo"])["playKidInfo"],
            }
        )
        if seconds == 15:
            page.evaluate("() => window.__dbg.petView()")
            page.wait_for_timeout(800)
            page.screenshot(path=str(SHOTS / "ANIMAL-SHELTER-01-rain.png"))
        if seconds == 35:
            page.screenshot(path=str(SHOTS / "CHILD-EVAC-01-rain-35s.png"))

    rain_final = read_debug(
        page,
        ["playKidInfo", "petShelterInfo", "evacuationInfo", "nightInfo"],
    )

    page.locator("#btn-night").click()
    page.wait_for_timeout(12000)
    night = read_debug(page, ["nightInfo", "floorOccupancy", "petShelterInfo"])
    page.evaluate("() => window.__dbg.homeFloorView(16, 2)")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "FLOOR-OCC-01-house17-floor3-night.png"))
    page.screenshot(path=str(SHOTS / "NIGHT-ALL-01-night.png"))

    final_state = {
        "timestamp": stamp,
        "url": page.url,
        "httpStatus": response.status if response else None,
        "title": page.title(),
        "canvasCount": page.locator("canvas").count(),
        "baseline": baseline,
        "transportLater": transport_later,
        "rainTrajectory": rain_trajectory,
        "rainFinal": rain_final,
        "night": night,
        "consoleErrors": console_errors,
        "pageErrors": page_errors,
    }
    evidence_path.write_text(
        json.dumps(final_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({"evidence": str(evidence_path), **final_state}, ensure_ascii=False, indent=2))
    browser.close()
