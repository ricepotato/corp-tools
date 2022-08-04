from compguide import Compguide


def test_cg_get_market_cap():
    code = "005930"
    cg = Compguide(code)
    market_cap = cg.get_market_cap()
    assert market_cap
