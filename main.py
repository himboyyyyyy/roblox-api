from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/ccu")
def get_ccu():
    universe_ids = request.args.get("ids")
    if not universe_ids:
        return jsonify({"error": "Missing 'ids' parameter"}), 400

    try:
        url = f"https://games.roblox.com/v1/games?universeIds={universe_ids}"
        headers = {"User-Agent": "Mozilla/5.0"}  # helps avoid blocks
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch from Roblox API"}), 500

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
