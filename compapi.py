import logging
from dataclasses import dataclass
from enum import Enum

import FinanceDataReader as fdr
from bs4 import BeautifulSoup as BS

log = logging.getLogger()


@dataclass
class FinanacialReport:
    year: str
    roa: float
    roe: float
    per: float
    pbr: float

    def to_dict(self):
        return {
            "year": self.year,
            "roa": self.roa,
            "roe": self.roe,
            "per": self.per,
            "pbr": self.pbr,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            year=data["year"],
            roa=data["roa"],
            roe=data["roe"],
            per=data["per"],
            pbr=data["pbr"],
        )


@dataclass
class Company:
    market: str
    name: str
    stock_code: str
    reports: list[FinanacialReport]
    market_cap: int = None
    price: int = None

    def to_dict(self):
        return {
            "market": self.market,
            "name": self.name,
            "stock_code": self.stock_code,
            "market_cap": self.market_cap,
            "price": self.price,
            "reports": [fr.to_dict() for fr in self.reports],
        }

    @classmethod
    def from_dict(cls, data: dict):
        cls(
            market=data["market"],
            name=data["name"],
            stock_code=data["stock_code"],
            market_cap=data.get("market_cap"),
            price=data.get("price"),
            reports=[
                FinanacialReport.from_dict(report) for report in data.get("reports", [])
            ],
        )


class Market(Enum):
    KOSPI = "KOSPI"
    KOSDAQ = "KOSDAQ"


class CompApi:
    def get_list(self, market: Market):
        sl = fdr.StockListing(market.value)
        return [
            Company(
                market=market.value,
                name=row["Name"],
                stock_code=row["Symbol"],
                reports=[],
            )
            for _, row in sl.iterrows()
        ]


def get_corp_html_text(code: str):
    pass


def get_financial_report(code: str):
    text = get_corp_html_text(code)
    bs = BS(text, "html.parser")


def get_text_from_selector(self, bs, selector):
    log.debug("getting text from selector. sel=%s", selector)
    obj = bs.select(selector)
    return obj[0].text.strip().replace(",", "")
