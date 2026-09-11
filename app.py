import hashlib
import hmac
import os
import sqlite3
from datetime import timedelta
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegistrationForm


# =========================================================
# BASIC PATHS / ENVIRONMENT
# =========================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env",
    )
)

app = Flask(__name__)


# =========================================================
# SECURITY CONFIGURATION
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")
FLAG_PEPPER = os.getenv("FLAG_PEPPER")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing from .env"
    )

if not FLAG_PEPPER:
    raise RuntimeError(
        "FLAG_PEPPER is missing from .env"
    )


app.config.update(
    SECRET_KEY=SECRET_KEY,

    SESSION_COOKIE_NAME=(
        "cyberlearn_session"
    ),

    SESSION_COOKIE_HTTPONLY=True,

    SESSION_COOKIE_SAMESITE="Lax",

    # Local HTTP development.
    # Change to True only when HTTPS is configured.
    SESSION_COOKIE_SECURE=False,

    PERMANENT_SESSION_LIFETIME=timedelta(
        minutes=30
    ),

    WTF_CSRF_TIME_LIMIT=None,

    MAX_CONTENT_LENGTH=(
        2 * 1024 * 1024
    ),
)


# =========================================================
# CSRF PROTECTION
# =========================================================

csrf = CSRFProtect(app)


# =========================================================
# RATE LIMITING
# =========================================================

limiter = Limiter(
    key_func=get_remote_address,
    app=app,

    default_limits=[
        "300 per day",
        "100 per hour",
    ],

    storage_uri="memory://",
)


# =========================================================
# DATABASE
# =========================================================

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "cyberlearn.db",
)


# =========================================================
# CHALLENGE DEFINITIONS
# =========================================================

