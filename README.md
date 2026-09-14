# CyberLearn CTF — Group 18 Security Quest

A progressive educational Capture The Flag (CTF) platform developed for the **IE3132 Penetration Testing** module at the **Sri Lanka Institute of Information Technology (SLIIT)**.

CyberLearn CTF provides a controlled environment where participants solve six interconnected cybersecurity challenges covering Steganography, Web Security, Cryptography, Digital Forensics, Networking, and Linux/System Security.

The platform was implemented using **Python Flask, HTML5, CSS3, Jinja2, JavaScript, and SQLite**, with Kali Linux used as the primary challenge-analysis environment.

---

## Project Overview

CyberLearn CTF is designed for beginner-to-intermediate cybersecurity students who want hands-on experience with practical security investigation techniques.

Participants progress through six stages of increasing difficulty.

Each successful challenge requires the participant to:

1. Analyse the provided challenge or artefact.
2. Recover the correct flag.
3. Submit the flag through the CyberLearn platform.
4. Unlock the next stage.
5. Continue until all six stages are completed.

The standard flag format used throughout the CTF is:

```text
GROUP18{challenge_specific_value}
```

Actual challenge flags are intentionally excluded from this README.

---

# Key Features

- **Six Progressive Cybersecurity Challenges**: Covering file analysis, web flaws, crypto, forensics, PCAP, and Linux configurations.
- **Complete User Account Management**: Participants can view profile statistics, update username/email, change password, or permanently delete their account with cascade cleanup.
- **Light & Dark Mode Dual Theming**: Instant theme switcher (Moon / Sun) with zero-flash rendering and persistent `localStorage` preference.
- **Participant Registration & Authentication**: Secure session handling with password hashing (`scrypt`/`pbkdf2`).
- **Server-Side Flag Validation**: HMAC-SHA256 digests with secret peppering to prevent flag leakage.
- **Sequential Stage Unlocking**: Strict server-side authorization ensuring challenges must be solved in order.
- **Participant Quest Dashboard**: Real-time progress tracking, visual progress bars, and operational rank badges (*Recruit, Investigator, Master Operative*).
- **Downloadable Challenge Artefacts**: Secure distribution of challenge targets (images, text, ZIPs, PCAP files).
- **Controlled Web Challenge (Stage 02)**: Demonstrates client-side authorization weaknesses in an isolated test harness.
- **Progressive Hints**: Structured hint accordions to guide learners without spoiling solutions.
- **Modern Responsive Cyber UI**: Sleek glassmorphic aesthetics, monospace terminals, glowing accents, and mobile-friendly layouts.
- **Built-in Security Controls**: CSRF tokens, strict rate limiting, HTTPOnly/SameSite cookies, and Content Security Policy (CSP).

---

# Challenge Structure

| Stage | Challenge | Domain | Difficulty | Challenge Type |
|---|---|---|---|---|
| 01 | Hidden in Plain Sight | Steganography | Easy | Image Analysis |
| 02 | The Broken Gate | Web Security | Easy | Controlled Web Challenge |
| 03 | The Encoded Message | Cryptography | Moderate | Encoded Message |
| 04 | Digital Footprints | Digital Forensics | Moderate | Evidence Archive |
| 05 | Traffic Under Investigation | Networking | Moderate-Hard | PCAP Analysis |
| 06 | The Misconfigured Server | Linux / System Security | Hard | Linux Evidence Analysis |

---

# Challenge Progression

```text
Stage 01 (Steganography)
   ↓
Stage 02 (Web Security)
   ↓
Stage 03 (Cryptography)
   ↓
Stage 04 (Digital Forensics)
   ↓
Stage 05 (Networking / PCAP)
   ↓
Stage 06 (Linux Privilege Security)
   ↓
CyberLearn CTF Completed!
```

The platform enforces progression strictly on the server side. A participant cannot open a subsequent stage until the previous challenge has been successfully verified.

---

# Stage 01 — Hidden in Plain Sight

**Domain:** Steganography  
**Difficulty:** Easy

Participants receive an image called:

```text
welcome.png
```

The image contains information that is not immediately visible. The participant must inspect the file structure and recover the hidden Stage 01 flag.

