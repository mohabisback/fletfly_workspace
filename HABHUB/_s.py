import sys, os, shutil, subprocess, http.server, socketserver, webbrowser
from threading import Timer

# الكلاس الخاص بـ Caching (لضمان سرعة التحميل وعدم إعادة التنزيل)
class CachedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=31536000, immutable')
        super().end_headers()

def start_server():
    if not os.path.exists("dist"):
        print("Error: 'dist' folder not found. Run the build first.")
        return
    
    os.chdir("dist")
    PORT = 8000
    socketserver.TCPServer.allow_reuse_address = True
    
    Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    print(f"Serving existing dist at http://localhost:{PORT}")
    
    with socketserver.TCPServer(("", PORT), CachedHandler) as httpd:
        httpd.serve_forever()

def run_build(filename):
    LIB_SOURCE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fletfly"))
    LIB_DEST = "fletfly"
    
    if not filename.endswith(".py"): filename += ".py"
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return

    if os.path.exists(LIB_DEST):
        shutil.rmtree(LIB_DEST)
    shutil.copytree(LIB_SOURCE, LIB_DEST)

    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    print(f"Publishing {filename}...")
    result = subprocess.run(["flet", "publish", filename])
    
    if result.returncode != 0:
        print("Build failed!")
        return

    # الانتقال لتشغيل السيرفر بعد البناء
    start_server()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        start_server()
        print("Server only started. for re publishing use: python b.py <filename>")
    else:
        run_build(sys.argv[1])