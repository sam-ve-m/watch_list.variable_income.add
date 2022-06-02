# Jormungandr
from src.repositories.watch_list.repository import WatchListRepository
from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
import asyncio


class WatchListService:

    watch_list_repository = WatchListRepository

    @classmethod
    async def register_symbols(
        cls, watch_list_symbols: WatchListSymbols, unique_id: str
    ):
        futures = list()
        for watch_list_symbol in watch_list_symbols.symbols:
            watch_list_symbol_model = WatchListSymbolModel(watch_list_symbol, unique_id)
            symbol_already_exists_on_watch_list = (
                await cls.watch_list_repository.exists_in_watch_list(
                    watch_list_symbol_model
                )
            )
            if not symbol_already_exists_on_watch_list:
                futures.append(
                    cls.watch_list_repository.insert_one_symbol_in_watch_list(
                        watch_list_symbol_model
                    )
                )
        await asyncio.gather(*futures)

        return True
