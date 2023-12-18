import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup

from config import Config, cfg
from models import Concert, Region
from logger import logger


class Client:
    config: Config
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

    async def parse_region(self, region) -> Concert:
        return Concert(region=region)

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
                        logger.error(f"Can not decode body JSON: {e}")
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