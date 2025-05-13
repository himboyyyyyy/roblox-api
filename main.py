from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/ccu")
def get_ccu_with_icons():
    universe_ids = request.args.get("ids")
    if not universe_ids:
        return jsonify({"error": "Missing 'ids' parameter"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        # Step 1: Get game data (includes CCU)
        games_url = f"https://games.roblox.com/v1/games?universeIds={universe_ids}"
        games_response = requests.get(games_url, headers=headers)

        if games_response.status_code != 200:
            return jsonify({"error": "Failed to fetch games data"}), 500

        games_data = games_response.json().get("data", [])

        # Step 2: Get icons
        icons_url = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_ids}&size=512x512&format=Png&isCircular=false"
        icons_response = requests.get(icons_url, headers=headers)

        if icons_response.status_code != 200:
            return jsonify({"error": "Failed to fetch icons"}), 500

        icons_data = icons_response.json().get("data", [])
        icon_map = {str(icon["targetId"]): icon["imageUrl"] for icon in icons_data}

        # Step 3: Combine game data with icons
        combined = []
        for game in games_data:
            universe_id = str(game.get("id"))
            combined.append({
                "universeId": universe_id,
                "name": game.get("name"),
                "playing": game.get("playing"),
                "visits": game.get("visits"),
                "icon": icon_map.get(universe_id, ""),
                "favoritedCount":game.get("favoritedCount")
            })

        return jsonify(combined)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
