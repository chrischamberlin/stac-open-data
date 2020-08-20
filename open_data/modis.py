from .base import StacCollectionProvider
from azure.storage.blob import ContainerClient

import functools
import logging
import re
from datetime import datetime
from typing import (
    Tuple,
    List,
    Dict,
    Optional)
import numpy as np

class ModisBlobStorage(StacCollectionProvider):

    _modis_container_name = 'modis'
    _modis_account_url = 'https://modissa.blob.core.windows.net/'

    # (v,h,lonmin,lonmax,latmin,latmax)
    @property
    @functools.lru_cache()
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

    def item_list(self, page_token=None) -> Tuple[List[Dict], str]:
        cc = ContainerClient(account_url=self._modis_account_url,
                             container_name=self._modis_container_name,
                             credential=None)
        logging.info("retrieve list from page for %s" % cc)
        blob_stream = cc.list_blobs().by_page()
        blob_pg = blob_stream.next()

        # for all blobs found, collect by id
        # TODO manage partial datasets at page boundaries
        items = {}
        for b in blob_pg:
            path = b['name']
            itemid = self.id_for_path(path)
            asset = self.asset_for_path(path)
            if itemid is not None and asset is not None:
                item = items.get(itemid)
                if item is None:
                    item = self.item_for_path(path)
                item['assets'][asset[0]] = asset[1]
                items[itemid] = item
        logging.info("retrieved %s items modis" % (len(items)))
        return list(items.values()), blob_stream.continuation_token

    _path_id_re = re.compile('^.+/../../(\\d{7})/(BROWSE\\.)?(.+\\.A\\d{7}\\.h\\d\\dv\\d\\d\\.\\d{3})\\.\\d+\\.(.+)$')

    def _path_group(self, path, num) -> Optional[str]:
        m = re.search(self._path_id_re, path)
        if m:
            return m.group(num)
        else:
            return None

    def id_for_path(self, path) -> Optional[str]:
        return self._path_group(path, 3)

    def datetime_for_path(self, path) -> Optional[datetime]:
        d = self._path_group(path, 1)
        # daynum is a four-digit year plus a three-digit day of year (from 001 to 365)
        if d:
            try:
                return datetime.strptime(d, "%Y%j")
            except ValueError as e:
                pass
        logging.debug("Unable to parse datetime from path: %s" % path)
        return None

    def item_for_path(self, path) -> Dict:
        return {
            "id": self.id_for_path(path),
            "stac_version": "1.0.0.beta2",
            "type": "Feature",
            "geometry": None,  # TODO get from grid_extends
            "bbox": None, # TODO compute from grid_extents
            "properties": {
                "datetime": self.datetime_for_path(path).isoformat()
            },
            "assets": {},
            "links": []
        }

    def uri_for_path(self, path) -> str:
        return self._modis_account_url + self._modis_container_name + '/' + path

    def asset_for_path(self, path) -> Optional[Tuple]:
        is_browse = self._path_group(path, 2)
        name_suffix = self._path_group(path, 4)
        a = None
        roles = []
        if is_browse:
            a = "thumbnail"
            roles = ["thumbnail"]
        elif name_suffix and name_suffix.endswith(".xml"):
            a = name_suffix
            roles = ["metadata"]
        elif name_suffix and name_suffix.endswith(".tiff"):
            a = name_suffix
            roles = ["data"]

        if a:
            # TODO complete asset record
            return a, {"href": self.uri_for_path(path),
                       "roles": roles}
        else:
            return None

