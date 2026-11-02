# Source catalog (fill during Phase 1)

| source_id | provider | dataset | version | license | retrieval_date | spatial_res | temporal_cov | access_method | caveats | status |
|---|---|---|---|---|---|---|---|---|---|---|
| s2 | Copernicus DSE | Sentinel-2 L2A | | | | 10-20 m | 2017/2018-now | openEO / Statistical API | cloud; check L2A availability per year | todo |
| chirps | CHC UCSB | CHIRPS v3 | | | | ~0.05 deg | 1981-now | HTTP download | not a forecast | todo |
| era5l | ECMWF/C3S | ERA5-Land | | | | ~9 km | 1950-now | cdsapi | reanalysis, not a forecast | todo |
| soilgrids | ISRIC | SoilGrids | | | | 250 m | static | REST/WCS | not live moisture | todo |
| bounds | TBD | Admin boundaries | | | | vector | static | TBD | pick one, record license | todo |
| landcover | ESA | WorldCover (cropland mask) | | | | 10 m | 2020/2021 | download | NOT in original blueprint; masks forest/pasture | todo |
| ingc | INGC | Large-crop statistics | | | | governorate? | ? years | web | check definitions | todo |
| oc | Office des Céréales | Collection stats | | | | governorate | ? years | web | collection != production | todo |
| giews | FAO | GIEWS calendars/reports | | | | country | | web | context only | todo |
