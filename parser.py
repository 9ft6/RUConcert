import asyncio
import json

import aiohttp
from datetime import datetime
from pathlib import Path

from client import Client
from config import cfg
from logger import logger


class Parser:
    result: dict = {}
    default_path: Path = Path("results")

    def parse(self):
        return asyncio.run(self._parse())

    async def _parse(self):
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
                logger.info(f"Regions parsed successfully. "
                            f"Check --help for available regions")
                await cfg.dump_regions()
                exit(0)

            # parsing selected region
            tasks = [self.client.parse_region(r) for r in cfg.to_parse]
            [self.result.update(r) for r in await asyncio.gather(*tasks)]
            self.save(self.result)

    def save(self, result):
        if not self.default_path.exists():
            self.default_path.mkdir(exist_ok=True, parents=True)
        filename = self.default_path / f"result_{datetime.utcnow()}.json"

        result = {r: {i: c for i, c in cs.items()} for r, cs in result.items()}
        with open(filename, "w") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    def _get_config(self):
        return {}