CHALLENGES = [

    {
        "id": 1,

        "title": (
            "Hidden in Plain Sight"
        ),

        "domain": (
            "Steganography"
        ),

        "difficulty": (
            "Easy"
        ),

        "objective": (
            "Inspect an image and recover "
            "hidden information."
        ),

        "mission": (
            "A welcome image contains more "
            "information than can be seen at "
            "first glance. Analyse the file "
            "carefully and recover the flag."
        ),
    },


    {
        "id": 2,

        "title": (
            "The Broken Gate"
        ),

        "domain": (
            "Web Security"
        ),

        "difficulty": (
            "Easy"
        ),

        "objective": (
            "Identify intentionally exposed "
            "client-side information inside "
            "a controlled web challenge."
        ),

        "mission": (
            "A restricted interface appears "
            "to protect a hidden resource. "
            "Inspect what the browser receives "
            "and identify the intended weakness."
        ),
    },


    {
        "id": 3,

        "title": (
            "The Encoded Message"
        ),

        "domain": (
            "Cryptography"
        ),

        "difficulty": (
            "Moderate"
        ),

        "objective": (
            "Reverse multiple encoding "
            "and cipher layers."
        ),

        "mission": (
            "A recovered message has been "
            "transformed more than once. "
            "Reverse the layers and recover "
            "the hidden plaintext."
        ),
    },


    {
        "id": 4,

        "title": (
            "Digital Footprints"
        ),

        "domain": (
            "Digital Forensics"
        ),

        "difficulty": (
            "Moderate"
        ),

        "objective": (
            "Follow a forensic evidence "
            "chain across logs and files."
        ),

        "mission": (
            "A collection of digital evidence "
            "contains useful clues and distractors. "
            "Identify the relevant artefact and "
            "follow the trail."
        ),
    },


    {
        "id": 5,

        "title": (
            "Traffic Under Investigation"
        ),

        "domain": (
            "Networking"
        ),

        "difficulty": (
            "Moderate-Hard"
        ),

        "objective": (
            "Analyse captured traffic and "
            "isolate the relevant conversation."
        ),

        "mission": (
            "A packet capture contains several "
            "protocols and background conversations. "
            "Use the previous clue to identify "
            "the traffic that matters."
        ),
    },


    {
        "id": 6,

        "title": (
            "The Misconfigured Server"
        ),

        "domain": (
            "Linux / System Security"
        ),

        "difficulty": (
            "Hard"
        ),

        "objective": (
            "Analyse Linux configuration files, "
            "user privileges and security logs "
            "to identify an insecure privilege "
            "configuration."
        ),

        "mission": (
            "Evidence collected from a simulated "
            "Linux server contains user information, "
            "privilege configuration, authentication "
            "logs and system notes. Analyse the "
            "evidence, identify the intended "
            "privilege-related security weakness, "
            "and follow the evidence chain to "
            "recover the final flag."
        ),
    },

]


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    connection = sqlite3.connect(
        DATABASE,
        timeout=10,
    )

    connection.row_factory = (
        sqlite3.Row
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# =========================================================
# FLAG HASHING
# =========================================================

def flag_digest(
    flag_value
):

    return hmac.new(
        FLAG_PEPPER.encode(
            "utf-8"
        ),

        flag_value.encode(
            "utf-8"
        ),

        hashlib.sha256,

    ).hexdigest()


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    os.makedirs(
        os.path.join(
            BASE_DIR,
            "database",
        ),

        exist_ok=True,
    )

    connection = (
        get_db_connection()
    )

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        );


        CREATE TABLE IF NOT EXISTS challenges (

            id INTEGER PRIMARY KEY,

            title TEXT NOT NULL,

            domain TEXT NOT NULL,

            difficulty TEXT NOT NULL,

            flag_digest TEXT NOT NULL
        );


        CREATE TABLE IF NOT EXISTS progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            stage_id INTEGER NOT NULL,

            completed INTEGER NOT NULL DEFAULT 0,

            completed_at TEXT,

            UNIQUE(
                user_id,
                stage_id
            ),

            FOREIGN KEY(
                user_id
            )
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY(
                stage_id
            )
                REFERENCES challenges(id)
                ON DELETE CASCADE
        );
        """
    )

    connection.commit()

    connection.close()


# =========================================================
# SEED CHALLENGES
# =========================================================

def seed_challenges():

    connection = (
        get_db_connection()
    )

    for challenge in CHALLENGES:

        env_name = (
            f"STAGE{challenge['id']}_FLAG"
        )

        flag_value = os.getenv(
            env_name
        )

        if not flag_value:

            connection.close()

            raise RuntimeError(
                f"{env_name} is missing "
                "from .env"
            )


        connection.execute(
            """
            INSERT INTO challenges (
                id,
                title,
                domain,
                difficulty,
                flag_digest
            )

            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(id)
            DO UPDATE SET

                title = excluded.title,

                domain = excluded.domain,

                difficulty = excluded.difficulty,

                flag_digest = excluded.flag_digest
            """,

            (
                challenge["id"],

                challenge["title"],

                challenge["domain"],

                challenge["difficulty"],

                flag_digest(
                    flag_value
                ),
            ),
        )


    connection.commit()

    connection.close()


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================

def login_required(
    view_function
):

    @wraps(
        view_function
    )

    def wrapped_view(
        *args,
        **kwargs
    ):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "error",
            )

            return redirect(
                url_for(
                    "login"
                )
            )


        return view_function(
            *args,
            **kwargs
        )


    return wrapped_view


# =========================================================
# CHALLENGE HELPERS
# =========================================================

def get_challenge(
    stage_id
):

    return next(

        (
            challenge

            for challenge
            in CHALLENGES

            if challenge["id"]
            == stage_id
        ),

        None,
    )


def get_completed_stages(
    user_id
):

    connection = (
        get_db_connection()
    )


    rows = connection.execute(
        """
        SELECT stage_id

        FROM progress

        WHERE user_id = ?

          AND completed = 1
        """,

        (
            user_id,
        ),

    ).fetchall()


    connection.close()


    return {

        row["stage_id"]

        for row
        in rows
    }


def stage_is_unlocked(
    user_id,
    stage_id
):

    if stage_id == 1:

        return True


    completed = (
        get_completed_stages(
            user_id
        )
    )


    # Completed stages remain accessible.

    if stage_id in completed:

        return True


    # The previous stage must be completed.

    return (
        stage_id - 1
        in completed
    )


# =========================================================
# SECURITY HEADERS
# =========================================================

@app.after_request
def add_security_headers(
    response
):

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"


    response.headers[
        "X-Frame-Options"
    ] = "DENY"


    response.headers[
        "Referrer-Policy"
    ] = (
        "strict-origin-when-cross-origin"
    )


    response.headers[
        "Permissions-Policy"
    ] = (
        "camera=(), "
        "microphone=(), "
        "geolocation=()"
    )


    response.headers[
        "Content-Security-Policy"
    ] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"
    )


    if session.get(
        "user_id"
    ):

        response.headers[
            "Cache-Control"
        ] = (
            "no-store, max-age=0"
        )


    return response


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",

    methods=[
        "GET",
        "POST",
    ],
)

@limiter.limit(
    "8 per minute"
)
def register():

    if "user_id" in session:

        return redirect(
            url_for(
                "dashboard"
            )
        )


    form = (
        RegistrationForm()
    )


    if form.validate_on_submit():

        username = (
            form.username.data
            .strip()
            .casefold()
        )


        email = (
            form.email.data
            .strip()
            .lower()
        )


        password_hash = (
            generate_password_hash(
                form.password.data
            )
        )


        connection = (
            get_db_connection()
        )


        existing = (
            connection.execute(
                """
                SELECT id

                FROM users

                WHERE username = ?

                   OR email = ?
                """,

                (
                    username,
                    email,
                ),

            ).fetchone()
        )


        if existing:

            connection.close()


            flash(
                "Username or email "
                "already exists.",
                "error",
            )


            return render_template(
                "register.html",

                form=form,
            )


        connection.execute(
            """
            INSERT INTO users (
                username,
                email,
                password_hash
            )

            VALUES (?, ?, ?)
            """,

            (
                username,
                email,
                password_hash,
            ),
        )


        connection.commit()

        connection.close()


        flash(
            "Account created successfully. "
            "You can now login.",
            "success",
        )


        return redirect(
            url_for(
                "login"
            )
        )


    return render_template(
        "register.html",

        form=form,
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",

    methods=[
        "GET",
        "POST",
    ],
)

@limiter.limit(
    "8 per minute"
)
def login():

    if "user_id" in session:

        return redirect(
            url_for(
                "dashboard"
            )
        )


    form = LoginForm()


    if form.validate_on_submit():

        username = (
            form.username.data
            .strip()
            .casefold()
        )


        connection = (
            get_db_connection()
        )


        user = connection.execute(
            """
            SELECT *

            FROM users

            WHERE username = ?
            """,

            (
                username,
            ),

        ).fetchone()


        connection.close()


        if user and check_password_hash(
            user["password_hash"],

            form.password.data,
        ):

            # Prevent session fixation.
            session.clear()


            session[
                "user_id"
            ] = user["id"]


            session[
                "username"
            ] = user["username"]


            session.permanent = True


            flash(
                "Login successful.",
                "success",
            )


            return redirect(
                url_for(
                    "dashboard"
                )
            )


        flash(
            "Invalid username "
            "or password.",
            "error",
        )


    return render_template(
        "login.html",

        form=form,
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route(
    "/logout",

    methods=[
        "POST"
    ],
)

@login_required
def logout():

    session.clear()


    flash(
        "You have been logged out.",
        "success",
    )


    return redirect(
        url_for(
            "home"
        )
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route(
    "/dashboard"
)

@login_required
def dashboard():

    user_id = (
        session[
            "user_id"
        ]
    )


    completed = (
        get_completed_stages(
            user_id
        )
    )


    cards = []


    for challenge in CHALLENGES:

        item = (
            challenge.copy()
        )


        item[
            "completed"
        ] = (
            challenge["id"]
            in completed
        )


        item[
            "unlocked"
        ] = (
            stage_is_unlocked(
                user_id,

                challenge["id"],
            )
        )


        cards.append(
            item
        )


    return render_template(
        "dashboard.html",

        challenges=cards,

        completed_count=len(
            completed
        ),
    )


# =========================================================
# CHALLENGE PAGE
# =========================================================

@app.route(
    "/challenge/<int:stage_id>"
)

@login_required
def challenge(
    stage_id
):

    challenge_data = (
        get_challenge(
            stage_id
        )
    )


    if challenge_data is None:

        abort(404)


    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        stage_id,
    ):

        flash(
            "Complete the previous stage "
            "before opening this challenge.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    completed = (

        stage_id

        in get_completed_stages(
            user_id
        )
    )


    return render_template(
        "challenge.html",

        challenge=challenge_data,

        completed=completed,
    )


# =========================================================
# STAGE 01 DOWNLOAD
# =========================================================

@app.route(
    "/challenge/1/download"
)

@login_required
def download_stage01():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        1,
    ):

        abort(403)


    stage_directory = (
        os.path.join(
            BASE_DIR,
            "challenges",
            "stage01",
        )
    )


    file_path = (
        os.path.join(
            stage_directory,
            "welcome.png",
        )
    )


    if not os.path.isfile(
        file_path
    ):

        flash(
            "Stage 01 challenge file "
            "is not available yet.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=1,
            )
        )


    return send_from_directory(
        stage_directory,

        "welcome.png",

        as_attachment=True,

        download_name=(
            "welcome.png"
        ),
    )


# =========================================================
# STAGE 02 - THE BROKEN GATE
# =========================================================

@app.route(
    "/challenge/2/gate"
)

@login_required
def stage02_gate():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        2,
    ):

        flash(
            "Complete Stage 01 before "
            "accessing Stage 02.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    return render_template(
        "stage02/gate.html"
    )


# =========================================================
# STAGE 02 CLIENT-SIDE JAVASCRIPT
# Intentionally vulnerable challenge component
# =========================================================

@app.route(
    "/challenge/2/gate.js"
)

@login_required
def stage02_script():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        2,
    ):

        abort(403)


    stage2_flag = (
        os.getenv(
            "STAGE2_FLAG"
        )
    )


    if not stage2_flag:

        abort(500)


    access_code = (
        "CYBERLEARN-GATE-2026"
    )


    javascript = (
        render_template(
            "stage02/gate.js.j2",

            access_code=access_code,

            stage2_flag=stage2_flag,
        )
    )


    response = (
        make_response(
            javascript
        )
    )


    response.headers[
        "Content-Type"
    ] = (
        "application/javascript; "
        "charset=utf-8"
    )


    response.headers[
        "Cache-Control"
    ] = (
        "no-store, max-age=0"
    )


    return response


# =========================================================
# STAGE 03 DOWNLOAD
# =========================================================

@app.route(
    "/challenge/3/download"
)

@login_required
def download_stage03():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        3,
    ):

        flash(
            "Complete Stage 02 before "
            "accessing Stage 03.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    stage_directory = (
        os.path.join(
            BASE_DIR,
            "challenges",
            "stage03",
        )
    )


    file_path = (
        os.path.join(
            stage_directory,
            "message.txt",
        )
    )


    if not os.path.isfile(
        file_path
    ):

        flash(
            "Stage 03 challenge file "
            "is not available yet.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=3,
            )
        )


    return send_from_directory(
        stage_directory,

        "message.txt",

        as_attachment=True,

        download_name=(
            "message.txt"
        ),
    )


# =========================================================
# STAGE 04 DOWNLOAD
# =========================================================

@app.route(
    "/challenge/4/download"
)

@login_required
def download_stage04():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        4,
    ):

        flash(
            "Complete Stage 03 before "
            "accessing Stage 04.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    stage_directory = (
        os.path.join(
            BASE_DIR,
            "challenges",
            "stage04",
        )
    )


    file_path = (
        os.path.join(
            stage_directory,
            "evidence.zip",
        )
    )


    if not os.path.isfile(
        file_path
    ):

        flash(
            "Stage 04 evidence file "
            "is not available yet.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=4,
            )
        )


    return send_from_directory(
        stage_directory,

        "evidence.zip",

        as_attachment=True,

        download_name=(
            "evidence.zip"
        ),
    )


# =========================================================
# STAGE 05 DOWNLOAD
# =========================================================

@app.route(
    "/challenge/5/download"
)

@login_required
def download_stage05():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        5,
    ):

        flash(
            "Complete Stage 04 before "
            "accessing Stage 05.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    stage_directory = (
        os.path.join(
            BASE_DIR,
            "challenges",
            "stage05",
        )
    )


    file_path = (
        os.path.join(
            stage_directory,
            "traffic_capture.pcap",
        )
    )


    if not os.path.isfile(
        file_path
    ):

        flash(
            "Stage 05 packet capture "
            "is not available yet.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=5,
            )
        )


    return send_from_directory(
        stage_directory,

        "traffic_capture.pcap",

        as_attachment=True,

        download_name=(
            "traffic_capture.pcap"
        ),
    )


# =========================================================
# STAGE 06 DOWNLOAD
# =========================================================

@app.route(
    "/challenge/6/download"
)

@login_required
def download_stage06():

    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        6,
    ):

        flash(
            "Complete Stage 05 before "
            "accessing Stage 06.",
            "error",
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    stage_directory = (
        os.path.join(
            BASE_DIR,
            "challenges",
            "stage06",
        )
    )


    file_path = (
        os.path.join(
            stage_directory,
            "stage06_evidence.zip",
        )
    )


    if not os.path.isfile(
        file_path
    ):

        flash(
            "Stage 06 evidence package "
            "is not available yet.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=6,
            )
        )


    return send_from_directory(
        stage_directory,

        "stage06_evidence.zip",

        as_attachment=True,

        download_name=(
            "stage06_evidence.zip"
        ),
    )


# =========================================================
# FLAG SUBMISSION
# =========================================================

@app.route(
    "/challenge/<int:stage_id>/submit",

    methods=[
        "POST"
    ],
)

@login_required

@limiter.limit(
    "15 per minute"
)
def submit_flag(
    stage_id
):

    challenge_data = (
        get_challenge(
            stage_id
        )
    )


    if challenge_data is None:

        abort(404)


    user_id = (
        session[
            "user_id"
        ]
    )


    if not stage_is_unlocked(
        user_id,
        stage_id,
    ):

        abort(403)


    submitted_flag = (
        request.form.get(
            "flag",
            "",
        )
        .strip()
    )


    if (
        not submitted_flag

        or len(
            submitted_flag
        ) > 200
    ):

        flash(
            "Please enter a valid flag.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=stage_id,
            )
        )


    connection = (
        get_db_connection()
    )


    record = connection.execute(
        """
        SELECT flag_digest

        FROM challenges

        WHERE id = ?
        """,

        (
            stage_id,
        ),

    ).fetchone()


    if record is None:

        connection.close()

        abort(404)


    is_valid = (
        hmac.compare_digest(

            record[
                "flag_digest"
            ],

            flag_digest(
                submitted_flag
            ),
        )
    )


    if not is_valid:

        connection.close()


        flash(
            "Incorrect flag. "
            "Check your evidence "
            "and try again.",
            "error",
        )


        return redirect(
            url_for(
                "challenge",

                stage_id=stage_id,
            )
        )


    connection.execute(
        """
        INSERT INTO progress (
            user_id,
            stage_id,
            completed,
            completed_at
        )

        VALUES (
            ?,
            ?,
            1,
            CURRENT_TIMESTAMP
        )

        ON CONFLICT(
            user_id,
            stage_id
        )

        DO UPDATE SET

            completed = 1,

            completed_at = COALESCE(
                progress.completed_at,
                CURRENT_TIMESTAMP
            )
        """,

        (
            user_id,
            stage_id,
        ),
    )


    connection.commit()

    connection.close()


    if stage_id == 6:

        flash(
            "Congratulations! "
            "You completed the "
            "CyberLearn CTF.",
            "success",
        )


    else:

        flash(
            f"Stage {stage_id:02d} "
            "completed. "
            f"Stage {stage_id + 1:02d} "
            "is now unlocked.",
            "success",
        )


    return redirect(
        url_for(
            "dashboard"
        )
    )


# =========================================================
# CSRF ERROR
# =========================================================

@app.errorhandler(
    CSRFError
)
def handle_csrf_error(
    error
):

    flash(
        "Security token is invalid. "
        "Refresh the page and try again.",
        "error",
    )


    if session.get(
        "user_id"
    ):

        return redirect(
            url_for(
                "dashboard"
            )
        )


    return redirect(
        url_for(
            "home"
        )
    )


# =========================================================
# 403
# =========================================================

@app.errorhandler(403)
def forbidden(
    error
):

    return render_template(
        "error.html",

        code=403,

        title=(
            "Access Denied"
        ),

        message=(
            "You do not have permission "
            "to access this resource."
        ),

    ), 403


# =========================================================
# 404
# =========================================================

@app.errorhandler(404)
def not_found(
    error
):

    return render_template(
        "error.html",

        code=404,

        title=(
            "Page Not Found"
        ),

        message=(
            "The requested CyberLearn "
            "resource could not be found."
        ),

    ), 404


# =========================================================
# 429
# =========================================================

@app.errorhandler(429)
def too_many_requests(
    error
):

    return render_template(
        "error.html",

        code=429,

        title=(
            "Too Many Requests"
        ),

        message=(
            "Too many requests were "
            "received. Wait a moment "
            "and try again."
        ),

    ), 429


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()

seed_challenges()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )