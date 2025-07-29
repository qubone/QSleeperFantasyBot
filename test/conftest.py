import pytest

@pytest.fixture
def player_a_dict():
    return {
        "player": {
            "id": 5856,
            "name": "Player A",
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": 10152,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }

@pytest.fixture
def player_b_dict():
    return {
        "player": {
            "id": 5856,
            "name": "Player B",
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": 12000,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }

@pytest.fixture
def player_no_value_dict():
    return {
        "player": {
            "id": 5856,
            "name": "Player B",
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": None,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }

@pytest.fixture
def player_no_name_dict():
    return {
        "player": {
            "id": 5856,
            "name": None,
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": 1,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }