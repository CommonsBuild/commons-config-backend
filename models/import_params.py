import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_data(issue_number):
    MONGODB_CLIENT = os.getenv('MONGODB_CLIENT')
    client = MongoClient(MONGODB_CLIENT)
    db = client.get_database('test_tec_params_db')
    test_params_db = db.test_params
    issue_data = test_params_db.find_one({'issue_number':issue_number})
    issue_data.pop('_id', None)
    issue_data["augmentedBondingCurve"]["commonsTribute"] = 100 * issue_data["augmentedBondingCurve"]["commonsTribute"]
    issue_data["augmentedBondingCurve"]["entryTribute"] = 100 * issue_data["augmentedBondingCurve"]["entryTribute"]
    issue_data["augmentedBondingCurve"]["exitTribute"] = 100 * issue_data["augmentedBondingCurve"]["exitTribute"]

    issue_data["convictionVoting"]["minimumConviction"] = 100 * issue_data["convictionVoting"]["minimumConviction"]
    issue_data["convictionVoting"]["spendingLimit"] = 100 * issue_data["convictionVoting"]["spendingLimit"]

    issue_data["advancedSettings"]["minimumEffectiveSupply"] = 100 * issue_data["advancedSettings"]["minimumEffectiveSupply"]

    return issue_data