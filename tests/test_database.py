import pytest
from database.db import Database
from database.models import Player, ScoreRecord

@pytest.fixture(scope="module", autouse=True)
def init_db():
    Database.init()

@pytest.fixture(autouse=True)
def clean_test_data():
    Database.delete("players", {"name": "TestPlayer"})
    Database.delete("scores", {"player_name": "TestPlayer"})
    yield
    Database.delete("players", {"name": "TestPlayer"})
    Database.delete("scores", {"player_name": "TestPlayer"})


def test_create_player():
    player = Player("TestPlayer")
    player.model_create()

    result = Database.read("players", {"name": "TestPlayer"})
    assert len(result) == 1
    assert result[0]["name"] == "TestPlayer"
    assert result[0]["total_score"] == 0


def test_update_player_score():
    player = Player("TestPlayer")
    player.model_create()
    player.add_score(10)

    result = Database.read("players", {"name": "TestPlayer"})
    assert result[0]["total_score"] == 10


def test_load_player_existing_and_non_existing():
    player = Player("TestPlayer")
    player.load()

    result = Database.read("players", {"name": "TestPlayer"})
    assert len(result) == 1

    player.add_score(5)
    reloaded = Player("TestPlayer")
    reloaded.load()
    assert reloaded.total_score == 5


def test_save_score_record():
    record = ScoreRecord("TestPlayer", score=7, collected_berries=3, time="00:02:00")
    record.save()

    results = Database.read("scores", {"player_name": "TestPlayer"})
    assert len(results) == 1
    assert results[0]["score"] == 7
    assert results[0]["collected_berries"] == 3


def test_load_score_records():
    ScoreRecord("TestPlayer", 10, 5, "00:01:30").save()
    ScoreRecord("TestPlayer", 12, 6, "00:01:45").save()

    records = ScoreRecord.load("TestPlayer")
    assert len(records) >= 2
    assert all(r.player_name == "TestPlayer" for r in records)
    assert all(isinstance(r.score, int) for r in records)
