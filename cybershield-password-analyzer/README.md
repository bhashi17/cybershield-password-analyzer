# 🛡️ CyberShield Password Analyzer

A professional cybersecurity web application that evaluates password strength in real time, estimates crack times across multiple attack scenarios, and generates cryptographically secure passwords.

---

## 🚀 Features

| Feature | Details |
|---|---|
| Real-time analysis | Instant feedback as you type |
| Strength scoring | 0–100% score with 5 levels (Weak → Very Strong) |
| Entropy calculation | Shannon entropy in bits |
| Crack time estimation | Four attack scenarios (online throttled → offline MD5) |
| Common password detection | Checked against a curated list of top common passwords |
| Pattern detection | Sequential, repeating, and keyboard-walk detection |
| Secure password generator | Cryptographically random via `secrets` module |
| Passphrase generator | Memorable multi-word passphrases |
| Responsive UI | Works on desktop and mobile |

---

## 🖥️ Screenshots

![CyberShield Preview](screenshots/preview.png)
![alt text](image-1.png)
---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/cybershield-password-analyzer.git
cd cybershield-password-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open your browser and navigate to **http://localhost:5000**

---

## 📁 Project Structure

```
cybershield-password-analyzer/
│
├── app.py                   # Flask application & API routes
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html           # Main UI template
│
├── static/
│   ├── css/style.css        # Cyberpunk-themed styles
│   ├── js/script.js         # Real-time analysis logic
│   └── images/logo.png
│
├── data/
│   └── common_passwords.txt # Common password blacklist
│
├── utils/
│   ├── password_checker.py  # Core strength analysis engine
│   ├── password_generator.py# Secure password/passphrase generator
│   └── crack_time.py        # Brute-force time estimator
│
└── screenshots/
    └── preview.png
```

---

## 🔌 API Endpoints

### `POST /api/analyze`
Analyze a password's strength.

**Request:**
```json
{ "password": "MyP@ssw0rd!" }
```

**Response:**
```json
{
  "score": 80,
  "level": "Strong",
  "color": "#2ecc71",
  "entropy": 65.4,
  "length": 11,
  "is_common": false,
  "checks": { "length_8": true, "has_upper": true, ... },
  "recommendations": ["16+ characters makes your password significantly harder to crack."],
  "crack_times": {
    "Online (throttled)": "Longer than the age of the universe",
    "Offline (MD5)": "3 hours"
  }
}
```

### `POST /api/generate`
Generate a secure password.

**Request:**
```json
{ "mode": "random", "length": 20, "upper": true, "lower": true, "digits": true, "special": true }
```

**Passphrase mode:**
```json
{ "mode": "passphrase", "words": 4 }
```

---

## 🔐 Security Concepts Demonstrated

- **Password entropy** — measuring unpredictability in bits
- **Brute-force attack modeling** — realistic crack time estimation
- **Common password blacklisting** — dictionary attack prevention
- **Pattern analysis** — sequential and repetition detection
- **Cryptographically secure generation** — using Python's `secrets` module (CSPRNG)
- **Input validation** — server-side analysis, no plaintext storage

---

## 🎓 Academic Use

This project is designed as a portfolio piece demonstrating:
- Practical cybersecurity fundamentals
- Python backend development (Flask)
- RESTful API design
- Responsive frontend (HTML5 / CSS3 / Vanilla JS)

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

## 👤 Author

Built with ❤️ for cybersecurity education.
