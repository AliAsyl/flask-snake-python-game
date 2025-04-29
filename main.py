from engine.entities import Cat, Berry, GameObject
from engine.core import Vector2D
from database.db import Database
from database.models import Player, ScoreRecord

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory



import random

player = None
cat = Cat(Vector2D(5, 5), 5)

app = Flask(__name__)
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
    response = {
        "cat":{},
        "berries":[]
    }
    
    for obj in GameObject.GAME_OBJECTS:        
        if isinstance(obj, Cat):
            response["cat"] = {
                "x":obj.hitbox.position.x,
                "y":obj.hitbox.position.y,
                "score": obj.collected_points,
                "berries_collected": obj.collected_berries,
                "berries_required": obj.berries_to_collect,
                "game_over": obj.collected_berries >= obj.berries_to_collect
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
    
    vec = Vector2D(0, 0)
    if direction == 'up':
        vec = vec + Vector2D.DOWN
    elif direction == 'down':
        vec = vec + Vector2D.UP
    elif direction == 'left':
        vec = vec + Vector2D.LEFT
    elif direction == 'right':
        vec = vec + Vector2D.RIGHT
    if random.random() > 0.9:
        Berry(Vector2D(
            random.randint(0,9),
            random.randint(0,9)
        ))

    cat.move_and_collide(vec, cat.move_speed)
    return '', 200



@app.route('/api/start_game', methods=['POST'])
def start_game():
    global player
    data = request.get_json()
    player_name = data.get('player_name')
    player = Player(player_name)
    player.load()
    return '', 200


@app.route('/api/scores/<player_name>', methods=['GET'])
def get_scores(player_name):
    player = Player(player_name)
    if not player.exists():
        return jsonify({"exists": False})
    scores = ScoreRecord.load(player.name)
    return jsonify({
        "exists": True, 
        "scores": [{
            "score": s.score, 
            "collected_berries": s.collected_berries
        } for s in scores]}
    )



def main():
    Database.init()
    
    app.run(debug=True)


if __name__ == "__main__":
    main()