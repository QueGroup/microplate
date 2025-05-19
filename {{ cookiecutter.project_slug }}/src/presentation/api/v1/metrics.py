from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest


def metrics_handler(request: Request) -> Response:
    return Response(
        generate_latest(REGISTRY),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )
