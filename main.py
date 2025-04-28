from engine.entities import Cat, Berry, GameObject
from engine.core import Vector2D
from database.db import Database

from flask import Flask, request, jsonify
from flask_cors import CORS


import random




app = Flask(__name__)
CORS(app)


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




def main():
    Database.init()
    cat = Cat(Vector2D(200, 200), 5)
    app.run(debug=True)


if __name__ == "__main__":
    main()