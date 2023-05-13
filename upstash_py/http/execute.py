from upstash_py.exception import UpstashException
from upstash_py.http.decode import decode
from upstash_py.schema.http import RESTResult, RESTResponse, RESTEncoding
from asyncio import sleep
from aiohttp import ClientSession
from json import dumps
from platform import python_version


async def execute(
    session: ClientSession,
    url: str,
    token: str,
    encoding: RESTEncoding,
    retries: int,
    retry_interval: int,
    command: list,
    allow_telemetry: bool
) -> RESTResult:
    """
    Execute the given command over the REST API.
    """

    # Serialize the command; more specifically, write string-incompatible types as JSON strings.
    command = [
        element if isinstance(element, str | int | float)

        else dumps(element)

        for element in command
    ]

    for i in range(retries + 1):
        try:
            headers: dict[str, str] = {"Authorization": f'Bearer {token}'}

            if allow_telemetry:
                headers["Upstash-Telemetry-Runtime"] = f'python@v.{python_version()}'
                headers["Upstash-Telemetry-Sdk"] = "upstash_py@development"

            if encoding:
                headers["Upstash-Encoding"] = encoding

            async with session.post(url, headers=headers, json=command) as response:
                body: RESTResponse[RESTResult] = await response.json()

                # Avoid the [] syntax to prevent KeyError from being raised.
                if body.get("error"):
                    raise UpstashException(body.get("error"))

                return decode(raw=body["result"], encoding=encoding) if encoding else body["result"]
            break
        except Exception as exception:
            if i == retries:
                # If we exhausted all the retries, raise the exception.
                raise exception
            else:
                await sleep(retry_interval)
