import FinanceDataReader as fdr


def test_stock_listing():
    kospi = fdr.StockListing("KOSPI")
    for index, row in kospi.iterrows():
        print(row)
