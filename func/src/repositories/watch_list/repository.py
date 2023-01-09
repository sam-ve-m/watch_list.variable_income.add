from typing import List

from decouple import config
from etria_logger import Gladsheim
from nidavellir import Sindri

from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class WatchListRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_WATCH_LIST_COLLECTION")]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def insert_all_symbols_in_watch_list(
        cls, symbols: List[WatchListSymbolModel]
    ):
        client = cls.infra.get_client()
        collection = await cls.__get_collection()

        try:
            async with await client.start_session() as session:
                async with session.start_transaction():
                    for symbol in symbols:
                        symbol_filter = {"_id": symbol.get_id()}
                        watch_list_symbol_dict = symbol.to_dict()
                        Sindri.dict_to_primitive_types(watch_list_symbol_dict)

                        await collection.update_one(
                            filter=symbol_filter,
                            update={"$set": watch_list_symbol_dict},
                            upsert=True,
                            session=session,
                        )

        except Exception as ex:
            message = f"UserRepository::insert_all_symbols_in_watch_list"
            Gladsheim.error(error=ex, message=message)
            raise ex
