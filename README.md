# 🛡️ Web-based Honeypot System

A deceptive web application designed to attract and log unauthorized login attempts. Built using **Python (Flask)** and **SQLite**, this honeypot simulates a realistic login page to capture credentials and IP addresses of potential attackers.

## 🔍 Project Overview

This project is a minimal yet effective honeypot intended for educational and cybersecurity research purposes. It logs every login attempt made on the fake portal and stores the data for analysis via a simple web dashboard.

## 🎯 Features

- 🔐 Fake login form with username/password fields
- 🧠 Captures IP address and credentials on every attempt
- 💾 Stores logs in a local SQLite database
- 🌐 Accessible from another VM (e.g., attacker VM using Kali)
- 📊 Web-based route `/view-logs` to see collected data
- 🛠️ Easy to deploy and run using Python virtual environment

## ⚙️ Tech Stack

- Python 3
- Flask (Web Framework)
- SQLite (Database)
- HTML/CSS (Frontend)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NavyaNandakumar107/Web_based_Honeypot_system.git
cd Web_based_Honeypot_system
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### 3. Run the Application
```bash
python honeypot.py
```

### 4. Access the Honeypot
Open your browser and go to: http://<YOUR-VM-IP>:5000/

### 🧪 Demo Use Case
- Attacker VM (Kali Linux): Simulates a brute-force or manual login attempt.
- Victim VM (Ubuntu): Hosts the honeypot.
- Logs include timestamps, IP addresses, and attempted credentials.

### 📌 Notes
- This project is for educational and demo purposes.
- Do NOT deploy it on a public-facing server without further hardening.

### 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
