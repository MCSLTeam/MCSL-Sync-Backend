async def get_proxy() -> dict | None:
    from urllib.request import getproxies
    try:
        proxy = getproxies()["http"]
    except KeyError:
        proxy = None
    proxies = {"http": proxy, "https": proxy}
    del proxy
    del getproxies
    return proxies
