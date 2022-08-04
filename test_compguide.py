from compguide import Compguide


def test_cg_get_market_cap():
    code = "005930"
    cg = Compguide(code)
    market_cap = cg.get_market_cap()
    assert market_cap


def test_cg_get_fr1():
    code = "005930"  # 삼성전자
    cg = Compguide(code)
    fr_list = cg.get_financial_reports()
    assert fr_list

    fr_2017 = next(filter(lambda fr: fr.year == "2017", fr_list))
    assert fr_2017.roa == 14.96
    assert fr_2017.pbr == 1.76

    fr_2019 = next(filter(lambda fr: fr.year == "2019", fr_list))
    assert fr_2019.roe == 8.69
    assert fr_2019.per == 17.63

    fr_2021 = next(filter(lambda fr: fr.year == "2021", fr_list))
    assert fr_2021.roa == 9.92
    assert fr_2021.pbr == 1.80


def test_cg_get_fr2():
    code = "293490"  # 카카오 게임즈
    cg = Compguide(code)
    fr_list = cg.get_financial_reports()
    assert fr_list

    fr_2017 = next(filter(lambda fr: fr.year == "2017", fr_list))
    assert fr_2017.per == 0
    assert fr_2017.pbr == 0
    assert fr_2017.roa == 26.32

    fr_2020 = next(filter(lambda fr: fr.year == "2020", fr_list))
    assert fr_2020.roa == 7.10
    assert fr_2020.per == 33.33
