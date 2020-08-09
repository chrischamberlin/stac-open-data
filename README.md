# stac-open-data

This is an experiment in exposing existing public geospatial datasets via
a STAC-compliant API. This application avoids reindexing the public datasets, 
instead retrieving items from the public dataset's index and returning
results in STAC format.

## Data support

* [MODIS](https://azure.microsoft.com/en-us/services/open-datasets/catalog/modis/), 
hosted on Azure open datasets

## Deployment

This is an Azure Functions project.
