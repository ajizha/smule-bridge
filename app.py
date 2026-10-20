# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/smuledl', methods=['GET'])
def smule_downloader():
    link = request.args.get('url')
    if not link:
        return jsonify({"status": False, "message": "URL Smule tidak ditemukan!"}), 400
        
    try:
        # Ekstraksi ID dari URL Smule
        match = re.search(r'([0-9]+_[0-9]+)', link)
        if not match:
            return jsonify({"status": False, "message": "Format URL Smule tidak valid!"}), 400
            
        perf_id = match.group(1)
        api_url = f"https://www.smule.com/recording/_/{perf_id}/json"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": link,
            "X-Requested-With": "XMLHttpRequest"
        }
        
        resp = requests.get(api_url, headers=headers, timeout=12)
        
        if resp.status_code == 200:
            data = resp.json()
            audio_url = data.get("performance_url") or data.get("media_url") or ""
            title = data.get("title", "Smule Recording")
            username = data.get("owner", {}).get("handle", "Unknown")
            
            if not audio_url:
                arr_url = data.get("ensemble", {}).get("performance_url")
                if arr_url:
                    audio_url = arr_url

            if audio_url:
                return jsonify({
                    "status": True,
                    "result": {
                        "username": username,
                        "title": title,
                        "type": "audio",
                        "mp3Url": audio_url,
                        "mp4Url": "",
                        "thumbnail": data.get("cover_url", ""),
                        "created": "-",
                        "listens": str(data.get("listen_count", "0"))
                    }
                })

        return jsonify({"status": False, "message": "Gagal mengambil media dari endpoint Smule."}), 500
            
    except Exception as e:
        return jsonify({"status": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