Suggested tools:

```text
file
strings
ExifTool
Steganography analysis tools
Hex viewers
```

This challenge introduces basic file analysis, metadata inspection, and hidden-information discovery.

---

# Stage 02 — The Broken Gate

**Domain:** Web Security  
**Difficulty:** Easy

Stage 02 contains a deliberately vulnerable web component protected by an access gate.

The participant must investigate the page and inspect browser-side resources to identify information that has been insecurely trusted or exposed on the client side.

Suggested tools:

```text
Web Browser
Browser Developer Tools (F12)
View Page Source
Network / Sources Tab
Burp Suite
```

> **Note:** Stage 02 is intentionally vulnerable for educational purposes. The weakness is confined to the controlled Stage 02 challenge component and demonstrates why client-side security checks should never be trusted.

---

# Stage 03 — The Encoded Message

**Domain:** Cryptography  
**Difficulty:** Moderate

Participants receive:

```text
message.txt
```

The message has been transformed using multiple layers of encoding and ciphering. The participant must identify the encoding schemes, reverse the transformation layers, and recover the original plaintext.

Techniques include:

```text
Base64 decoding
Caesar cipher / Substitution analysis
```

Suggested tools:

```text
CyberChef
Linux base64 utility
Python
Text editor
```

---

# Stage 04 — Digital Footprints

**Domain:** Digital Forensics  
**Difficulty:** Moderate

Participants receive a forensic evidence archive:

```text
evidence.zip
```

The archive contains logs, terminal history, standard artefacts, distractors, and suspicious user session activity. Participants must correlate the available artefacts, inspect hidden files, and follow the evidence chain.

Suggested tools:

```text
unzip
file
strings
grep
find
cat / less
ExifTool
```

---

# Stage 05 — Traffic Under Investigation

**Domain:** Networking  
**Difficulty:** Moderate-Hard

Participants receive:

```text
traffic_capture.pcap
```

The packet capture contains multiple protocols and conversations mixed with background noise. Participants must isolate the relevant network conversation, reconstruct the TCP session, and extract the hidden flag.

Suggested tools:

```text
Wireshark
TShark
Wireshark Display Filters (e.g. http, tcp.port)
Follow TCP Stream
```

---

# Stage 06 — The Misconfigured Server

**Domain:** Linux / System Security  
**Difficulty:** Hard

The final stage provides a controlled Linux server evidence package:

```text
stage06_evidence.zip
```

The package simulates evidence collected from an audit of a Linux server. It contains files such as:

```text
/etc/passwd
/etc/sudoers
/etc/crontab
/etc/ssh/sshd_config
/var/log/auth.log
System notes & configuration snapshots
```

Investigation workflow:

```text
Audit Linux user accounts
        ↓
Review sudoers privilege configuration
        ↓
Identify the over-privileged account
        ↓
Correlate with authentication & execution logs
        ↓
Locate the restricted evidence path
        ↓
Recover the final flag
```

Suggested tools:

```text
unzip
grep
find
cat / less
```

---

# User Account Management

CyberLearn CTF includes dedicated participant profile and account settings accessible at `/account`:

1. **Profile Overview**: Displays operative username, registered email, registration timestamp, solved stages ratio, and an animated quest progress indicator.
2. **Update Profile Details**: Participants can update their username and email address with automatic conflict checking against existing users.
3. **Change Password**: Participants can update their passphrase by verifying their current password and entering a new secure passphrase meeting complexity rules.
4. **Danger Zone (Account Deletion)**: Participants can permanently delete their account. Account deletion requires entering the current password and typing `DELETE` in uppercase. All associated records in `progress` are automatically cascade deleted via SQLite foreign keys.

---

# Theming (Light & Dark Mode)

The platform features a modern, eye-friendly dual-theme engine:

- **Dark Cyber Mode (Default)**: Deep obsidian/navy background, glowing cyan and mint accents, terminal fonts, and high-contrast card borders.
- **Crisp Light Mode**: High-contrast white and soft slate backgrounds, clean typography, teal and azure accents, and subtle card elevation.
- **Persistence**: Theme selection is remembered using browser `localStorage`.
- **Zero-Flicker (Anti-FOUC)**: Theme initialization runs in `<head>` via `static/js/theme.js` to ensure seamless loading across page transitions.

