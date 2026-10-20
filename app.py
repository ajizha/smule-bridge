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
        # Menggunakan jalur alternatif API publik yang handal untuk melewati blokir Smule
        api_endpoint = f"https://api.vkr.cc/api/download/smule?url={link}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        resp = requests.get(api_endpoint, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") and "result" in data:
                res = data["result"]
                return jsonify({
                    "status": True,
                    "result": {
                        "username": res.get("owner", "Unknown"),
                        "title": res.get("title", "Smule Recording"),
                        "type": "video" if "mp4" in res.get("audio", "") else "audio",
                        "mp3Url": res.get("audio", ""),
                        "mp4Url": res.get("video", "") or res.get("audio", ""),
                        "thumbnail": res.get("cover", ""),
                        "created": "-",
                        "listens": "0"
                    }
                })

        return jsonify({"status": False, "message": "Gagal memproses tautan Smule melalui layanan perantara."}), 500
            
    except Exception as e:
        return jsonify({"status": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
