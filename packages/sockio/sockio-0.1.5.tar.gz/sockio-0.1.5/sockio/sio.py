import asyncio
import functools
import threading

from . import aio


class BaseProxy:

    def __init__(self, ref):
        self._ref = ref


class EventLoop(threading.Thread):

    def __init__(self, name='AIOTH', loop=None):
        self.loop = loop or asyncio.new_event_loop()
        self.proxies = {}
        super().__init__(name=name)
        self.daemon = True

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    def call_soon(self, func, *args, **kwargs):
        f = functools.partial(func, *args, **kwargs)
        return self.loop.call_soon_threadsafe(f)

    def run_coroutine(self, coro):
         return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def _create_coroutine_threadsafe(self, corof, resolve_future):
        @functools.wraps(corof)
        def wrapper(obj, *args, **kwargs):
            coro = corof(obj._ref, *args, **kwargs)
            future = self.run_coroutine(coro)
            return future.result() if resolve_future else future
        return wrapper

    def _create_proxy_for(self, klass, resolve_futures=True):
        class Proxy(BaseProxy):
            pass
        for name in dir(klass):
            if name.startswith('_'):
                continue
            member = getattr(klass, name)
            if asyncio.iscoroutinefunction(member):
                member = self._create_coroutine_threadsafe(
                    member, resolve_futures)
            setattr(Proxy, name, member)
        return Proxy

    def proxy(self, obj, resolve_futures=True):
        if not self.is_alive():
            self.start()
        klass = type(obj)
        key = klass, resolve_futures
        Proxy = self.proxies.get(key)
        if not Proxy:
            Proxy = self._create_proxy_for(klass, resolve_futures)
            self.proxies[key] = Proxy
        return Proxy(obj)

    def socket(self, host, port, eol=b'\n', auto_reconnect=True,
               resolve_futures=True):
        sock = aio.Socket(host, port, eol=eol, auto_reconnect=auto_reconnect)
        return self.proxy(sock, resolve_futures)


DefaultEventLoop = EventLoop()
Socket = DefaultEventLoop.socket


