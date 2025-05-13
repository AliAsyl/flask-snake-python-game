# s30939-python-game

Instruction of Launching the game:

1. Build the container with following command:
```docker build -t snake-game .```
2. launch the container with following command:
```docker run -p 5000:5000 snake-game```
3. Open the http://localhost:5000/ in the browser
3. Control of the Cat is by the WASD keys.

The goal of the game is to collect as much points as possible. Each berry has a random number of points. To win, collect 25 berries.