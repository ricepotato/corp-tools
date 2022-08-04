import requests
import logging

from bs4 import BeautifulSoup as BS

log = logging.getLogger()


class Compguide:
    def __init__(self, stock_code: str):
        self.stock_code = stock_code
        self._html = None
        self._bs = None

    @property
    def html(self):
        if self._html is not None:
            return self._html

        r = requests.get(
            f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{self.stock_code}"
        )
        r.raise_for_status()
        self._html = r.text
        return self._html

    @property
    def bs(self):
        if self._bs is not None:
            return self._bs

        self._bs = BS(self._html, "html.parser")
        return self._bs

    def get_financial_reports(self):
        pass

    def get_market_cap(self) -> str:
        return self._gtfs(
            "#svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)"
        )

    def _gtfs(self, selector):
        log.debug("getting text from selector. sel=%s", selector)
        obj = self.bs.select(selector)
        return obj[0].text.strip().replace(",", "")
