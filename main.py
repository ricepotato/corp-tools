import json
import logging

from concurrent.futures import ThreadPoolExecutor

from compapi import CompApi, Market
from compguide import Compguide


log = logging.getLogger()
stream_handler = logging.StreamHandler()
format = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
stream_handler.setFormatter(logging.Formatter(format))
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)


def main():
    api = CompApi()
    log.info("get kospi list")
    kospi = api.get_list(Market.KOSPI)

    with ThreadPoolExecutor(max_workers=10) as exec:
        # for corp in kospi[:10]:
        futures = [exec.submit(cwfr, corp) for corp in kospi]
        result = [f.result() for f in futures]
        dict_list = [corp.to_dict() for corp in result]

    with open("kospi.json", "w") as f:
        f.write(json.dumps(dict_list, indent=4))


def cwfr(corp):
    cg = Compguide(corp.stock_code)
    corp.market_cap = cg.get_market_cap()
    corp.reports = cg.get_financial_reports()
    return corp


if __name__ == "__main__":
    main()
