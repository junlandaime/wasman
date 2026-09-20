import os
import sys
import subprocess
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
DESKTOP_DIR = os.path.join(DOCS_DIR, "desktop")
MOBILE_DIR = os.path.join(DOCS_DIR, "mobile")

ARTIFACT_DIR = r"C:\Users\jdiju\.gemini\antigravity-ide\brain\4bdc9acc-0323-48ec-aa39-bcbd7271751d\screenshots"
ARTIFACT_DESKTOP_DIR = os.path.join(ARTIFACT_DIR, "desktop")
ARTIFACT_MOBILE_DIR = os.path.join(ARTIFACT_DIR, "mobile")

PAGES = [
    # Public & Auth
    ("landingpage", os.path.join(BASE_DIR, "mockups", "landingpage.html")),
    ("auth-login", os.path.join(BASE_DIR, "mockups", "auth", "login.html")),
    ("auth-register", os.path.join(BASE_DIR, "mockups", "auth", "register.html")),
    
    # Household
    ("household-dashboard", os.path.join(BASE_DIR, "mockups", "household", "dashboard.html")),
    ("household-schedule", os.path.join(BASE_DIR, "mockups", "household", "schedule.html")),
    ("household-collections-create", os.path.join(BASE_DIR, "mockups", "household", "collections-create.html")),
    ("household-collections-index", os.path.join(BASE_DIR, "mockups", "household", "collections-index.html")),
    ("household-collections-show", os.path.join(BASE_DIR, "mockups", "household", "collections-show.html")),
    ("household-education", os.path.join(BASE_DIR, "mockups", "household", "education.html")),
    ("household-education-show", os.path.join(BASE_DIR, "mockups", "household", "education-show.html")),
    ("household-profile", os.path.join(BASE_DIR, "mockups", "household", "profile.html")),
    ("household-notifications", os.path.join(BASE_DIR, "mockups", "household", "notifications.html")),

    # Community
    ("community-dashboard", os.path.join(BASE_DIR, "mockups", "community", "dashboard.html")),
    ("community-tasks", os.path.join(BASE_DIR, "mockups", "community", "tasks.html")),
    ("community-collections-index", os.path.join(BASE_DIR, "mockups", "community", "collections-index.html")),
    ("community-collections-show", os.path.join(BASE_DIR, "mockups", "community", "collections-show.html")),
    ("community-schedules-index", os.path.join(BASE_DIR, "mockups", "community", "schedules-index.html")),
    ("community-schedules-create", os.path.join(BASE_DIR, "mockups", "community", "schedules-create.html")),
    ("community-fleet", os.path.join(BASE_DIR, "mockups", "community", "fleet.html")),
    ("community-officers", os.path.join(BASE_DIR, "mockups", "community", "officers.html")),
    ("community-service-areas", os.path.join(BASE_DIR, "mockups", "community", "service-areas.html")),
    ("community-households", os.path.join(BASE_DIR, "mockups", "community", "households.html")),

    # Factory
    ("factory-dashboard", os.path.join(BASE_DIR, "mockups", "factory", "dashboard.html")),
    ("factory-profile", os.path.join(BASE_DIR, "mockups", "factory", "profile.html")),
    ("factory-supply", os.path.join(BASE_DIR, "mockups", "factory", "supply.html")),

    # Admin
    ("admin-dashboard", os.path.join(BASE_DIR, "mockups", "admin", "dashboard.html")),
    ("admin-users", os.path.join(BASE_DIR, "mockups", "admin", "users.html")),
    ("admin-organizations", os.path.join(BASE_DIR, "mockups", "admin", "organizations.html")),
    ("admin-waste-categories", os.path.join(BASE_DIR, "mockups", "admin", "waste-categories.html")),
    ("admin-waste-materials", os.path.join(BASE_DIR, "mockups", "admin", "waste-materials.html")),
    
    # Navigation Overview
    ("mockup-index", os.path.join(BASE_DIR, "mockups", "index.html")),
]

def ensure_dirs():
    for d in [DESKTOP_DIR, MOBILE_DIR, ARTIFACT_DESKTOP_DIR, ARTIFACT_MOBILE_DIR]:
        os.makedirs(d, exist_ok=True)

def capture_task(name, file_path, mode, out_path, window_size):
    file_url = "file:///" + file_path.replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=2500",
        f"--window-size={window_size}",
        "--hide-scrollbars",
        f"--screenshot={out_path}",
        file_url
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            return True, f"[{mode.upper()}] {name} OK ({os.path.getsize(out_path):,} B)"
        else:
            return False, f"[{mode.upper()}] {name} FAILED (File not created or empty)"
    except Exception as e:
        return False, f"[{mode.upper()}] {name} ERROR: {str(e)}"

def main():
    print(f"Starting screenshot generation for {len(PAGES)} pages...")
    ensure_dirs()

    tasks = []
    for name, file_path in PAGES:
        # Desktop task (1280x850)
        desk_out = os.path.join(DESKTOP_DIR, f"{name}.png")
        tasks.append((name, file_path, "desktop", desk_out, "1280,850"))
        
        # Mobile task (390x844)
        mob_out = os.path.join(MOBILE_DIR, f"{name}.png")
        tasks.append((name, file_path, "mobile", mob_out, "390,844"))

    print(f"Total tasks: {len(tasks)}")
    start_time = time.time()
    
    # Use ThreadPoolExecutor with 4 workers for fast concurrent captures
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(capture_task, *t): t for t in tasks}
        success_count = 0
        for future in as_completed(futures):
            ok, msg = future.result()
            print(msg)
            if ok:
                success_count += 1

    # Copy files to artifact directory as well
    print("\nCopying screenshots to artifact directory...")
    for f in os.listdir(DESKTOP_DIR):
        if f.endswith(".png"):
            shutil.copy2(os.path.join(DESKTOP_DIR, f), os.path.join(ARTIFACT_DESKTOP_DIR, f))
            
    for f in os.listdir(MOBILE_DIR):
        if f.endswith(".png"):
            shutil.copy2(os.path.join(MOBILE_DIR, f), os.path.join(ARTIFACT_MOBILE_DIR, f))

    elapsed = time.time() - start_time
    print(f"\nFinished: {success_count}/{len(tasks)} screenshots captured in {elapsed:.1f}s.")

if __name__ == "__main__":
    main()
