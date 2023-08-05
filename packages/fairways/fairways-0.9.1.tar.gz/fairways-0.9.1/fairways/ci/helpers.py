import os, sys
import logging
logging.basicConfig( stream=sys.stderr )

try:
    from colorlog import ColoredFormatter
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s %(message)s%(reset)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )
except:
    formatter = None
    print("You could install colorlog")

def getLogger():        
    handler = logging.StreamHandler()
    if formatter:
        handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)
    return root

def run_asyn(coro_obj, new_loop=True):
    import asyncio
    own_loop = None
    if new_loop:
        own_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(own_loop)
        loop = own_loop
    else:
        loop = asyncio.get_event_loop()
    try:
        task = asyncio.ensure_future(coro_obj, loop=loop)
        # Note that "gather" wraps results into list:
        (result,) = loop.run_until_complete(asyncio.gather(task))
        return result
    finally:
        if own_loop:
            own_loop.close()
