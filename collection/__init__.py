import json
import logging

import azure.functions as func

from ..open_data import COLLECTIONS

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    collectionid = req.route_params['collection']
    collection = COLLECTIONS.get(collectionid)
    if collection is None:
        return func.HttpResponse("collection %s does not exist" % collectionid, status_code=404)

    return func.HttpResponse(json.dumps(collection.collection()), status_code=200)
