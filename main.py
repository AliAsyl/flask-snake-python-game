from engine.entities import Cat, Berry
from engine.core import Vector2D
from database.db import Database

from flask import Flask, request, jsonify
from flask_cors import CORS


import random


def main():
    Database.init()
    cat = Cat(Vector2D(200, 200), 5)

if __name__ == "__main__":
    main()