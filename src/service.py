import logging

import backoff
from httpx import AsyncClient, codes, HTTPError, ConnectError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MessageService:
    async def send_message(self, msg, url):
        status_code = await self.client_post(msg, url)

        if status_code == codes.OK:
            logger.info(f'message is replicated on secondary server {url}')
            return msg
        else:
            raise

    @staticmethod
    @backoff.on_exception(backoff.expo, ConnectError, max_time=3)
    async def client_post(msg, url):
        try:
            async with AsyncClient() as client:
                resp = await client.post(url=url,
                                         json=dict(msg),
                                         headers={"Content-Type": "application/json"}
                                         )
                resp.raise_for_status()
            return resp.status_code
        except HTTPError:
            raise
