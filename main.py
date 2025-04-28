from engine.entities import Cat, Berry, GameObject
from engine.core import Vector2D
from database.db import Database
from database.models import Player

from flask import Flask, request, jsonify
from flask_cors import CORS


import random


cat = Cat(Vector2D(200, 200), 5)

app = Flask(__name__)
CORS(app)



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


@app.route('/api/game/move', methods=['POST'])
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

    cat.move_and_collide(vec, cat.move_speed)
    return '', 200

def main():
    Database.init()
    
    app.run(debug=True)


if __name__ == "__main__":
    main()