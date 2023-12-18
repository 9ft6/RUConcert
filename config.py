import json
from argparse import ArgumentParser
from pathlib import Path

import aiofiles
from pydantic import BaseConfig, validator

from models import Region


class Config(BaseConfig):
    parser: ArgumentParser
    regions: list[Region] = []
    request_attempts: int = 5

    config_filename: Path = Path("config.json")

    update_regions: bool = False
    regions_url: str = "https://www.ticketland.ru/afisha/"
    url: str

    def __init__(self):
        super().__init__()

        self.parser = ArgumentParser()
        # TODO: --update_regions, -u self.update_regions
        # TODO: --list, -l list regions
        # TODO: generation --help

    async def load_regions(self):
        try:
           async with aiofiles.open(self.config_filename, "r") as file:
                regions = json.loads(await file.read())
                self.regions = [Region(**r) for r in regions]
        except:
            ...

    async def dump_regions(self):
        async with aiofiles.open(self.config_filename, "w") as file:
            regions = [r.model_dump() for r in self.regions]
            await file.write(json.dumps(regions, ensure_ascii=False, indent=4))


cfg = Config()
