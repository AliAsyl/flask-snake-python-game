FROM python:3.11-slim

WORKDIR /snake-game

COPY . /snake-game

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]