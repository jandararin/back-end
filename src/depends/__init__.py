from fastapi import Header, Request


def sample_depends(content_type=Header(...), request: Request = None):
    print(content_type, request)
