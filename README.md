# stac-open-data

This is an experiment in exposing existing public geospatial datasets via
a [STAC](https://stacspec.org/)-compliant API. The application avoids reindexing the public datasets, 
instead retrieving asset lists from the public dataset's storage directly, and
reformatted the result into STAC item format. This choice will limit the available 
search capabilities to those that can be executed by listing items,
but may be helpful for browsing existing collections using standard tooling.

## Demo

The application is hosted in Azure Functions and is currently configured
to browse the [MODIS](https://azure.microsoft.com/en-us/services/open-datasets/catalog/modis/)
archive hosted on Azure Open Datasets.

Some example URLs:

 * [List collections](https://stac-open-data.azurewebsites.net/api/collections)
 * [Get MODIS collection](https://stac-open-data.azurewebsites.net/api/collections/modis)
 * [List MODIS items](https://stac-open-data.azurewebsites.net/api/collections/modis/items)
