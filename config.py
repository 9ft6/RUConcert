import json
import sys
from argparse import ArgumentParser
from pathlib import Path

import aiofiles
from pydantic import BaseConfig

from models import Region


class Config(BaseConfig):
    regions: list[Region] = []
    to_parse: list[Region] = []
    request_attempts: int = 5

    config_filename: Path = Path("config.json")

    update_regions: bool = False
    regions_url: str = "https://www.ticketland.ru/afisha/"
    concerts_url: str = "https://{region}.ticketland.ru/concert/page-{page}/"
    url: str

    def __init__(self):
        super().__init__()

    def parse_args(self):
        parser = ArgumentParser()

        parser.add_argument("--update-regions", "-u", action="store_true", help="Update regions", default=False)
        parser.add_argument("--list", "-l", action="store_true", help="List regions", default=False)
        parser.add_argument("--all", "-a", action="store_true", help="Parse all regions", default=False)

        for region in self.regions:
            parser.add_argument(f"--{region.id}", action="store_true", help=region.name, default=False)

        args = parser.parse_args(sys.argv[1:])

        if args.list:
            [print(f"{r.id:12} : {r.name}")for r in self.regions]
            sys.exit(0)

        if args.update_regions:
            self.update_regions = True

        if args.all:
            self.to_parse = list(self.regions)
        else:
            self.to_parse = [r for r in self.regions if getattr(args, r.id, None)]

        if self.to_parse:
            self.args = args
        else:
            parser.print_help()
            exit(0)

    async def load_regions(self):
        try:
            async with aiofiles.open(self.config_filename, "r") as file:
                regions = json.loads(await file.read())
                self.regions = [Region(**r) for r in regions]
                return self.regions
        except:
            ...

    async def dump_regions(self):
        async with aiofiles.open(self.config_filename, "w") as file:
            regions = [r.model_dump() for r in self.regions]
            await file.write(json.dumps(regions, ensure_ascii=False, indent=4))


cfg = Config()
