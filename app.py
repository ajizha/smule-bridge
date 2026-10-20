# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/smuledl', methods=['GET'])
def smule_downloader():
    link = request.args.get('url')
    if not link:
        return jsonify({"status": False, "message": "URL Smule tidak ditemukan!"}), 400
        
    try:
        # Menggunakan jalur API publik cepat khusus pengunduh Smule
        api_endpoint = f"https://itzpire.com/download/smule?url={link}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        resp = requests.get(api_endpoint, headers=headers, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and "data" in data:
                res = data["data"]
                return jsonify({
                    "status": True,
                    "result": {
                        "username": res.get("owner", "Unknown"),
                        "title": res.get("title", "Smule Recording"),
                        "type": "audio",
                        "mp3Url": res.get("audio", ""),
                        "mp4Url": "",
                        "thumbnail": res.get("cover", ""),
                        "created": "-",
                        "listens": "0"
                    }
                })

        return jsonify({"status": False, "message": "Gagal merespons dari server unduhan."}), 500
            
    except Exception as e:
        return jsonify({"status": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
