# 🚀 Project Setup & Usage Guide

## 📌 Introduction

This repository contains a Python-based project that can be run on both desktop (Kali Linux) and mobile (Termux). Follow the steps below to set it up correctly.

---

## 🖥️ Kali Linux / Desktop Installation

Run the following commands in your terminal:

```bash
cd project_folder
pip install flask
python launcher.py
```

### ▶️ Steps:

1. Open terminal
2. Navigate to the project folder
3. Install required dependencies
4. Run the script
5. Follow on-screen instructions

---

## 📱 Termux (Android) Installation

Run these commands:

```bash
pkg update && pkg upgrade
pkg install python openssh
pip install flask
cd project_folder
python launcher.py
```

### ▶️ Steps:

1. Update packages
2. Install Python & OpenSSH
3. Install required Python libraries
4. Navigate to project directory
5. Execute the script

---

## ⚙️ Key Features

* Cross-platform support (Linux & Android)
* Simple command-line interface
* Easy setup process
* Lightweight dependencies

---

## 🌐 Tunneling Options

| Tool                   | Desktop       | Termux                    | Notes                         |
| ---------------------- | ------------- | ------------------------- | ----------------------------- |
| Cloudflared            | ✅ Best Option | ⚠️ Install manually first | No signup required            |
| Ngrok                  | ✅ Supported   | ✅ Supported               | Requires account & auth token |
| Serveo / localhost.run | ✅ Supported   | ✅ Supported               | Works via SSH                 |

---

## 💡 Recommendation

For beginners, **Cloudflared** is recommended because:

* No signup required
* No token setup
* Easy and fast

---

## ⚠️ Disclaimer

This project is intended for **educational and ethical purposes only**.
Do not use it for unauthorized access, data collection, or illegal activities.

---

## 📞 Support

If you face any issues:

* Recheck installation steps
* Ensure dependencies are installed
* Run commands with proper permissions

---

## 📄 License

This project is provided for learning purposes. Modify and use responsibly.
