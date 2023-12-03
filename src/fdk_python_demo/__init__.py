import io
import json

from fdk import context
from fdk.context import InvokeContext
from fdk.response import Response


def handler(ctx: InvokeContext, data: io.BytesIO = None):
    url = ctx.RequestURL()
    method = ctx.Method()

    if url == "/hello":
        if method == "GET":
            return hello_world_route(ctx)
        return method_not_allowed_route(ctx)
    elif url == "/gimme-json":
        if method == "POST":
            return route_that_uses_body(ctx, data)
        return method_not_allowed_route(ctx)

    return not_found_route(ctx)


def hello_world_route(ctx: InvokeContext) -> Response:
    return JsonResponse(ctx, response_obj={"message": "Hello World"})


def route_that_uses_body(ctx: InvokeContext, data: io.BytesIO):
    json_data = json.load(data)

    return JsonResponse(
        ctx,
        response_obj={
            "received_json_data": json_data,
        },
    )


def not_found_route(ctx: InvokeContext) -> Response:
    return JsonResponse(ctx, response_obj={"message": "Not found."}, status_code=404)


def method_not_allowed_route(ctx: InvokeContext) -> Response:
    return JsonResponse(
        ctx, response_obj={"message": "Method not allowed."}, status_code=405
    )


class JsonResponse(Response):
    def __init__(
        self,
        ctx: context.InvokeContext,
        response_obj,
        headers: dict = None,
        status_code: int = 200,
        response_encoding: str = "utf-8",
    ):
        if headers is None:
            headers = {"content-type": "application/json"}
        elif "content-type" not in [key.lower() for key in headers]:
            headers["content-type"] = "application/json"
        super().__init__(
            ctx, json.dumps(response_obj), headers, status_code, response_encoding
        )
