# 🚀 WhatsPhish - Setup & Usage Guide

## 📌 Overview

This project demonstrates a **cybersecurity awareness / educational tool** built using Python and Flask.
It is designed for **learning, testing, and ethical research purposes only**.

---

## ⚠️ Disclaimer

> This project is strictly for **educational and ethical use**.
> Do NOT use it for unauthorized access, phishing, or illegal activities.

---

## 🖥️ Requirements

Make sure you have:

* Python 3.x
* pip (Python package manager)
* Git (optional)

---

## 📥 Installation

### 1️⃣ Clone Repository

```bash id="clone"
git clone https://github.com/anascybertech/WhatsPhish.git
cd WhatsPhish
```

---

## 🖥️ Kali Linux / Desktop Setup

```bash id="kali"
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & pip (if not installed)
sudo apt install python3 python3-pip -y

# Install dependencies
pip install -r requirements.txt || pip install flask

# Run the project
python launcher.py
```

### ▶️ Steps:

1. Navigate to project folder
2. Install dependencies
3. Run script
4. Follow terminal instructions

---

## 📱 Termux (Android) Setup

```bash id="termux"
pkg update && pkg upgrade -y

# Install required packages
pkg install python openssh git -y

# Clone repository
git clone https://github.com/anascybertech/WhatsPhish.git
cd WhatsPhish

# Install dependencies
pip install -r requirements.txt || pip install flask

# Run the project
python launcher.py
```

---

## 🌐 Networking / Access (General)

Depending on your setup, you may use:

* Localhost (default)
* Port forwarding
* External tunneling tools (for development/testing only)

---

## ⚙️ Features

* Simple Python-based interface
* Cross-platform support
* Lightweight setup
* Educational cybersecurity demonstration

---

## 🛠️ Troubleshooting

### ❌ Module Not Found

```bash id="fix1"
pip install flask
```

### ❌ Permission Issues

```bash id="fix2"
chmod +x launcher.py
```

### ❌ Python Not Found

```bash id="fix3"
python3 launcher.py
```

---

## 📁 Project Structure

```
WhatsPhish/
│── launcher.py
│── requirements.txt
│── templates/
│── static/
│── README.md
```

---

## 📞 Support

If you face any issues:

* Recheck installation steps
* Ensure Python is installed
* Check dependencies

---

## 📄 License

This project is for **educational purposes only**.
Use responsibly.