---

# Technology Stack

## Backend
```text
Python 3
Flask (3.1+)
Flask-WTF (CSRF & Form Validation)
Flask-Limiter (Rate Limiting)
SQLite 3 (Relational Database with Foreign Key Cascading)
Werkzeug (Secure Password Hashing)
python-dotenv (Environment Variable Management)
```

## Frontend
```text
HTML5 (Semantic Markup)
Vanilla CSS3 (Custom Properties / Dual Theming / Glassmorphism)
JavaScript (Vanilla ES6, CSP Compliant)
Jinja2 (Template Inheritance)
```

## Challenge Analysis & Tools
```text
Kali Linux
Oracle VirtualBox
Wireshark / TShark
Burp Suite
CyberChef
ExifTool
Linux CLI Tools (strings, grep, find, base64)
```

---

# Architecture

```text
                     ┌─────────────────────────┐
                     │      Kali Linux VM      │
                     │ Participant Environment │
                     └────────────┬────────────┘
                                  │
                                  │ HTTP (Port 5000)
                                  ▼
                     ┌─────────────────────────┐
                     │    CyberLearn Flask     │
                     │        Platform         │
                     ├─────────────────────────┤
                     │ Authentication & Profile│
                     │ Light / Dark Theme      │
                     │ Challenge Management    │
                     │ Stage Progression       │
                     │ Flag Validation (HMAC)  │
                     │ Challenge Downloads     │
                     │ Progress Tracking       │
                     └────────────┬────────────┘
                                  │
                   ┌──────────────┴──────────────┐
                   │                             │
                   ▼                             ▼
         ┌──────────────────┐        ┌──────────────────────┐
         │ SQLite Database  │        │ Challenge Artefacts  │
         ├──────────────────┤        ├──────────────────────┤
         │ users            │        │ Stage 01 - Image     │
         │ challenges       │        │ Stage 03 - Message   │
         │ progress         │        │ Stage 04 - ZIP       │
         │ (CASCADE on del) │        │ Stage 05 - PCAP      │
         └──────────────────┘        │ Stage 06 - ZIP       │
                                     └──────────────────────┘
```

---

# Project Structure

```text
CyberLearnCTF/
│
├── app.py                      # Main Flask application & routes
├── forms.py                    # WTForms classes (Auth, Profile, Password, Delete)
├── requirements.txt            # Python dependencies
├── setup_env.py                # Helper script to initialize .env file
│
├── create_stage01.py           # Artefact generator: Steganography (welcome.png)
├── create_stage03.py           # Artefact generator: Cryptography (message.txt)
├── create_stage04.py           # Artefact generator: Forensics (evidence.zip)
├── create_stage05.py           # Artefact generator: Networking (traffic_capture.pcap)
├── create_stage06.py           # Artefact generator: Linux Security (stage06_evidence.zip)
│
├── challenges/                 # Directory containing generated challenge files
│   ├── stage01/welcome.png
│   ├── stage03/message.txt
│   ├── stage04/evidence.zip
│   ├── stage05/traffic_capture.pcap
│   └── stage06/stage06_evidence.zip
│
├── database/                   # Database storage
│   └── cyberlearn.db           # SQLite database (auto-created)
│
├── static/
│   ├── css/
│   │   └── style.css           # Design system, light/dark themes & responsive styles
│   └── js/
│       └── theme.js            # Light/Dark mode switcher & local storage persistence
│
└── templates/                  # Jinja2 HTML templates
    ├── stage02/
    │   ├── gate.html           # Stage 02 controlled web challenge page
    │   └── gate.js.j2          # Stage 02 dynamic client-side challenge script
    │
    ├── base.html               # Master layout (Navbar, Theme Toggle, Alerts, Footer)
    ├── index.html              # Landing page (Hero, Terminal, 6 Domains)
    ├── register.html           # Participant registration
    ├── login.html              # Participant login
    ├── dashboard.html          # Participant quest dashboard & progress
    ├── account.html            # User account settings & danger zone
    ├── challenge.html          # Challenge view, briefing, hints & flag submission
    └── error.html              # Custom error pages (403, 404, 429)
```

