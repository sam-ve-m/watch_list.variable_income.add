from unittest.mock import patch

from pytest import mark

from src.domain.request.model import WatchListSymbols
from src.repositories.watch_list.repository import WatchListRepository
from src.services.watch_list import WatchListService

dummy_symbols_to_register = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols = WatchListSymbols(**dummy_symbols_to_register)


@mark.asyncio
@mark.parametrize("exists_in_watch_list_value", [False, True])
@patch.object(WatchListRepository, "insert_one_symbol_in_watch_list")
@patch.object(WatchListRepository, "exists_in_watch_list")
async def test_register_symbols(
    exists_mock, insert_one_symbol_in_watch_list_mock, exists_in_watch_list_value
):
    exists_mock.return_value = exists_in_watch_list_value
    result = await WatchListService.register_symbols(
        dummy_watch_list_symbols, "test-id"
    )

    if not exists_in_watch_list_value:
        assert insert_one_symbol_in_watch_list_mock.call_count == len(
            dummy_symbols_to_register["symbols"]
        )
    else:
        insert_one_symbol_in_watch_list_mock.assert_not_called()
