from .base import StacCollectionProvider
from azure.storage.blob import ContainerClient

import functools
import logging
from typing import (
    Tuple,
    List,
    Dict)
import numpy as np

class ModisBlobStorage(StacCollectionProvider):

    _modis_container_name = 'modis'
    _modis_account_url = 'https://modissa.blob.core.windows.net/'

    # (v,h,lonmin,lonmax,latmin,latmax)
    #@functools.cached_property
    def grid_extents(self):
        return np.genfromtxt(self._modis_account_url + self._modis_container_name + '/sn_bound_10deg.txt',
                      skip_header=7,
                      skip_footer=3)

    def collection(self):
        return {"id": "modis",
                "stac_version": "1.0.0-beta.2",
                "title": "Moderate Resolution Imaging Spectroradiometer (MODIS)",
                "description": "MODIS provides Earth observation data in a wide spectral range, from 1999 to the present. The MODIS satellites image the Earth every one to two days, though individual products derived from MODIS data may have lower temporal resolutions. MODIS is administered by the National Aeronautics and Space Administration (NASA) and the US Geological Survey (USGS). We currently mirror the MCD43A4 (500m-resolution global daily surface reflectance) product on Azure dating back to 2000, and we will be on-boarding select additional MODIS products.",
                "license": "--",
                "extent": [[-180.0, -90.0, 180.0, 90.0]],
                "links": []
                }

    def item(self, itemid):
        return self.grid_extents

    def item_list(self) -> Tuple[List[Dict], str]:
        cc = ContainerClient(account_url=self._modis_account_url,
                             container_name=self._modis_container_name,
                             credential=None)
        blob_stream = cc.list_blobs().by_page()
        blob_pg = blob_stream.next()
        blob_names = [b['name'] for b in blob_pg]
        return blob_names, blob_stream.continuation_token

