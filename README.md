# CyberLearn CTF — Group 18 Security Quest

A progressive educational Capture The Flag (CTF) platform developed for the **IE3132 Penetration Testing** module at the **Sri Lanka Institute of Information Technology (SLIIT)**.

CyberLearn CTF provides a controlled environment where participants solve six interconnected cybersecurity challenges covering Steganography, Web Security, Cryptography, Digital Forensics, Networking, and Linux/System Security.

The platform was implemented using **Python Flask, HTML, CSS, Jinja2, and SQLite**, with Kali Linux used as the primary challenge-analysis environment.

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

- Six progressive cybersecurity challenges
- Participant registration and login
- Password hashing
- Server-side flag validation
- Sequential stage unlocking
- Participant progress tracking
- Downloadable challenge artefacts
- Controlled vulnerable web challenge
- Progressive hints
- SQLite database integration
- CSRF protection
- Rate limiting
- Secure session configuration
- Security headers
- Responsive web interface
- Kali Linux compatible challenge workflow

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
Stage 01
   ↓
Stage 02
   ↓
Stage 03
   ↓
Stage 04
   ↓
Stage 05
   ↓
Stage 06
   ↓
CTF Completed
```

The platform enforces progression on the server side.

A participant cannot open the next stage until the previous stage has been successfully completed.

---

# Stage 01 — Hidden in Plain Sight

**Domain:** Steganography  
**Difficulty:** Easy

Participants receive an image called:

```text
welcome.png
```

The image contains information that is not immediately visible.

The participant must inspect the file and recover the hidden Stage 01 flag.

Suggested tools:

```text
file
strings
ExifTool
Steganography analysis tools
```

This challenge introduces basic file analysis, metadata inspection, and hidden-information discovery.

---

# Stage 02 — The Broken Gate

**Domain:** Web Security  
**Difficulty:** Easy

Stage 02 contains a deliberately vulnerable web component.

The participant must investigate the page and inspect browser-side resources to identify information that has been insecurely trusted or exposed on the client side.

Suggested tools:

```text
Web Browser
Browser Developer Tools
View Source
Burp Suite
```

> Stage 02 is intentionally vulnerable for educational purposes. The weakness is limited to the controlled Stage 02 challenge component and is not intended to represent secure application-development practice.

---

# Stage 03 — The Encoded Message

**Domain:** Cryptography  
**Difficulty:** Moderate

Participants receive:

```text
message.txt
```

The message has been transformed using multiple layers.

The intended challenge requires the participant to reverse the transformations and recover the original information.

Techniques include:

```text
Base64 decoding
Caesar cipher analysis
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

The archive contains logs, files, normal artefacts, distractors, and suspicious evidence.

Participants must correlate the available artefacts and follow the intended evidence chain.

Suggested tools:

```text
unzip
file
strings
grep
find
cat
less
ExifTool
```

The challenge develops basic digital-forensics and evidence-correlation skills.

---

# Stage 05 — Traffic Under Investigation

**Domain:** Networking  
**Difficulty:** Moderate-Hard

Participants receive:

```text
traffic_capture.pcap
```

The packet capture contains relevant communication mixed with background traffic.

Participants must identify the important network conversation and reconstruct the relevant traffic stream.

Suggested tools:

```text
Wireshark
TShark
Wireshark Display Filters
Follow TCP Stream
```

The challenge focuses on packet analysis, protocol identification, traffic filtering, and stream reconstruction.

---

# Stage 06 — The Misconfigured Server

**Domain:** Linux / System Security  
**Difficulty:** Hard

The final stage provides a controlled Linux server evidence package:

```text
stage06_evidence.zip
```

The package simulates evidence collected from a Linux server.

It contains artefacts such as:

```text
/etc/passwd
/etc/sudoers
/etc/crontab
/etc/ssh/sshd_config
/var/log/auth.log
system notes
supporting evidence files
```

Participants must:

```text
Identify Linux users
        ↓
Review privilege configuration
        ↓
Identify the suspicious account
        ↓
Correlate the finding with authentication logs
        ↓
Follow the evidence path
        ↓
Recover the final flag
```

