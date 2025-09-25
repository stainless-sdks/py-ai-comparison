import asyncio

import httpx
import respx
from anthropic import AsyncAnthropic


async def main():
    api_key = "<example api key>"

    with respx.mock:
        respx.mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "role": "new-role",  # Unknown enum value
                    "unexpected_property": True,  # Field not in the OpenAPI spec
                    # mismatched type
                    "id": {"value": "..."},
                    # base response
                    "model": "...",
                    "content": [],
                },
            )
        )

        client = AsyncAnthropic(api_key=api_key)

        message = await client.messages.create(
            extra_body={"custom_request_param": "value"},
            extra_headers={"x-my-header": "value"},
            # base request
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello!",
                }
            ],
            model="claude-sonnet-4-20250514",
        )

        print(message)
        print(message.role)  # 'new-role'


if __name__ == "__main__":
    asyncio.run(main())
