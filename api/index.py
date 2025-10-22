from flask import Flask, request, jsonify
import requests, json, os
from vercel_wsgi import handle

app = Flask(__name__)

# --- Configuration ---
HALFBLOOD_URL = "https://halfblood.famapp.in/vpa/verifyExt"
RAZORPAY_IFSC_URL = "https://ifsc.razorpay.com/"
HEADERS = {
    'User-Agent': "A015 | Android 15 | Dalvik/2.1.0 | Tetris | 318D0D6589676E17F88CCE03A86C2591C8EBAFBA | (Build -1) | 3DB5HIEMMG",
    'Accept': "application/json",
    'Content-Type': "application/json",
    'authorization': os.getenv("FAMPAY_TOKEN", "Token your_default_token_here")
}

ALLOWED_KEYS = {
    "notfirnkanshs": "Free User",
    "456": "Premium User",
    "keyNever019191": "Admin"
}


def check_api_key(req):
    api_key = req.headers.get("x-api-key") or req.args.get("key")
    if not api_key:
        return False, "Missing API key"
    if api_key not in ALLOWED_KEYS:
        return False, "Invalid API key"
    return True, ALLOWED_KEYS[api_key]


def fetch_and_chain(upi_id):
    try:
        payload = {"upi_string": f"upi://pay?pa={upi_id}"}
        res_vpa = requests.post(HALFBLOOD_URL, data=json.dumps(payload), headers=HEADERS, timeout=10)
        res_vpa.raise_for_status()
        data = res_vpa.json().get("data", {}).get("verify_vpa_resp", {})

        if not data:
            return {"error": "No VPA data found"}, 400

        vpa_details = {
            "name": data.get("name"),
            "vpa": data.get("vpa"),
            "ifsc": data.get("ifsc")
        }

        result = {"vpa_details": vpa_details, "bank_details_raw": None}

        if vpa_details.get("ifsc"):
            ifsc = vpa_details["ifsc"]
            r = requests.get(f"{RAZORPAY_IFSC_URL}{ifsc}", timeout=10)
            if r.status_code == 200:
                result["bank_details_raw"] = r.json()
            else:
                result["bank_details_raw"] = {"error": f"IFSC lookup failed ({r.status_code})"}

        return result, 200

    except Exception as e:
        import traceback
        print("🔥 Internal Error:", traceback.format_exc())
        return {"error": str(e)}, 500


@app.route("/api/upi", methods=["GET"])
def api_upi_lookup():
    valid, message = check_api_key(request)
    if not valid:
        return jsonify({"error": message}), 403

    upi_id = request.args.get("upi_id")
    if not upi_id:
        return jsonify({"error": "Missing required parameter: upi_id"}), 400

    result, status = fetch_and_chain(upi_id)
    return jsonify(result), status


# ✅ Vercel entrypoint
def handler(event, context):
    return handle(app, event, context)
