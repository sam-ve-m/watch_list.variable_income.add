from unittest.mock import patch

from pytest import mark

from func.src.domain.request.model import WatchListSymbols
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.repositories.watch_list.repository import WatchListRepository
from func.src.services.watch_list import WatchListService

dummy_symbols_to_register = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols = WatchListSymbols(**dummy_symbols_to_register)


@mark.asyncio
@patch.object(WatchListRepository, "insert_all_symbols_in_watch_list")
async def test_register_symbols(insert_all_symbols_in_watch_list_mock):
    result = await WatchListService.register_symbols(
        dummy_watch_list_symbols, "test-id"
    )
    assert insert_all_symbols_in_watch_list_mock.call_count == 1
    for call in insert_all_symbols_in_watch_list_mock.call_args[0][0]:
        assert isinstance(call, WatchListSymbolModel)
    assert result is True
