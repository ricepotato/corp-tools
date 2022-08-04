from dataclasses import dataclass


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
    code: str
    name: str
    stock_code: str
    modify_date: str
    reports: list[FinanacialReport]
    market_cap: int = None
    price: int = None

    def to_dict(self):
        return {
            "market": self.market,
            "code": self.code,
            "name": self.name,
            "stock_code": self.stock_code,
            "modify_date": self.modify_date,
            "market_cap": self.market_cap,
            "price": self.price,
            "reports": [fr.to_dict() for fr in self.reports],
        }

    @classmethod
    def from_dict(cls, data: dict):
        cls(
            market=data["market"],
            code=data["code"],
            name=data["name"],
            stock_code=data["stock_code"],
            modify_date=data["modify_date"],
            market_cap=data.get("market_cap"),
            price=data.get("price"),
            reports=[
                FinanacialReport.from_dict(report) for report in data.get("reports", [])
            ],
        )
