from engine.entities import Cat, Berry, GameObject
from engine.core import Vector2D, Rect2D
from database.db import Database
from database.models import Player, ScoreRecord

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
import statics



app = Flask(__name__, static_folder="ui", static_url_path="")
CORS(app)




@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('ui/assets', filename)

@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.get_all_players()
    return jsonify({"players": [{"name": p.name, "total_score": p.total_score, "last_session_time": p.last_session_time} for p in players]})


@app.route('/api/game/state', methods=['GET'])
def game_state():
    if not(statics.GAME_RUNNING):
        return jsonify({})
    

    response = {
        "cat":{},
        "berries":[]
    }
    for obj in GameObject.GAME_OBJECTS:        
        if isinstance(obj, Cat):
            obj.move(statics.SCREEN_RECT)
            response["cat"] = {
                "x":obj.hitbox.position.x,
                "y":obj.hitbox.position.y,
                "tail":[{"x":t.hitbox.position.x, "y":t.hitbox.position.y} for t in obj.tail],
                "score": obj.collected_points,
                "berries_collected": obj.collected_berries,
                "berries_required": obj.berries_to_collect,
                "game_over": (obj.collected_berries >= obj.berries_to_collect) and obj.berries_to_collect != 0
            }
            
        elif isinstance(obj, Berry):
            response["berries"].append({
                "x": obj.hitbox.position.x, 
                "y": obj.hitbox.position.y
            })

    return jsonify(response)


@app.route('/api/move', methods=['POST'])
def game_move():
    data = request.get_json()
    direction = data.get('direction')
    
    if direction == 'up':
        statics.CAT.move_direction = Vector2D.DOWN
    elif direction == 'down':
        statics.CAT.move_direction = Vector2D.UP
    elif direction == 'left':
        statics.CAT.move_direction = Vector2D.LEFT
    elif direction == 'right':
        statics.CAT.move_direction = Vector2D.RIGHT

    return '', 200

@app.route('/api/save_score', methods=['POST'])
def save_score():   
    statics.GAME_RUNNING = False
    statics.PLAYER.add_score(statics.CAT.collected_points)
    ScoreRecord(statics.PLAYER.name, statics.CAT.collected_points, statics.CAT.collected_berries).save()
    return '', 200

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_name = data.get('player_name')
    board_size = data.get('board_size')
    statics.PLAYER = Player(player_name)
    statics.PLAYER.load()
    statics.CAT = Cat(Vector2D(5, 5), 25)
    statics.GAME_RUNNING = True
    statics.SCREEN_RECT = Rect2D(Vector2D(0,0), board_size, board_size)
    Berry.spawn_new_berry()
    return '', 200


@app.route('/api/scores/<player_name>', methods=['GET'])
def get_scores(player_name):
    statics.PLAYER = Player(player_name)
    if not statics.PLAYER.exists():
        return jsonify({"exists": False})
    scores = ScoreRecord.load(statics.PLAYER.name)
    return jsonify({
        "exists": True, 
        "scores": [{
            "score": s.score, 
            "collected_berries": s.collected_berries
        } for s in scores]}
    )

@app.route("/")
def index():
    return send_from_directory("ui", "index.html")


def main():
    Database.init()
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()