import asyncio
from src.completion_handler import papermc_runner, arclight_powered_runner


asyncio.run(papermc_runner())
asyncio.run(arclight_powered_runner())
