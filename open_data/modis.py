from .base import StacCollectionProvider


class ModisBlobStorage(StacCollectionProvider):
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
        pass


