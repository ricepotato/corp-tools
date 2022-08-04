from dartapi import DartAPI
import json


def test_dartapi_dump():
    api = DartAPI()
    cc_list = api.get_corp_code()

    filterd_list = filter(lambda corp: corp.stock_code, cc_list)
    corp_dict_list = [comp.to_dict() for comp in filterd_list]

    with open("corps.json", "w") as f:
        f.write(json.dumps(corp_dict_list, indent=4))
