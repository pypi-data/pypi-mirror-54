# openapi2oms
This tool aims to convert an OpenAPI 3 spec to its corresponding OMS
equivalent. Not all features are supported, and some assumptions have
been made. Please read the caveats section to understand these
assumptions. 

## Storyscript
```coffee
result = openapi2oms convert spec: openApiSpec properties: {"serverIndex": 0}
```  

## Caveats
### Assumptions
1. If there are multiple content types available for a given path, the content type
   `application/json` shall be preferred if available. If `application/json` is not
   available, then an appropriate content type will be chosen arbitrarily
2. OMS doesn't support multiple responses. As such, the following order of response
   codes are considered as successful operations: `200, 201, 202, 2XX, 204, default`.
   Furthermore, since multiple content types are not supported, `application/json`
   will be used if available. If `application/json` is not available, then an
   appropriate content type will be chosen arbitrarily
   
   
### todos 
related:
1. [ ] https://github.com/microservices/openmicroservices.org/issues/50
2. [x] https://github.com/microservices/openmicroservices.org/pull/96

## License
MIT License
