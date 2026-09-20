import os
import sys
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external IP to determine the local outbound interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def run_server(port=8000):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mockups"))
    os.chdir(base_dir)
    
    lan_ip = get_lan_ip()
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print("=" * 65)
    print("       WASMAN - SERVER AKSES JARINGAN LOKAL (WI-FI)      ")
    print("=" * 65)
    print(f"\n[OK] Server aktif melayani direktori: {base_dir}")
    print(f"[OK] Port: {port}\n")
    print("CARA AKSES:")
    print("-" * 65)
    print(f"1. Dari Komputer ini (Laptop/PC):")
    print(f"   👉 http://localhost:{port}")
    print(f"   👉 http://{lan_ip}:{port}")
    print()
    print(f"2. Dari HP / Smartphone / Tablet di Wi-Fi yang SAMA:")
    print(f"   👉 http://{lan_ip}:{port}")
    print("-" * 65)
    print("TIPS PENGUJIAN MOBILE DI HP:")
    print("• Buka browser Chrome / Safari di HP Anda.")
    print(f"• Ketik: http://{lan_ip}:{port}")
    print("• Pilih peran yang ingin dicoba (Rumah Tangga, Komunitas, dll).")
    print("• Tekan 'Add to Home Screen' di browser HP untuk simulasi PWA.")
    print("-" * 65)
    print("Tekan Ctrl + C di jendela ini untuk menghentikan server.\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server dihentikan.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