Suggested tools:

```text
unzip
find
cat
less
grep
```

Stage 06 uses a simulated evidence package instead of a live vulnerable Linux server.

This keeps the challenge lightweight while still teaching Linux privilege configuration, security-log analysis, evidence correlation, and system-security concepts.

---

# Technology Stack

## Backend

```text
Python 3
Flask
Flask-WTF
Flask-Limiter
SQLite
Werkzeug
python-dotenv
```

## Frontend

```text
HTML5
CSS3
Jinja2
```

## Security Analysis Environment

```text
Kali Linux
Oracle VirtualBox
```

## Cybersecurity Tools

```text
ExifTool
Burp Suite
Browser Developer Tools
CyberChef
Wireshark
TShark
Linux command-line utilities
```

## Development Tools

```text
Visual Studio Code
Git
GitHub
```

---

# Architecture

```text
                    ┌─────────────────────────┐
                    │      Kali Linux VM      │
                    │ Participant Environment │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP
                                 ▼
                    ┌─────────────────────────┐
                    │    CyberLearn Flask     │
                    │        Platform         │
                    ├─────────────────────────┤
                    │ Authentication          │
                    │ Challenge Management    │
                    │ Stage Progression       │
                    │ Flag Validation         │
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
        │ Users            │        │ Stage 01 - Image     │
        │ Challenges       │        │ Stage 03 - Message   │
        │ Progress         │        │ Stage 04 - ZIP       │
        │ Flag Digests     │        │ Stage 05 - PCAP      │
        └──────────────────┘        │ Stage 06 - ZIP       │
                                    └──────────────────────┘
```

Stage 02 is provided as a controlled intentionally vulnerable web component inside the local CTF environment.

---

# Project Structure

```text
CyberLearnCTF/
│
├── app.py
├── forms.py
├── requirements.txt
├── setup_env.py
│
├── create_stage01.py
├── create_stage03.py
├── create_stage04.py
├── create_stage05.py
├── create_stage06.py
│
├── challenges/
│   │
│   ├── stage01/
│   │   └── welcome.png
│   │
│   ├── stage03/
│   │   └── message.txt
│   │
│   ├── stage04/
│   │   └── evidence.zip
│   │
│   ├── stage05/
│   │   └── traffic_capture.pcap
│   │
│   └── stage06/
│       └── stage06_evidence.zip
│
├── database/
│   └── cyberlearn.db
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    │
    ├── stage02/
    │   ├── gate.html
    │   └── gate.js.j2
    │
    ├── base.html
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── challenge.html
    └── error.html
```

> The `.env` file, virtual environment, and local SQLite database are excluded from Git version control.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/aroshasampath/CyberLearnCTF.git
```

Move into the project directory:

```bash
cd CyberLearnCTF
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Sensitive application configuration is stored inside a local `.env` file.

The `.env` file must never be committed to GitHub.

Required environment variables include:

```env
SECRET_KEY=your_secret_key_here
FLAG_PEPPER=your_flag_pepper_here

STAGE1_FLAG=GROUP18{your_stage1_flag}
STAGE2_FLAG=GROUP18{your_stage2_flag}
STAGE3_FLAG=GROUP18{your_stage3_flag}
STAGE4_FLAG=GROUP18{your_stage4_flag}
STAGE5_FLAG=GROUP18{your_stage5_flag}
STAGE6_FLAG=GROUP18{your_stage6_flag}
```

If the included environment setup script is being used:

```bash
python setup_env.py
```

---

# Generate Challenge Artefacts

The challenge-generation scripts can be used to recreate the challenge files.

```bash
python create_stage01.py
python create_stage03.py
python create_stage04.py
python create_stage05.py
python create_stage06.py
```

Generated challenge artefacts are stored inside the corresponding folders under:

```text
challenges/
```

---

# Run the Application

Start the application:

```bash
python app.py
```

The Flask application can then be accessed using:

```text
http://127.0.0.1:5000
```

