from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8060/index.html"
QA_DIR = Path(r"D:\claude\rainbow\qa")
SHOTS = QA_DIR / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    errors = []
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.on("console", lambda msg: errors.append(f"console-{msg.type}: {msg.text}") if msg.type == "error" else None)
    response = page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(SHOTS / "ENTRY.png"), full_page=True)
    data = page.evaluate("""
    () => {
      const d = window.__dbg || {};
      const read = key => {
        try { return typeof d[key] === 'function' ? d[key]() : d[key]; }
        catch (error) { return {error: String(error)}; }
      };
      return ({
      status: document.readyState,
      title: document.title,
      canvasCount: document.querySelectorAll('canvas').length,
      buttons: [...document.querySelectorAll('button')].map(b => ({id:b.id,text:b.textContent.trim()})),
      dbgKeys: Object.keys(d),
      tableSupportInfo: read('tableSupportInfo'),
      slideInfo: read('slideInfo'),
      treeBuildingClearance: read('treeBuildingClearance'),
      transportCount: read('transportCount'),
      transportLabels: read('transportLabels'),
      transportTypes: read('transportTypes'),
      riverTransportInfo: read('riverTransportInfo'),
      playKidInfo: read('playKidInfo'),
      petShelterInfo: read('petShelterInfo'),
      nightInfo: read('nightInfo'),
      floorOccupancy: read('floorOccupancy'),
      bodyText: document.body.innerText.slice(0, 4000)
      });
    }
    """)
    data["httpStatus"] = response.status if response else None
    data["errors"] = errors
    print(json.dumps(data, ensure_ascii=False, indent=2))
    browser.close()
