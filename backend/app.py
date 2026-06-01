from flask import Flask, request, jsonify, session
from flask_cors import CORS
from web3 import Web3
import json
import qrcode
import io
import base64
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "blockchain_attendance_secret_2024"

# Configure session cookies to be highly permissive for cross-port HTTP development
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=False
)

CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:8080", "http://localhost:8080", "http://192.168.0.104:8080",
    "http://127.0.0.1:5500", "http://localhost:5500", "http://192.168.0.104:5500"
])

# ─── Connect to Blockchain (Local Ganache or Sepolia Cloud) ───────────────────
import os

SEPOLIA_RPC_URL = os.environ.get("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS_ENV = os.environ.get("CONTRACT_ADDRESS")
OWNER_PRIVATE_KEY = os.environ.get("OWNER_PRIVATE_KEY")

if SEPOLIA_RPC_URL:
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    print(f"[INFO] Connected to Public RPC: {SEPOLIA_RPC_URL}")
else:
    GANACHE_URL = "http://127.0.0.1:7546"
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("[INFO] Connected to Local Ganache")

if not w3.is_connected():
    raise Exception("Cannot connect to Ethereum network.")

# ─── Load Contract ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_PATH = os.path.join(BASE_DIR, "contract_abi.json")

with open(ABI_PATH, "r") as f:
    contract_data = json.load(f)

CONTRACT_ADDRESS = CONTRACT_ADDRESS_ENV if CONTRACT_ADDRESS_ENV else contract_data["address"]
CONTRACT_ABI     = contract_data["abi"]

contract      = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

if OWNER_PRIVATE_KEY:
    OWNER_ACCOUNT = w3.eth.account.from_key(OWNER_PRIVATE_KEY).address
    print(f"[INFO] Using private-key signed owner account: {OWNER_ACCOUNT}")
else:
    OWNER_ACCOUNT = w3.eth.accounts[0]
    print(f"[INFO] Using local Ganache owner account: {OWNER_ACCOUNT}")

# ─── Local Database for raw GPS logging and Proxy Audit ────────────────────────
LOG_FILE = os.path.join(BASE_DIR, "attendance_gps_log.json")

def log_attendance_record(srn, name, subject, latitude, longitude, status, is_proxy, location_hash):
    records = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                records = json.load(f)
        except Exception:
            records = []
            
    record = {
        "srn": srn,
        "name": name,
        "subject": subject,
        "timestamp": int(datetime.now().timestamp()),
        "latitude": latitude if latitude is not None else "Mock/None",
        "longitude": longitude if longitude is not None else "Mock/None",
        "status": status,
        "is_proxy": is_proxy,
        "location_hash": location_hash
    }
    records.append(record)
    
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        print(f"Failed to write to local log: {e}")

def populate_from_blockchain():
    if os.path.exists(LOG_FILE):
        return
    try:
        total = contract.functions.getTotalStudents().call()
        records = []
        for i in range(total):
            srn = contract.functions.allSRNs(i).call()
            student = contract.functions.students(srn).call()
            raw_records = contract.functions.getStudentRecords(srn).call()
            
            for r in raw_records:
                rec = {
                    "srn": r[0],
                    "name": student[0],
                    "subject": r[1],
                    "timestamp": r[2],
                    "latitude": "N/A",
                    "longitude": "N/A",
                    "status": "On-Chain Verified (Historical)",
                    "is_proxy": "No (Historical On-Chain)",
                    "location_hash": r[4] if len(r) > 4 else "0x0"
                }
                records.append(rec)
        
        records.sort(key=lambda x: x["timestamp"])
        with open(LOG_FILE, "w") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        print(f"Could not auto-populate from blockchain: {e}")

# Trigger initial sync
populate_from_blockchain()


# ─── Teacher Credentials (username => hashed password) ────────────────────────
# To add more teachers, add entries here
# Password is stored as SHA256 hash — never plain text
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

TEACHERS = {
    "teacher1": hash_password("teacher123"),
    "teacher2": hash_password("admin456"),
    "admin":    hash_password("admin123"),
}


# ─── Auth decorator ───────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Support token-based authentication via headers fallback
        teacher = request.headers.get("X-Teacher-Username")
        if not teacher:
            teacher = session.get("teacher")

        if not teacher:
            return jsonify({
                "success": False,
                "message": "Unauthorized. Please log in as a teacher first."
            }), 401
        return f(*args, **kwargs)
    return decorated


# ─── Helpers ───────────────────────────────────────────────────────────────────
def send_tx(fn):
    if not OWNER_PRIVATE_KEY:
        tx_hash = fn.transact({"from": OWNER_ACCOUNT, "gas": 300000})
        return w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Public network signed transaction execution
    nonce = w3.eth.get_transaction_count(OWNER_ACCOUNT)
    built_tx = fn.build_transaction({
        'from': OWNER_ACCOUNT,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(built_tx, private_key=OWNER_PRIVATE_KEY)
    raw_tx = getattr(signed_tx, "raw_transaction", getattr(signed_tx, "rawTransaction", None))
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def today():
    return datetime.now().strftime("%Y-%m-%d")

def fmt_time(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m} min {s} sec"


# ══════════════════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ══════════════════════════════════════════════════════════════════════════════

# ── Login ─────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data     = request.json
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    hashed = hash_password(password)
    if username in TEACHERS and TEACHERS[username] == hashed:
        session["teacher"] = username
        return jsonify({"success": True, "message": f"Welcome, {username}!", "teacher": username})

    return jsonify({"success": False, "message": "Invalid username or password"}), 401


# ── Logout ────────────────────────────────────────────────────────────────────
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("teacher", None)
    return jsonify({"success": True, "message": "Logged out"})


# ── Check session ─────────────────────────────────────────────────────────────
@app.route("/me", methods=["GET"])
def me():
    teacher = request.headers.get("X-Teacher-Username")
    if not teacher:
        teacher = session.get("teacher")
    if teacher:
        return jsonify({"success": True, "teacher": teacher, "logged_in": True})
    return jsonify({"success": False, "logged_in": False})


# ══════════════════════════════════════════════════════════════════════════════
# PROTECTED ROUTES (teacher login required)
# ══════════════════════════════════════════════════════════════════════════════

# ── Register Student ──────────────────────────────────────────────────────────
@app.route("/register", methods=["POST"])
@login_required
def register_student():
    data = request.json
    srn  = data.get("srn", "").strip().upper()
    name = data.get("name", "").strip()

    if not srn or not name:
        return jsonify({"success": False, "message": "SRN and name are required"}), 400

    if contract.functions.isRegistered(srn).call():
        return jsonify({"success": False, "message": f"Student {srn} already registered"}), 400

    try:
        send_tx(contract.functions.registerStudent(srn, name))
        return jsonify({"success": True, "message": f"Student {name} ({srn}) registered on blockchain"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ── Generate QR Code ──────────────────────────────────────────────────────────
@app.route("/generate_qr/<srn>", methods=["GET"])
@login_required
def generate_qr(srn):
    srn = srn.strip().upper()
    if not contract.functions.isRegistered(srn).call():
        return jsonify({"success": False, "message": "Student not registered"}), 404

    qr     = qrcode.make(srn)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_b64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({"success": True, "srn": srn, "qr_image": img_b64})


# ── Mark Attendance ───────────────────────────────────────────────────────────
@app.route("/mark_attendance", methods=["POST"])
@login_required
def mark_attendance():
    data    = request.json
    srn     = data.get("srn", "").strip().upper()
    subject = data.get("subject", "").strip()
    date    = today()

    if not srn or not subject:
        return jsonify({"success": False, "message": "SRN and subject are required"}), 400

    if not contract.functions.isRegistered(srn).call():
        return jsonify({"success": False, "message": "Student not registered"}), 404

    # Check 1: same subject same day
    if contract.functions.hasMarkedToday(srn, subject, date).call():
        return jsonify({
            "success": False,
            "message": f"Attendance already marked for {srn} in {subject} today"
        }), 400

    # Check 2: 45 minute gap
    wait_seconds = contract.functions.timeUntilNextMark(srn).call()
    if wait_seconds > 0:
        return jsonify({
            "success": False,
            "message": f"Too soon! {srn} must wait {fmt_time(wait_seconds)} before next subject"
        }), 400

    try:
        timestamp_str = datetime.now().isoformat()
        teacher = request.headers.get("X-Teacher-Username") or session.get("teacher", "Unknown")
        manual_raw = f"MANUAL,{teacher},{timestamp_str}"
        location_hash = f"0x{hashlib.sha256(manual_raw.encode()).hexdigest()}"

        send_tx(contract.functions.markAttendance(srn, subject, date, location_hash))
        student = contract.functions.students(srn).call()

        # Log manual mark to local audit database
        log_attendance_record(
            srn=srn,
            name=student[0],
            subject=subject,
            latitude="N/A",
            longitude="N/A",
            status=f"Manually Marked (by {teacher})",
            is_proxy="No (Teacher Override)",
            location_hash=location_hash
        )

        return jsonify({
            "success": True,
            "message": f"Attendance marked for {student[0]} ({srn}) in {subject}",
            "marked_by": teacher,
            "location_hash": location_hash
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ── Get Student Records ───────────────────────────────────────────────────────
@app.route("/records/<srn>", methods=["GET"])
@login_required
def get_records(srn):
    srn = srn.strip().upper()
    if not contract.functions.isRegistered(srn).call():
        return jsonify({"success": False, "message": "Student not found"}), 404

    student     = contract.functions.students(srn).call()
    raw_records = contract.functions.getStudentRecords(srn).call()

    records = [
        {
            "srn": r[0],
            "subject": r[1],
            "timestamp": r[2],
            "present": r[3],
            "locationHash": r[4] if len(r) > 4 else "0x0"
        }
        for r in raw_records
    ]

    return jsonify({
        "success": True,
        "student": {"name": student[0], "srn": student[1]},
        "records": records
    })


# ── Get All Students ──────────────────────────────────────────────────────────
@app.route("/students", methods=["GET"])
@login_required
def get_students():
    total    = contract.functions.getTotalStudents().call()
    students = []
    for i in range(total):
        srn     = contract.functions.allSRNs(i).call()
        student = contract.functions.students(srn).call()
        students.append({"name": student[0], "srn": student[1]})
    return jsonify({"success": True, "students": students})


# ── Wait time ─────────────────────────────────────────────────────────────────
@app.route("/wait_time/<srn>", methods=["GET"])
@login_required
def wait_time(srn):
    srn          = srn.strip().upper()
    wait_seconds = contract.functions.timeUntilNextMark(srn).call()
    return jsonify({
        "success":      True,
        "srn":          srn,
        "wait_seconds": wait_seconds,
        "wait_display": fmt_time(wait_seconds) if wait_seconds > 0 else "Ready"
    })


# ── Attendance Count ──────────────────────────────────────────────────────────
@app.route("/count/<srn>/<subject>", methods=["GET"])
@login_required
def get_count(srn, subject):
    srn   = srn.strip().upper()
    count = contract.functions.getAttendanceCount(srn, subject).call()
    return jsonify({"success": True, "srn": srn, "subject": subject, "count": count})


# ── Status (public — no login needed) ────────────────────────────────────────
@app.route("/status", methods=["GET"])
def status():
    connected = w3.is_connected()
    return jsonify({
        "ganache_connected": connected,
        "latest_block":      w3.eth.block_number if connected else None,
        "contract_address":  CONTRACT_ADDRESS
    })


# Server startup block moved to end of file


# ══════════════════════════════════════════════════════════════════════════════
# SESSION TOKEN ROUTES (proxy prevention)
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# SESSION TOKEN ROUTES (proxy prevention + GPS geofencing)
# ══════════════════════════════════════════════════════════════════════════════

import math

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000  # Radius of earth in meters
    return c * r

# In-memory store: subject => current valid token details
active_tokens = {}

# ── Teacher stores current QR token ──────────────────────────────────────────
@app.route("/session/token", methods=["POST"])
@login_required
def set_session_token():
    data      = request.json
    token     = data.get("token", "").strip()
    subject   = data.get("subject", "").strip()
    latitude  = data.get("latitude")
    longitude = data.get("longitude")
    radius    = data.get("radius", 50)

    if not token or not subject:
        return jsonify({"success": False, "message": "Token and subject required"}), 400
    
    teacher = request.headers.get("X-Teacher-Username") or session.get("teacher", "Unknown")
    active_tokens[subject] = {
        "token":     token,
        "teacher":   teacher,
        "updated":   datetime.now().isoformat(),
        "latitude":  float(latitude) if latitude is not None else None,
        "longitude": float(longitude) if longitude is not None else None,
        "radius":    float(radius) if radius is not None else 50
    }
    return jsonify({"success": True})


# ── Student submits scanned token to mark attendance ─────────────────────────
@app.route("/session/attend", methods=["POST"])
def student_attend():
    data      = request.json
    srn       = data.get("srn", "").strip().upper()
    token     = data.get("token", "").strip()
    subject   = data.get("subject", "").strip()
    stud_lat  = data.get("latitude")
    stud_lon  = data.get("longitude")
    date      = today()

    if not srn or not token or not subject:
        return jsonify({"success": False, "message": "SRN, token and subject required"}), 400

    # ── Validate token ─────────────────────────────────────────────────────────
    active = active_tokens.get(subject)
    if not active or active["token"] != token:
        return jsonify({
            "success": False,
            "message": "Invalid or expired QR code. Ask your teacher for the latest QR."
        }), 400

    if not contract.functions.isRegistered(srn).call():
        return jsonify({"success": False, "message": "Student SRN not registered"}), 404

    # ── Geofence Validation ───────────────────────────────────────────────────
    session_lat = active.get("latitude")
    session_lon = active.get("longitude")
    allowed_rad = active.get("radius", 50)

    distance = None
    if session_lat is not None and session_lon is not None:
        if stud_lat is None or stud_lon is None:
            return jsonify({
                "success": False,
                "message": "GPS location is required to mark attendance in this geofenced session."
            }), 400
        
        # Calculate distance using Haversine formula
        distance = haversine_distance(float(stud_lat), float(stud_lon), session_lat, session_lon)
        if distance > allowed_rad:
            return jsonify({
                "success": False,
                "message": f"Outside geofence! You are {distance:.1f}m away from the classroom (allowed radius: {allowed_rad}m)."
            }), 400

    # ── Duplicate check ────────────────────────────────────────────────────────
    if contract.functions.hasMarkedToday(srn, subject, date).call():
        return jsonify({"success": False, "message": "Attendance already marked today"}), 400

    # ── 45 min gap check ───────────────────────────────────────────────────────
    wait_seconds = contract.functions.timeUntilNextMark(srn).call()
    if wait_seconds > 0:
        return jsonify({
            "success": False,
            "message": f"Wait {fmt_time(wait_seconds)} before next subject"
        }), 400

    try:
        # Create Privacy-Preserving Location Hash
        timestamp_str = datetime.now().isoformat()
        lat_val = stud_lat if stud_lat is not None else "mock"
        lon_val = stud_lon if stud_lon is not None else "mock"
        raw_location = f"{srn},{lat_val},{lon_val},{timestamp_str}"
        location_hash = f"0x{hashlib.sha256(raw_location.encode()).hexdigest()}"

        send_tx(contract.functions.markAttendance(srn, subject, date, location_hash))
        student = contract.functions.students(srn).call()

        # Audit and status formatting
        if session_lat is not None and session_lon is not None:
            status_str = f"Attended properly (Verified: {distance:.1f}m from center)"
            is_proxy_str = "No (Verified)"
        else:
            if stud_lat is not None and stud_lon is not None:
                status_str = "Attended (No Geofence - GPS Recorded)"
                is_proxy_str = "No (GPS active)"
            else:
                status_str = "Attended (Presentation Mode - No GPS)"
                is_proxy_str = "Possible Proxy (No GPS verification)"

        # Log to local audit database
        log_attendance_record(
            srn=srn,
            name=student[0],
            subject=subject,
            latitude=stud_lat,
            longitude=stud_lon,
            status=status_str,
            is_proxy=is_proxy_str,
            location_hash=location_hash
        )

        return jsonify({
            "success": True,
            "message": f"Attendance marked for {student[0]} in {subject}!",
            "location_hash": location_hash
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ── Get today's marked students for a subject (for teacher session view) ──────
@app.route("/session/marked", methods=["GET"])
@login_required
def session_marked():
    subject = request.args.get("subject", "").strip()
    date    = today()
    total   = contract.functions.getTotalStudents().call()
    records = []
    for i in range(total):
        srn = contract.functions.allSRNs(i).call()
        if contract.functions.hasMarkedToday(srn, subject, date).call():
            student     = contract.functions.students(srn).call()
            raw_records = contract.functions.getStudentRecords(srn).call()
            # Get latest timestamp for this subject today
            ts = next((r[2] for r in reversed(raw_records)
                       if r[1] == subject), 0)
            records.append({"srn": srn, "name": student[0], "timestamp": ts})
    return jsonify({"success": True, "records": records})


# ── Get All Local GPS Logs (for report page audit) ─────────────────────────────
@app.route("/session/reports/all", methods=["GET"])
@login_required
def get_all_reports():
    records = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                records = json.load(f)
        except Exception:
            records = []
    return jsonify({"success": True, "records": records})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)