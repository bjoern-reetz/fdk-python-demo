import io
import json

import pytest
from fdk.fixtures import setup_fn_call

from src.fdk_python_demo import handler


def setup_fn_gateway_call(
    handle_func,
    request_url: str,
    method="GET",
    headers=None,
    content: io.BytesIO = None,
    deadline=None,
):
    return setup_fn_call(
        handle_func=handle_func,
        request_url=request_url,
        method=method,
        headers=headers,
        content=content,
        deadline=deadline,
        gateway=True,
    )


@pytest.mark.asyncio
async def test_hello_route():
    call = await setup_fn_gateway_call(handler, request_url="/hello")

    content, status, headers = await call

    assert 200 == status
    assert {"message": "Hello World"} == json.loads(content)


@pytest.mark.asyncio
async def test_gimme_json_route():
    json_data = {"some": "json"}
    content = io.BytesIO(json.dumps(json_data).encode())
    call = await setup_fn_gateway_call(
        handler, request_url="/gimme-json", method="POST", content=content
    )

    content, status, headers = await call

    assert 200 == status
    assert {"received_json_data": json_data} == json.loads(content)


@pytest.mark.asyncio
async def test_404s():
    call = await setup_fn_gateway_call(
        handler, request_url="/does-not-exist", method="GET"
    )
    content, status, headers = await call
    assert 404 == status

    call = await setup_fn_gateway_call(handler, request_url="/hello", method="POST")
    content, status, headers = await call
    assert 405 == status
