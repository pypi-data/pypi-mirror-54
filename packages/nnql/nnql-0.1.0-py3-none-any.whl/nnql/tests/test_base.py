import asyncio
import threading

from nnql.tests.just_add import just_add


def test_just_add():
    just_add()


async def after(tid):
    assert tid == threading.get_ident()


async def main(tid):
    assert tid == threading.get_ident()
    await after(tid)
    assert tid == threading.get_ident()


def test_async_in_same_thread():
    tid = threading.get_ident()
    asyncio.run(main(tid))
