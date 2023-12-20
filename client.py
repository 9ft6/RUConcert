import aiohttp
import asyncio
from bs4 import BeautifulSoup

from config import cfg
from models import Concert, Region
from logger import logger


class Client:
    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_regions(self) -> list[Region]:
        response, status = await self.make_request("GET", cfg.regions_url)

        regions = []
        soup = BeautifulSoup(response, 'html.parser')
        dropdown_regions = soup.find("ul", {"class": "dropdown__list"})
        for region in dropdown_regions.find_all("li", {"class": "dropdown__item"}):
            regions.append(Region(name=region.text.strip(), **region.attrs))

        return regions

    async def parse_region(self, region) -> dict[str, Concert]:
        # TODO: implement pagination
        concerts = {}
        page = 1
        while True:
            concerts = await self._get_page(page, region)
            page += 1

            break

        return concerts

    async def _get_page(self, page: int, region: Region) -> dict[str, Concert]:
        result = {}
        url = cfg.concerts_url.format(region=region.id, page=page)
        response, status = await self.make_request("GET", url)
        print(response)

        logger.info(f"{region.id:^12} Parsing region {region.name}")
        soup = BeautifulSoup(response, 'html.parser')
        for item in soup.find_all("div", {"class": "card-search--show"}):
            item = item.find("a", {"class": "card-search__name"})
            print()
            # TODO: implement concert parsing
            concert_id = item.attrs["data-show-id"]
            result[concert_id] = Concert(
                region=region,
                name=item.text,
                date=...,
                price=...,
                url=...,
                id=concert_id,
            )
        return result


    async def make_request(self, method, url, attempts=cfg.request_attempts, **kwargs):
        while attempts:
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    if "/token" in url:
                        kwargs["headers"] = {"Content-Type": "application/json"}

                    logger.debug(f"{url}: {response.status=}")
                    if response.status >= 300:
                        logger.warning(f"{url}: got a {response.status} response code")
                        attempts -= 1
                        return await self.make_request(
                            method,
                            url,
                            attempts=attempts,
                            **kwargs,
                        )

                    try:
                        result = await response.json()
                    except Exception as e:
                        # logger.error(f"Can not decode body JSON: {e}")
                        result = await response.read()

                    # logger.debug(f"{url}: RESPONSE BODY: {result}")
                    return result, response.status
            except aiohttp.InvalidURL as error:
                logger.error(f"{url}: Invalid url: {error}")
                return None, None
            except aiohttp.ClientPayloadError as error:
                logger.error(f"{url}: Malformed payload: {error}")
                return None, None
            except (
                aiohttp.ClientConnectorError,
                aiohttp.ClientResponseError,
                aiohttp.ServerDisconnectedError,
                asyncio.TimeoutError,
            ) as error:
                attempts -= 1
                logger.warning(f"{url}: Got an error {error} during GET request")
                if not attempts:
                    break

                return await self.make_request(method, url, attempts=attempts, **kwargs)

        logger.error(f"{url}: Exceeded the number of attempts to perform {method.upper()} request")
        return None, None