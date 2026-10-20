# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/smuledl', methods=['GET'])
def smule_downloader():
    link = request.args.get('url')
    if not link:
        return jsonify({"status": False, "message": "URL Smule tidak ditemukan!"}), 400
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/"
        }
        
        # Menggunakan timeout pas agar tidak mengalami gantung (hanging)
        resp = requests.get(link, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            audio_url = ""
            title = "Smule Recording"
            username = "Unknown"
            
            og_audio = soup.find("meta", property="og:audio")
            if og_audio:
                audio_url = og_audio.get("content", "").replace("&amp;", "&")
                
            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = og_title.get("content", "Smule Recording")
                
            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                username = og_desc.get("content", "Unknown")

            if not audio_url:
                match = re.search(r'"performance_url"\s*:\s*"([^"]+)"', resp.text)
                if match:
                    audio_url = match.group(1).replace(r'\u0026', '&').replace('&amp;', '&')

            if audio_url:
                return jsonify({
                    "status": True,
                    "result": {
                        "username": username,
                        "title": title,
                        "type": "audio",
                        "mp3Url": audio_url,
                        "mp4Url": "",
                        "thumbnail": "",
                        "created": "-",
                        "listens": "0"
                    }
                })

        return jsonify({"status": False, "message": "Gagal mengekstrak data dari halaman Smule."}), 500
            
    except Exception as e:
        return jsonify({"status": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
