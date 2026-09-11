import os
import shutil
import zipfile
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# PATHS / ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


stage4_flag = os.getenv(
    "STAGE4_FLAG"
)


if not stage4_flag:

    raise RuntimeError(
        "STAGE4_FLAG is missing from .env"
    )


OUTPUT_DIR = (
    BASE_DIR
    / "challenges"
    / "stage04"
)


BUILD_DIR = (
    OUTPUT_DIR
    / "evidence_build"
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "evidence.zip"
)


# =========================================================
# CLEAN OLD BUILD
# =========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


if BUILD_DIR.exists():

    shutil.rmtree(
        BUILD_DIR
    )


if OUTPUT_FILE.exists():

    OUTPUT_FILE.unlink()


# =========================================================
# CREATE DIRECTORY STRUCTURE
# =========================================================

logs_dir = (
    BUILD_DIR
    / "logs"
)

user_dir = (
    BUILD_DIR
    / "user"
)

cache_dir = (
    BUILD_DIR
    / "cache"
)


logs_dir.mkdir(
    parents=True,
    exist_ok=True
)

user_dir.mkdir(
    parents=True,
    exist_ok=True
)

cache_dir.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# CASE INFORMATION
# =========================================================

case_info = """
CYBERLEARN DIGITAL FORENSICS UNIT
CASE ID: CL-DF-04

Incident Summary
----------------
A suspicious account session was detected on a training
workstation.

Your task is to examine the collected evidence and determine
what information the suspicious session accessed.

Available evidence includes:

- Authentication logs
- Web access logs
- Recent-file information
- User notes
- Cached application data

Investigators should follow the evidence trail rather than
assuming that every file is relevant.

Flag Format:
GROUP18{...}
""".strip()


(
    BUILD_DIR
    / "CASE_README.txt"
).write_text(
    case_info + "\n",
    encoding="utf-8"
)


# =========================================================
# AUTHENTICATION LOG
# =========================================================

auth_log = """
Sep 10 01:42:03 cyberlearn sshd[1204]: Accepted password for student from 10.10.18.21 port 44182 ssh2
Sep 10 01:43:11 cyberlearn sshd[1204]: pam_unix(sshd:session): session opened for user student
Sep 10 01:58:30 cyberlearn sshd[1204]: pam_unix(sshd:session): session closed for user student

Sep 10 02:05:12 cyberlearn sshd[1488]: Failed password for analyst from 10.10.18.77 port 49311 ssh2
Sep 10 02:05:16 cyberlearn sshd[1488]: Failed password for analyst from 10.10.18.77 port 49311 ssh2
Sep 10 02:05:23 cyberlearn sshd[1488]: Accepted password for analyst from 10.10.18.77 port 49311 ssh2
Sep 10 02:05:23 cyberlearn sshd[1488]: pam_unix(sshd:session): session opened for user analyst

Sep 10 02:07:44 cyberlearn sudo: analyst : TTY=pts/1 ; PWD=/home/analyst ; USER=root ; COMMAND=/usr/bin/cat /home/analyst/.cache/.session_4f2a.log

Sep 10 02:09:18 cyberlearn sshd[1488]: pam_unix(sshd:session): session closed for user analyst

Sep 10 03:11:31 cyberlearn sshd[1701]: Accepted password for backup from 10.10.18.12 port 50521 ssh2
Sep 10 03:13:42 cyberlearn sshd[1701]: pam_unix(sshd:session): session closed for user backup
""".strip()


(
    logs_dir
    / "auth.log"
).write_text(
    auth_log + "\n",
    encoding="utf-8"
)


# =========================================================
# WEB ACCESS LOG - DISTRACTOR
# =========================================================

web_access_log = """
10.10.18.21 - - [10/Sep/2026:01:44:17 +0530] "GET / HTTP/1.1" 200 4218
10.10.18.21 - - [10/Sep/2026:01:44:19 +0530] "GET /assets/main.css HTTP/1.1" 200 1182
10.10.18.44 - - [10/Sep/2026:01:59:22 +0530] "GET /login HTTP/1.1" 200 2450
10.10.18.77 - - [10/Sep/2026:02:06:10 +0530] "GET /dashboard HTTP/1.1" 200 5110
10.10.18.77 - - [10/Sep/2026:02:06:15 +0530] "GET /help HTTP/1.1" 200 1820
10.10.18.12 - - [10/Sep/2026:03:12:07 +0530] "GET /status HTTP/1.1" 200 986
""".strip()


