from pathlib import Path
import os
import shutil
import zipfile

from dotenv import load_dotenv


# =========================================================
# BASE PATH / ENV
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)

STAGE6_FLAG = os.getenv(
    "STAGE6_FLAG"
)

if not STAGE6_FLAG:
    raise RuntimeError(
        "STAGE6_FLAG is missing from .env"
    )


# =========================================================
# STAGE 06 PATHS
# =========================================================

STAGE06_DIR = (
    BASE_DIR
    / "challenges"
    / "stage06"
)

BUILD_DIR = (
    STAGE06_DIR
    / "_build"
)

EVIDENCE_DIR = (
    BUILD_DIR
    / "stage06_evidence"
)

ZIP_FILE = (
    STAGE06_DIR
    / "stage06_evidence.zip"
)


# =========================================================
# CLEAN OLD TEMP BUILD
# =========================================================

if BUILD_DIR.exists():
    shutil.rmtree(
        BUILD_DIR
    )


# =========================================================
# CREATE FOLDERS
# =========================================================

folders = [

    EVIDENCE_DIR
    / "etc"
    / "ssh",

    EVIDENCE_DIR
    / "var"
    / "log",

    EVIDENCE_DIR
    / "home"
    / "analyst",

    EVIDENCE_DIR
    / "filesystem"
    / "opt"
    / "backups",

]

for folder in folders:

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )


# =========================================================
# README
# =========================================================

(
    EVIDENCE_DIR
    / "README.txt"
).write_text(
    """CYBERLEARN CTF - STAGE 06
THE MISCONFIGURED SERVER

Case ID:
CL-06

Host:
ctf-linux-final

Classification:
Training Evidence Only


SCENARIO

Selected artefacts were collected from a simulated
Linux server during a security review.

Some files contain normal system information.

Other files contain information relevant to the
security investigation.


OBJECTIVE

1. Identify the Linux users.

2. Review privilege-related configuration.

3. Correlate the configuration with authentication logs.

4. Identify the security misconfiguration.

5. Follow the evidence path.

6. Recover the final CyberLearn CTF flag.


NOTE

Files originally located under /opt have been copied
into the following evidence-export directory:

filesystem/opt/
""",
    encoding="utf-8",
)


# =========================================================
# PASSWD
# =========================================================

(
    EVIDENCE_DIR
    / "etc"
    / "passwd"
).write_text(
    """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
analyst:x:1000:1000:Security Analyst:/home/analyst:/bin/bash
backupsvc:x:1001:1001:Backup Service:/home/backupsvc:/bin/bash
monitor:x:1002:1002:Monitoring Service:/srv/monitor:/usr/sbin/nologin
""",
    encoding="utf-8",
)


# =========================================================
# SUDOERS
# MAIN SECURITY MISCONFIGURATION
# =========================================================

(
    EVIDENCE_DIR
    / "etc"
    / "sudoers"
).write_text(
    """Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

root ALL=(ALL:ALL) ALL

%admin ALL=(ALL) ALL


# Temporary maintenance privilege.
# This should have been removed after backup validation.

backupsvc ALL=(root) NOPASSWD: /usr/bin/cat /opt/backups/security_note.txt
""",
    encoding="utf-8",
)


# =========================================================
# CRONTAB
# DISTRACTOR / NORMAL CONFIG
# =========================================================

(
    EVIDENCE_DIR
    / "etc"
    / "crontab"
).write_text(
    """SHELL=/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

17 * * * * root cd / && run-parts --report /etc/cron.hourly

25 6 * * * root /usr/local/sbin/rotate-training-logs

0 2 * * * root /usr/local/bin/daily-backup --quiet
""",
    encoding="utf-8",
)


# =========================================================
# SSH CONFIG
# DISTRACTOR
# =========================================================

(
    EVIDENCE_DIR
    / "etc"
    / "ssh"
    / "sshd_config"
).write_text(
    """Port 22

PermitRootLogin no

PubkeyAuthentication yes

PasswordAuthentication no

PermitEmptyPasswords no

X11Forwarding no

UsePAM yes
""",
    encoding="utf-8",
)


# =========================================================
# AUTH LOG
# IMPORTANT EVIDENCE
# =========================================================

