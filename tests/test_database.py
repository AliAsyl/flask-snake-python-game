import pytest
from database.db import Database
from database.models import Player, ScoreRecord


@pytest.fixture(scope="module", autouse=True)
def init_db():
    Database.init()


@pytest.fixture(autouse=True)
def clean_db():
    Database.delete("players", {"name": "TestPlayer"})
    Database.delete("players", {"name": "Ghost"})
    Database.delete("scores", {"player_name": "TestPlayer"})
    Database.delete("scores", {"player_name": "Ghost"})
    yield
    Database.delete("players", {"name": "TestPlayer"})
    Database.delete("players", {"name": "Ghost"})
    Database.delete("scores", {"player_name": "TestPlayer"})
    Database.delete("scores", {"player_name": "Ghost"})


# ----- Player tests -----

def test_player_model_create_standard():
    player = Player("TestPlayer")
    player.model_create()
    assert player.exists()

def test_player_model_create_edge_duplicate_insert():
    player = Player("TestPlayer")
    player.model_create()
    player.model_create()  # Should not crash
    result = Database.read("players", {"name": "TestPlayer"})
    assert len(result) >= 1


def test_player_load_standard():
    player = Player("TestPlayer")
    player.load()
    assert player.exists()

def test_player_load_edge_missing_creates():
    ghost = Player("Ghost")
    ghost.load()
    assert ghost.exists()


def test_player_add_score_standard():
    player = Player("TestPlayer")
    player.load()
    previous_score = player.total_score
    player.add_score(10)
    updated = Database.read("players", {"name": "TestPlayer"})[0]
    assert updated["total_score"] == previous_score + 10
    assert updated["last_session_time"] != ""


def test_player_add_score_edge_zero_score():
    player = Player("TestPlayer")
    player.load()
    prev = player.total_score
    player.add_score(0)
    current = Database.read("players", {"name": "TestPlayer"})[0]["total_score"]
    assert current == prev


def test_get_all_players_standard():
    Player("TestPlayer").model_create()
    all_players = Player.get_all_players()
    assert any(p.name == "TestPlayer" for p in all_players)

def test_get_all_players_edge_empty():
    while True:
        all_players = Player.get_all_players()
        if not all_players:
            break
        for player in all_players:
            Database.delete("players", {"name": player.name})

    assert Player.get_all_players() == []



# ----- ScoreRecord tests -----

def test_score_record_save_standard():
    record = ScoreRecord("TestPlayer", 5, 3)
    record.save()
    result = Database.read("scores", {"player_name": "TestPlayer"})
    assert len(result) >= 1

def test_score_record_save_edge_empty_name():
    record = ScoreRecord("", 1, 1)
    record.save()
    result = Database.read("scores", {"player_name": ""})
    assert len(result) >= 1


def test_score_record_load_standard():
    ScoreRecord("TestPlayer", 8, 2).save()
    results = ScoreRecord.load("TestPlayer")
    assert any(r.score == 8 and r.collected_berries == 2 for r in results)

def test_score_record_load_edge_no_results():
    results = ScoreRecord.load("Ghost")
    assert results == []
