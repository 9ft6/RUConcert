import asyncio
import aiohttp

from client import Client
from config import cfg
from logger import logger


class Parser:
    result: dict

    def parse(self):
        return asyncio.run(self._parse())

    async def _parse(self) -> dict:
        async with aiohttp.ClientSession() as session:
            self.client = Client(session)

            # trying load regions from last run
            await cfg.load_regions()
            if cfg.regions:
                # parsing arguments if we have regions dump
                cfg.parse_args()

            # update regions if it is necessary
            is_no_regions = not bool(cfg.regions)
            if cfg.update_regions or is_no_regions:
                cfg.regions = await self.client.get_regions()
                logger.info(f"Regions parsed successfully. Check --help for available regions")
                await cfg.dump_regions()
                exit(0)

            # parsing selected region
            tasks = [self.client.parse_region(r) for r in cfg.to_parse]
            result = await asyncio.gather(*tasks)
            # logger.debug(result)
            return dict()

    def save(self):
        ...

    def _get_config(self):
        return {}
