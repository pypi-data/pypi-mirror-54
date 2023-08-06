# geoapi-client
Geospatial API for TAPIS


- API version: 0.1
- Package version: 0.2.1
- Build package: io.swagger.codegen.languages.PythonClientCodegen

For more information about the [GeoAPI](https://github.com/TACC-Cloud/geoap) and how this client is generated using [Swagger Codegen](https://github.com/swagger-api/swagger-codegen), visit https://github.com/TACC-Cloud/geoap .

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

The python package can be found at [PyPi](https://pypi.org/project/geoapi-client/)

```sh
pip install geoapi-client --user
```

Then import the package:
```python
import geoapi_client 
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import geoapi_client
from geoapi_client.rest import ApiException
from pprint import pprint

configuration = geoapi_client.Configuration()
configuration.host = MY_HOST # e.g. https://agave.designsafe-ci.org/geo/v2
configuration.api_key_prefix['Authorization'] = 'Bearer'
configuration.api_key['Authorization'] = TOKEN

api_client = geoapi_client.ApiClient(configuration)
api_instance = geoapi_client.ProjectsApi(api_client=api_client)

try:
    project = api_instance.create_project(payload={"name": "My project"})
    pprint(project)
    api_response = api_instance.upload_file(project.id, 'image.jpg')
    pprint(api_response)
except ApiException as e:
    print("Exception: %s\n" % e)
```

## API Endpoints

All URIs are relative to *https://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ProjectsApi* | **add_feature_asset** | **POST** /projects/{projectId}/features/{featureId}/assets/ | 
*ProjectsApi* | **add_geo_json_feature** | **POST** /projects/{projectId}/features/ | 
*ProjectsApi* | **add_overlay** | **POST** /projects/{projectId}/overlays/ | 
*ProjectsApi* | **add_point_cloud** | **POST** /projects/{projectId}/point-cloud/ | 
*ProjectsApi* | **add_user** | **POST** /projects/{projectId}/users/ | 
*ProjectsApi* | **cluster_features** | **GET** /projects/{projectId}/features/cluster/{numClusters}/ | 
*ProjectsApi* | **create_project** | **POST** /projects/ | 
*ProjectsApi* | **create_rapid_project** | **POST** /projects/rapid/ | 
*ProjectsApi* | **delete_point_cloud** | **DELETE** /projects/{projectId}/point-cloud/{pointCloudId}/ | 
*ProjectsApi* | **delete_project** | **DELETE** /projects/{projectId}/ | 
*ProjectsApi* | **get_all_features** | **GET** /projects/{projectId}/features/ | 
*ProjectsApi* | **get_all_point_clouds** | **GET** /projects/{projectId}/point-cloud/ | 
*ProjectsApi* | **get_feature** | **GET** /projects/{projectId}/features/{featureId}/ | 
*ProjectsApi* | **get_overlays** | **GET** /projects/{projectId}/overlays/ | 
*ProjectsApi* | **get_point_cloud** | **GET** /projects/{projectId}/point-cloud/{pointCloudId}/ | 
*ProjectsApi* | **get_project_by_id** | **GET** /projects/{projectId}/ | 
*ProjectsApi* | **get_project_users_resource** | **GET** /projects/{projectId}/users/ | 
*ProjectsApi* | **get_projects** | **GET** /projects/ | 
*ProjectsApi* | **get_tasks** | **GET** /projects/{projectId}/tasks/ | 
*ProjectsApi* | **import_file_from_tapis** | **POST** /projects/{projectId}/features/files/import/ | 
*ProjectsApi* | **remove_overlay** | **DELETE** /projects/{projectId}/overlays/{overlayId}/ | 
*ProjectsApi* | **remove_user** | **DELETE** /projects/{projectId}/users/{username}/ | 
*ProjectsApi* | **update_feature_properties** | **POST** /projects/{projectId}/features/{featureId}/properties/ | 
*ProjectsApi* | **update_feature_styles** | **POST** /projects/{projectId}/features/{featureId}/styles/ | 
*ProjectsApi* | **update_point_c_loud** | **PUT** /projects/{projectId}/point-cloud/{pointCloudId}/ | 
*ProjectsApi* | **update_project** | **PUT** /projects/{projectId}/ | 
*ProjectsApi* | **upload_file** | **POST** /projects/{projectId}/features/files/ | 
*ProjectsApi* | **upload_point_cloud** | **POST** /projects/{projectId}/point-cloud/{pointCloudId}/ | 


## Models

 - Asset
 - Feature
 - FeatureCollection
 - OkResponse
 - Overlay
 - PointCloud
 - Project
 - RapidProject
 - TapisFile
 - TapisFileImport
 - Task
 - User


## Documentation For Authorization


## JWT

- **Type**: API key
- **API key parameter name**: X-JWT-Assertion-designsafe
- **Location**: HTTP header

## Token

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header


## Author

Texas Advanced Computing Center
CICsupport@tacc.utexas.edu
