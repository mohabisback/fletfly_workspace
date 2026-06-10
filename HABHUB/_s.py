import sys, os, subprocess, shutil, http.server, socketserver, webbrowser
from threading import Timer

# الكلاس الخاص بـ Caching
class CachedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=31536000, immutable')
        super().end_headers()

def start_server():
    if not os.path.exists("dist"):
        print("Error: 'dist' folder not found.")
        return
    
    os.chdir("dist")
    PORT = 8000
    socketserver.TCPServer.allow_reuse_address = True
    Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    with socketserver.TCPServer(("", PORT), CachedHandler) as httpd:
        httpd.serve_forever()

def run_publish(filename):
    LIB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fletfly"))
    TEMP_DIST = "temp_wheel_dir"
    PACKAGE_NAME = "fletfly" # تأكد أن هذا هو الاسم الموجود في pyproject.toml
    
    if not filename.endswith(".py"): filename += ".py"
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return

    print("--- Starting Publish Cycle ---")

    # 1. إزالة النسخة الـ editable
    print("Removing editable install...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", PACKAGE_NAME, "-y"], capture_output=True)

    # 2. بناء الـ Wheel
    if os.path.exists(TEMP_DIST): shutil.rmtree(TEMP_DIST)
    print("Viewing fresh wheel...")
    subprocess.run([sys.executable, "-m", "view", LIB_PATH, "--outdir", TEMP_DIST], check=True)

    # 3. تثبيت الـ Wheel (عشان الـ publish يراها كـ package)
    wheels = [f for f in os.listdir(TEMP_DIST) if f.endswith(".whl")]
    wheel_path = os.path.join(TEMP_DIST, wheels[0])
    print(f"Installing {wheels[0]} for publishing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", wheel_path], check=True)

    # 4. النشر
    if os.path.exists("dist"): shutil.rmtree("dist")
    print(f"Publishing {filename}...")
    result = subprocess.run(["flet", "publish", filename])

    # 5. العودة للـ editable mode
    print("Restoring editable install...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", PACKAGE_NAME, "-y"], capture_output=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", LIB_PATH], check=True)
    
    # تنظيف
    shutil.rmtree(TEMP_DIST)

    if result.returncode == 0:
        start_server()
    else:
        print("Flet publish failed!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        start_server()
    else:
        run_publish(sys.argv[1])