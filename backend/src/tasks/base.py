import asyncio
import threading


_local = threading.local()

def get_worker_loop():
    if not hasattr(_local, "loop") or _local.loop.is_closed():
        _local.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_local.loop)
    return _local.loop

def run_async(coro):
    loop = get_worker_loop()
    return loop.run_until_complete(coro)