---

# Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/aroshasampath/CyberLearnCTF.git
cd CyberLearnCTF
```

---

## 2. Set Up Virtual Environment

### Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

The application requires a `.env` file containing secret keys and stage flags.

Generate a new `.env` file automatically using the setup script:

```bash
python setup_env.py
```

Or create a `.env` file manually:

```env
SECRET_KEY=generate_a_random_hex_key_here
FLAG_PEPPER=generate_another_random_hex_pepper_here

STAGE1_FLAG=GROUP18{hidden_metadata_found}
STAGE2_FLAG=GROUP18{client_side_gate_broken}
STAGE3_FLAG=GROUP18{double_layer_decoded}
STAGE4_FLAG=GROUP18{digital_footprints_traced}
STAGE5_FLAG=GROUP18{traffic_stream_identified}
STAGE6_FLAG=GROUP18{root_of_the_problem}
```

> **Security Note:** The `.env` file is excluded from Git version control via `.gitignore`.

---

## 5. Generate Challenge Artefacts

If the challenge files are not already present in the `challenges/` directory, recreate them using:

```bash
python create_stage01.py
python create_stage03.py
python create_stage04.py
python create_stage05.py
python create_stage06.py
```

---

## 6. Run the Application

Start the Flask development server:

```bash
python app.py
```

Or directly using the virtual environment interpreter on Windows:

```powershell
.\venv\Scripts\python.exe app.py
```

Access the platform in your browser at:

👉 **http://127.0.0.1:5000** or **http://localhost:5000**

---

# Participant Workflow

```text
1. Register Account  ──▶  2. Login  ──▶  3. Dashboard (Stage 01 Unlocked)
                                                    │
                                                    ▼
6. View Profile & Settings  ◀──  5. Next Stage Unlocks  ◀──  4. Download Artefact & Submit Flag
   (Theme, Password, Delete)     (Repeats through Stage 06)
```

---

# Security Controls

The platform implements robust defensive security controls:

- **Password Security**: Passwords hashed using Werkzeug's secure hashing.
- **SQL Injection Prevention**: Parameterized queries across all SQLite interactions.
- **CSRF Protection**: Form-level CSRF token validation via Flask-WTF.
- **HMAC Flag Digests**: Submitted flags are compared against peppered digests using `hmac.compare_digest` to prevent timing attacks.
- **Rate Limiting**: Configured with Flask-Limiter to guard against brute-force attacks on login, registration, and flag submission.
- **Cookie Hardening**: `HttpOnly=True`, `SameSite=Lax`, and configurable `Secure` cookies.
- **Security Headers**: Injected via after-request hooks:
  - `Content-Security-Policy`: Restricts scripts and styles to self.
  - `X-Frame-Options: DENY`: Prevents clickjacking.
  - `X-Content-Type-Options: nosniff`: Prevents MIME-sniffing.
  - `Referrer-Policy: strict-origin-when-cross-origin`.
  - `Cache-Control: no-store`: Applied to authenticated routes.

---

# Testing & Verification

The repository includes automated test verification covering:

- Participant registration, authentication, and session handling.
- Account profile updating (username and email uniqueness validation).
- Password change validation (current password verification and complexity rules).
- Account deletion and SQLite foreign key cascading.
- Sequential stage unlocking and flag submission validation.
- Stage 02 dynamic script delivery and client-side gate interface.
- Theme switching persistence.

---

# Academic Context

```text
Institution    : Sri Lanka Institute of Information Technology (SLIIT)
Faculty        : Faculty of Computing
Module         : IE3132 - Penetration Testing
Project        : Capture The Flag (CTF) Play Box Implementation
Group          : Group 18
Platform Name  : CyberLearn CTF
Academic Year  : 2026
```

---

# License & Educational Disclaimer

CyberLearn CTF was developed strictly for academic and educational purposes within the SLIIT IE3132 Penetration Testing module. 

All vulnerabilities and challenges are hosted within an isolated, controlled local environment. The techniques demonstrated should only be performed on systems you own or have explicit, documented authorization to test.

---

**CyberLearn CTF — Learn security by solving it.**
