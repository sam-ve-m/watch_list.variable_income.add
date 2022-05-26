from func.src.domain.validator import WatchListSymbol


class WatchListSymbolModel:

    def __init__(self, watch_list_symbol: WatchListSymbol, unique_id: str):
        self.unique_id = unique_id
        self.symbol = watch_list_symbol.symbol
        self.region = watch_list_symbol.region
        self._id = f"{self.symbol}_{self.region.value}"

    def to_dict(self) -> dict:
        dict_representation = {
            "unique_id": self.unique_id,
            "symbol": self.symbol,
            "region": self.region,
            "_id": self._id,
        }
        return dict_representation
