from typing import List

from pydantic import BaseModel, constr

from src.domain.enums.region.enum import Region


class WatchListSymbol(BaseModel):
    symbol: constr(min_length=1)
    region: Region


class WatchListSymbols(BaseModel):
    symbols: List[WatchListSymbol]
