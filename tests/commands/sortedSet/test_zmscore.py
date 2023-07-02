import pytest
from tests.sync_client import redis

@pytest.fixture(autouse=True)
def flush_sorted_set():
    sorted_set = "sorted_set"

    redis.delete(sorted_set)

def test_zmscore():
    sorted_set = "sorted_set"

    redis.zadd(sorted_set, {"member1": 10, "member2": 20, "member3": 30})

    members = ["member1", "member3", "non_existing_member"]
    result = redis.zmscore(sorted_set, members=members)

    assert result == [10.0, 30.0, None]

def test_zmscore_without_formatting():
    redis.format_return = False

    sorted_set = "sorted_set"

    redis.zadd(sorted_set, {"member1": 10, "member2": 20, "member3": 30})

    members = ["member1", "member3", "non_existing_member"]
    result = redis.zmscore(sorted_set, members=members)

    assert result == ["10", "30", None]

    redis.format_return = True