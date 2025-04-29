from engine.entities import Cat, Berry, GameObject
from engine.core import Vector2D, Rect2D
from database.db import Database
from database.models import Player, ScoreRecord

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory



import random

class GameStatic:
    PLAYER = None
    CAT = None
    GAME_RUNNING = False
    SCREEN_RECT = Rect2D(Vector2D(0,0), 10, 10)

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
    if not(GameStatic.GAME_RUNNING):
        return jsonify({})
    
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
    
    vec = Vector2D(0, 0)
    if direction == 'up':
        vec = vec + Vector2D.DOWN
    elif direction == 'down':
        vec = vec + Vector2D.UP
    elif direction == 'left':
        vec = vec + Vector2D.LEFT
    elif direction == 'right':
        vec = vec + Vector2D.RIGHT

    if GameStatic.GAME_RUNNING:
        if random.random() > 0.9:
            Berry(Vector2D(
                random.randint(0, GameStatic.SCREEN_RECT.width - 1),
                random.randint(0, GameStatic.SCREEN_RECT.height - 1)
            ))
        
        future_hitbox = GameStatic.CAT.hitbox.copy()
        future_hitbox.position += vec * GameStatic.CAT.move_speed
        
        if GameStatic.SCREEN_RECT.is_inner_rect(future_hitbox):
            GameStatic.CAT.move_and_collide(vec, GameStatic.CAT.move_speed)
    return '', 200

@app.route('/api/save_score', methods=['POST'])
def save_score():   
    GameStatic.GAME_RUNNING = False
    GameStatic.PLAYER.add_score(GameStatic.CAT.collected_points)
    ScoreRecord(GameStatic.PLAYER.name, GameStatic.CAT.collected_points, GameStatic.CAT.collected_berries).save()
    return '', 200

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_name = data.get('player_name')
    GameStatic.PLAYER = Player(player_name)
    GameStatic.PLAYER.load()
    GameStatic.CAT = Cat(Vector2D(5, 5), 5)
    GameStatic.GAME_RUNNING = True
    return '', 200


@app.route('/api/scores/<player_name>', methods=['GET'])
def get_scores(player_name):
    GameStatic.PLAYER = Player(player_name)
    if not GameStatic.PLAYER.exists():
        return jsonify({"exists": False})
    scores = ScoreRecord.load(GameStatic.PLAYER.name)
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