If the application is accessed from a Kali Linux VM, use the Windows host IP address associated with the controlled local or VirtualBox network.

---

# Participant Workflow

```text
Register
   ↓
Login
   ↓
Stage 01
   ↓
Recover Flag
   ↓
Submit Flag
   ↓
Stage 02 Unlocks
   ↓
Continue through all stages
   ↓
Stage 06
   ↓
Final Flag
   ↓
CyberLearn CTF Completed
```

---

# Security Features

The main CyberLearn platform includes several security-focused controls.

These include:

```text
Password hashing
Parameterized SQLite queries
CSRF protection
Server-side flag validation
Server-side stage authorization
Rate limiting
HTTPOnly session cookies
SameSite cookie restrictions
Content Security Policy
X-Frame-Options
X-Content-Type-Options
Restricted challenge progression
Environment-based secrets
```

Flag values used for normal challenge validation are not directly exposed through the participant-facing interface.

---

# Stage 02 Security Exception

Stage 02 intentionally demonstrates an insecure client-side security design.

The challenge is designed to show why:

```text
Client-side validation should not be trusted for authorization
Sensitive information should not be exposed to the browser
Security decisions should be enforced on the server side
```

The deliberately vulnerable behaviour is isolated to the educational Stage 02 challenge.

---

# Flag Validation

Each submitted flag is validated by the Flask backend.

Expected flag values are processed server-side before being stored for validation.

A correct submission:

```text
Marks the stage as completed
        ↓
Stores participant progress
        ↓
Unlocks the next challenge
```

An incorrect submission does not unlock the next stage.

---

# Testing

The project can be tested for:

```text
Participant registration
Participant login
Correct flag submission
Incorrect flag submission
Sequential stage locking
Challenge downloads
Stage 02 intended weakness
Stage 03 decoding path
Stage 04 evidence chain
Stage 05 PCAP analysis
Stage 06 Linux evidence analysis
CSRF protection
Rate limiting
Unauthorized stage access
Final CTF completion
```

---

# Recommended Environment

The project was designed to operate on lightweight student hardware.

```text
Host Operating System : Windows
Processor             : 4-core CPU or equivalent
RAM                   : 8 GB
Participant VM        : Kali Linux
Virtualization        : Oracle VirtualBox
Backend               : Python Flask
Database              : SQLite
```

The final Stage 06 implementation does not require an additional Ubuntu Server VM.

---

# Git Version Control

Typical development workflow:

```bash
git status
git add .
git commit -m "Describe the implemented change"
git push
```

Example:

```bash
git commit -m "Implement Stage 06 Linux evidence challenge"
```

---

# Repository Security

The following should not be uploaded to GitHub:

```text
.env
venv/
database/*.db
__pycache__/
*.pyc
```

Recommended `.gitignore`:

```gitignore
venv/
.env
__pycache__/
*.pyc
database/*.db
.vscode/
```

Never publish:

```text
Real passwords
Private keys
API keys
Production credentials
Personal data
Sensitive institutional information
```

---

# Educational Use

CyberLearn CTF was created only for authorized cybersecurity education, practical learning, and controlled penetration-testing exercises.

All challenge artefacts, credentials, vulnerabilities, and evidence used by the CTF are fictional or intentionally created for the lab environment.

Techniques demonstrated by this project should only be used against systems for which explicit authorization has been granted.

---

# Academic Context

```text
Institution : Sri Lanka Institute of Information Technology (SLIIT)
Module      : IE3132 - Penetration Testing
Project     : CTF Play Box Implementation
CTF Name    : CyberLearn CTF - Group 18 Security Quest
Academic Year: 2026
```

---

# Future Improvements

Possible future improvements include:

- Challenge scoring based on difficulty
- Hint penalties
- Leaderboard functionality
- Administrative dashboard
- Detailed participant activity logging
- Automated challenge resets
- Completion timestamps
- Additional cybersecurity challenge categories
- HTTPS deployment
- Improved analytics and reporting

---

# CyberLearn CTF

### Learn security by solving it.

A controlled environment for cybersecurity investigation, practical learning, and penetration-testing education.
