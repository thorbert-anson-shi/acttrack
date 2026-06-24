from tinyflux import TinyFlux

tsdb = TinyFlux("db.csv", auto_index=True)


async def get_db():
    yield tsdb