(
    logs_dir
    / "web_access.log"
).write_text(
    web_access_log + "\n",
    encoding="utf-8"
)


# =========================================================
# SYSTEM LOG - DISTRACTOR
# =========================================================

system_log = """
Sep 10 01:30:01 cyberlearn systemd[1]: Started Daily system activity accounting tool.
Sep 10 01:45:10 cyberlearn systemd[1]: Starting system cleanup service.
Sep 10 01:45:12 cyberlearn systemd[1]: Finished system cleanup service.
Sep 10 02:01:02 cyberlearn kernel: eth0: link up
Sep 10 02:10:44 cyberlearn systemd[1]: Started log rotation service.
Sep 10 03:00:01 cyberlearn CRON[1665]: backup task completed successfully
""".strip()


(
    logs_dir
    / "system.log"
).write_text(
    system_log + "\n",
    encoding="utf-8"
)


# =========================================================
# RECENT FILES
# =========================================================

recent_files = """
Recent File Activity
====================

2026-09-10 01:47:12  /home/student/Documents/network_notes.txt
2026-09-10 01:50:33  /home/student/Downloads/reference.pdf
2026-09-10 02:06:18  /home/analyst/Documents/case_notes.txt
2026-09-10 02:07:41  /home/analyst/.cache/.session_4f2a.log
2026-09-10 02:07:50  /home/analyst/Documents/todo.txt
2026-09-10 03:12:14  /home/backup/archive/status.txt
""".strip()


(
    user_dir
    / "recent_files.txt"
).write_text(
    recent_files + "\n",
    encoding="utf-8"
)


# =========================================================
# USER NOTES - DISTRACTOR
# =========================================================

user_notes = """
Analyst Notes
-------------

- Review login attempts
- Check workstation activity
- Ignore routine backup traffic
- Compare suspicious timestamps carefully
- Cached application files may contain session artefacts
""".strip()


(
    user_dir
    / "case_notes.txt"
).write_text(
    user_notes + "\n",
    encoding="utf-8"
)


# =========================================================
# TODO - DISTRACTOR
# =========================================================

todo = """
TODO
----

1. Update workstation inventory
2. Review training accounts
3. Archive old reports
4. Check authentication anomalies
""".strip()


(
    user_dir
    / "todo.txt"
).write_text(
    todo + "\n",
    encoding="utf-8"
)


# =========================================================
# CACHE INDEX - DISTRACTOR
# =========================================================

cache_index = """
Application Cache Index

cache_item_01.tmp    normal
cache_item_02.tmp    normal
session_4f2a         recovered session artefact
cache_item_04.tmp    expired
""".strip()


(
    cache_dir
    / "cache_index.txt"
).write_text(
    cache_index + "\n",
    encoding="utf-8"
)


# =========================================================
# HIDDEN FORENSIC ARTEFACT
# =========================================================

hidden_session = f"""
CYBERLEARN SESSION RECOVERY

Session ID:
4f2a

Recovered Activity:
The suspicious user accessed a cached investigation record.

Investigation Marker:
{stage4_flag}

NEXT_CLUE:
Some conversations are easier to understand when you follow the stream.
""".strip()


(
    cache_dir
    / ".session_4f2a.log"
).write_text(
    hidden_session + "\n",
    encoding="utf-8"
)


# =========================================================
# CREATE ZIP
# =========================================================

with zipfile.ZipFile(
    OUTPUT_FILE,
    "w",
    compression=zipfile.ZIP_DEFLATED
) as zip_file:

    for file_path in BUILD_DIR.rglob("*"):

        if file_path.is_file():

            archive_name = (
                file_path
                .relative_to(
                    BUILD_DIR
                )
            )

            zip_file.write(
                file_path,
                archive_name
            )


# =========================================================
# REMOVE TEMPORARY BUILD DIRECTORY
# =========================================================

shutil.rmtree(
    BUILD_DIR
)


# =========================================================
# RESULT
# =========================================================

print(
    "Stage 04 challenge created successfully:"
)

print(
    OUTPUT_FILE
)