(
    EVIDENCE_DIR
    / "var"
    / "log"
    / "auth.log"
).write_text(
    """Sep 10 01:54:13 ctf-linux-final sshd[1182]: Accepted publickey for analyst from 192.168.56.107 port 49320 ssh2

Sep 10 01:54:13 ctf-linux-final systemd-logind[721]: New session 14 of user analyst.

Sep 10 02:02:41 ctf-linux-final sudo: analyst : TTY=pts/0 ; PWD=/home/analyst ; USER=root ; COMMAND=/usr/bin/systemctl status ssh

Sep 10 02:02:42 ctf-linux-final sudo: pam_unix(sudo:session): session closed for user root

Sep 10 02:14:51 ctf-linux-final sshd[1266]: Accepted publickey for backupsvc from 192.168.56.10 port 52018 ssh2

Sep 10 02:15:07 ctf-linux-final sudo: backupsvc : TTY=pts/1 ; PWD=/home/backupsvc ; USER=root ; COMMAND=/usr/bin/cat /opt/backups/security_note.txt

Sep 10 02:15:07 ctf-linux-final sudo: pam_unix(sudo:session): session opened for user root(uid=0) by backupsvc(uid=1001)

Sep 10 02:15:08 ctf-linux-final sudo: pam_unix(sudo:session): session closed for user root

Sep 10 02:20:16 ctf-linux-final sshd[1266]: Received disconnect from 192.168.56.10 port 52018:11: disconnected by user

Sep 10 03:00:00 ctf-linux-final CRON[1412]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)

Sep 10 03:00:01 ctf-linux-final CRON[1412]: pam_unix(cron:session): session closed for user root
""",
    encoding="utf-8",
)


# =========================================================
# SYSTEM NOTES
# =========================================================

(
    EVIDENCE_DIR
    / "home"
    / "analyst"
    / "system_notes.txt"
).write_text(
    """SYSTEM SECURITY REVIEW NOTES

Host:
ctf-linux-final


Review Summary

1. Root SSH login is disabled.

2. Scheduled system tasks appear normal.

3. A temporary maintenance privilege was granted
   to the backup service account.

4. The temporary privilege should have been removed
   after backup validation.

5. Review authentication activity to determine
   whether this privilege was actually used.

6. If an original path under /opt is discovered,
   inspect its exported copy under:

   filesystem/opt/
""",
    encoding="utf-8",
)


# =========================================================
# SERVICE INVENTORY
# =========================================================

(
    EVIDENCE_DIR
    / "home"
    / "analyst"
    / "service_inventory.txt"
).write_text(
    """SERVICE INVENTORY

ssh.service
Status: active

cron.service
Status: active

rsyslog.service
Status: active

monitor-agent.service
Status: active


No public web application is hosted on this
simulated Linux evidence target.
""",
    encoding="utf-8",
)


# =========================================================
# FINAL EVIDENCE
# =========================================================

(
    EVIDENCE_DIR
    / "filesystem"
    / "opt"
    / "backups"
    / "security_note.txt"
).write_text(
    f"""BACKUP SECURITY REVIEW


SECURITY FINDING

The backup service account retained an unnecessary
passwordless root-level sudo privilege after the
maintenance task had been completed.


Affected Account

backupsvc


Configured Privileged Command

/usr/bin/cat /opt/backups/security_note.txt


SECURITY IMPACT

Unnecessary elevated privileges increase the risk
of unauthorized access to privileged information.


FINAL VERIFICATION TOKEN

{STAGE6_FLAG}
""",
    encoding="utf-8",
)


# =========================================================
# MANIFEST
# =========================================================

(
    EVIDENCE_DIR
    / "acquisition_manifest.txt"
).write_text(
    """CYBERLEARN CTF EVIDENCE MANIFEST

Case:
CL-06


Collected Artefacts

/etc/passwd

/etc/sudoers

/etc/crontab

/etc/ssh/sshd_config

/var/log/auth.log

/home/analyst/system_notes.txt

/home/analyst/service_inventory.txt

/opt/backups/security_note.txt
""",
    encoding="utf-8",
)


# =========================================================
# CREATE ZIP
# =========================================================

STAGE06_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

if ZIP_FILE.exists():
    ZIP_FILE.unlink()


with zipfile.ZipFile(
    ZIP_FILE,
    "w",
    compression=zipfile.ZIP_DEFLATED,
) as archive:

    for file_path in sorted(
        EVIDENCE_DIR.rglob("*")
    ):

        if file_path.is_file():

            archive.write(
                file_path,

                file_path.relative_to(
                    BUILD_DIR
                ),
            )


# =========================================================
# REMOVE TEMP BUILD
# =========================================================

shutil.rmtree(
    BUILD_DIR
)


# =========================================================
# DONE
# =========================================================

print()
print(
    "======================================="
)

print(
    " CyberLearn CTF - Stage 06"
)

print(
    "======================================="
)

print()

print(
    "Stage 06 evidence package created."
)

print()

print(
    f"File: {ZIP_FILE}"
)

print()

print(
    "Ready for Flask download."
)