import httpx


class Judge0Service:
    def __init__(self, url: str, header: str, token: str):
        if url[-1] == "/":
            url = url[:-1]
        self._url = url
        self._client = httpx.AsyncClient(headers={header: token})

    async def get_system_information(self) -> dict:
        resp = await self._client.get(f"{self._url}/system_info")
        return resp.json()

    async def get_available_languages(self) -> list[dict]:
        resp = await self._client.get(f"{self._url}/languages")
        return resp.json()
