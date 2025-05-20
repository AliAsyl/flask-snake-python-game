# s30939-python-game

## 🎮 Game Instructions

1. Build the Docker container:

```bash
docker build -t snake-game .
```

2. Run the container:

```bash
docker run -p 5000:5000 snake-game
```

3. Open the game in your browser at:

```
http://localhost:5000/
```

4. Control the Cat using **WASD** keys.

5. The goal of the game is to collect as many points as possible.
Each berry has a random number of points. To win, collect **25 berries**.

---

## ⚙️ CI/CD Pipeline – GitHub Actions

This project uses **GitHub Actions** for automatic testing (CI).

### ✅ What the pipeline does:

- Runs automatically on every **push** to `main` or **pull request**
- Installs required dependencies from `requirements.txt`
- Runs tests using **pytest**

### 🟢 CI Status Badge:

![CI](https://github.com/s30939/s30939-python-game/actions/workflows/ci.yml/badge.svg)
