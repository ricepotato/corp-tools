from compapi import CompApi, Market


def test_compapi():
    api = CompApi()
    kosdaq = api.get_list(Market.KOSDAQ)
    assert kosdaq
