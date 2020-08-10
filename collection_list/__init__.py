import json
import logging

import azure.functions as func

from ..open_data import COLLECTIONS

def main(req: func.HttpRequest) -> func.HttpResponse:
    collections = [c.collection() for c in COLLECTIONS.values()]

    return func.HttpResponse(json.dumps(collections), status_code=200,
                             mimetype="application/json")
