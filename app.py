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
        # Menggunakan endpoint alternatif publik yang aktif dan stabil
        api_endpoint = f"https://api.vhtear.com/smuledl?link={link}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        resp = requests.get(api_endpoint, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            # Menyesuaikan struktur data respons API
            if data.get("status") == 200 or data.get("status") == True:
                res = data.get("result", {})
                return jsonify({
                    "status": True,
                    "result": {
                        "username": res.get("owner", "Unknown"),
                        "title": res.get("title", "Smule Recording"),
                        "type": "audio",
                        "mp3Url": res.get("audio", "") or res.get("url", ""),
                        "mp4Url": res.get("video", ""),
                        "thumbnail": res.get("cover", ""),
                        "created": "-",
                        "listens": "0"
                    }
                })

        # Fallback menggunakan layanan API publik cadangan lainnya
        fallback_endpoint = f"https://itzpire.com/download/smule?url={link}"
        resp2 = requests.get(fallback_endpoint, headers=headers, timeout=15)
        if resp2.status_code == 200:
            data2 = resp2.json()
            if data2.get("status") == "success" and "data" in data2:
                res2 = data2["data"]
                return jsonify({
                    "status": True,
                    "result": {
                        "username": res2.get("owner", "Unknown"),
                        "title": res2.get("title", "Smule Recording"),
                        "type": "audio",
                        "mp3Url": res2.get("audio", ""),
                        "mp4Url": "",
                        "thumbnail": res2.get("cover", ""),
                        "created": "-",
                        "listens": "0"
                    }
                })

        return jsonify({"status": False, "message": "Gagal memproses tautan Smule dari semua jalur perantara."}), 500
            
    except Exception as e:
        return jsonify({"status": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
