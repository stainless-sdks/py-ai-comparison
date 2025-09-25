import asyncio

import httpx
import respx
from mistralai import Mistral


async def main():
    api_key = "<example api key>"

    with respx.mock:
        respx.mock.get("/v1/batch/jobs/test-job-id").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "UNKNOWN_STATUS",  # Unknown enum value
                    "unexpected_property": True,  # Field not in the OpenAPI spec
                    # mismatched type
                    "id": {"value": "..."},
                    # base response
                    "object": "batch",
                    "completed_requests": 1,
                    "input_files": ["file-1"],
                    "metadata": {},
                    "endpoint": "",
                    "errors": [],
                    "created_at": 1000000,
                    "started_at": 1000001,
                    "completed_at": 1000002,
                    "succeeded_requests": 10,
                    "failed_requests": 0,
                    "total_requests": 10,
                    "model": "mistral-test",
                    "output_file": "output-file-1",
                    "error_file": None,
                },
            )
        )

        client = Mistral(api_key=api_key)

        # crashes
        await client.batch.jobs.get_async(
            job_id="test-job-id",
            http_headers={"x-my-header": "value"},
            # note mistral sdk does not support custom query / body params
        )


if __name__ == "__main__":
    asyncio.run(main())
