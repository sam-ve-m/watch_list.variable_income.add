from unittest.mock import patch, AsyncMock

import pytest
from etria_logger import Gladsheim
from nidavellir import Sindri
from pytest import mark

from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
from src.repositories.watch_list.repository import WatchListRepository

dummy_symbols_to_insert = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols_model = [
    WatchListSymbolModel(symbol, "test_id")
    for symbol in WatchListSymbols(**dummy_symbols_to_insert).symbols
]
dummy_insert = [
    str(Sindri.dict_to_primitive_types(x.to_dict()))
    for x in dummy_watch_list_symbols_model
]


@mark.asyncio
@mark.parametrize("symbols_to_insert", dummy_watch_list_symbols_model)
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_one_symbol_in_watch_list(get_collection_mock, symbols_to_insert):
    await WatchListRepository.insert_one_symbol_in_watch_list(symbols_to_insert)
    get_collection_mock.assert_called_once_with()
    for insertion in range(0, len(dummy_insert)):
        for calls in get_collection_mock.mock_calls:
            if calls[0] == "().insert_one":
                assert str(calls[1][0]) in dummy_insert


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_one_symbol_in_watch_list_exception(
    get_collection_mock, etria_mock
):
    get_collection_mock.insert_one.side_effect = Exception("Erro")
    with pytest.raises(Exception):
        await WatchListRepository.insert_one_symbol_in_watch_list(
            dummy_watch_list_symbols_model[0]
        )
        get_collection_mock.assert_called_once_with()
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("symbol_finded", [{"symbol": "test"}, {}])
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_exists_in_watch_list(get_collection_mock, symbol_finded):
    collection_mock = AsyncMock()
    collection_mock.find_one.return_value = symbol_finded
    get_collection_mock.return_value = collection_mock
    result = await WatchListRepository.exists_in_watch_list(
        dummy_watch_list_symbols_model[0]
    )
    get_collection_mock.assert_called_once_with()
    assert result == bool(symbol_finded)


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_exists_in_watch_list_exception(get_collection_mock, etria_mock):
    get_collection_mock.find_one.side_effect = Exception("Erro")
    with pytest.raises(Exception):
        await WatchListRepository.exists_in_watch_list(
            dummy_watch_list_symbols_model[0]
        )
        get_collection_mock.assert_called_once_with()
        etria_mock.assert_called()
