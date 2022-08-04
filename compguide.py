from dataclasses import dataclass
import requests
import logging

from bs4 import BeautifulSoup as BS

from models import FinanacialReport

log = logging.getLogger()


@dataclass
class Selectors:
    year: str
    roa: str
    roe: str
    per: str
    pbr: str


class Compguide:
    def __init__(self, stock_code: str):
        self.stock_code = stock_code
        self._html = None
        self._bs = None

    def get_market_cap(self) -> str:
        log.debug("get market cap. stock_code=%s", self.stock_code)
        return self._gtfs(
            "#svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)"
        )

    def get_financial_reports(self):
        years = [2017, 2018, 2019, 2020, 2021]
        selectors = [
            Selectors(
                year=str(year),
                roa=f"#highlight_D_Y > table > tbody > tr:nth-child(17) > td:nth-child({year - 2015})",
                roe=f"#highlight_D_Y > table > tbody > tr:nth-child(18) > td:nth-child({year - 2015})",
                per=f"#highlight_D_Y > table > tbody > tr:nth-child(22) > td:nth-child({year - 2015})",
                pbr=f"#highlight_D_Y > table > tbody > tr:nth-child(23) > td:nth-child({year - 2015})",
            )
            for year in years
        ]

        return [
            FinanacialReport(
                year=sel.year,
                roa=self._gtfs(sel.roa),
                roe=self._gtfs(sel.roe),
                per=self._gtfs(sel.per),
                pbr=self._gtfs(sel.pbr),
            )
            for sel in selectors
        ]

    def _gtfs(self, selector):
        log.debug("getting text from selector. sel=%s", selector)
        obj = self.bs.select(selector)
        try:
            return obj[0].text.strip().replace(",", "")
        except IndexError as e:
            log.error("gtfs error. %s stock_code=%s", e, self.stock_code)
            return ""

    @property
    def html(self):
        if self._html is not None:
            return self._html

        log.debug("get html stock_code=%s", self.stock_code)
        try:
            r = requests.get(
                f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{self.stock_code}"
            )
            r.raise_for_status()
            self._html = r.text
            return self._html
        except Exception as e:
            log.error("getting html error. %s", e)
            return ""

    @property
    def bs(self):
        if self._bs is not None:
            return self._bs

        self._bs = BS(self.html, "html.parser")
        return self._bs
