# TODOs

## current task

* QTL Gene: num_qtls_targeting_gene
* gene links need correct sharded track
* QTLBedResult <-> some sort of an internal, allowable parameter not in the documentation for formatting QTL data in a visualization? 

### GenericFeatureParameter

* have a function that returns the right kind? --> see ResponseContent

```python
class FeatureParameter():
    def __init__(self, feature: Feature = None):
        # if features is None, set to all allowable features
        self.__feature: Feature = feature

    @classmethod
    def set_description(cls, featureType):
        match featureType:
            case None:
                return """genomic region to query, may be one of the following:
                Official Gene Symbol, Ensembl ID, Entrez ID, refSNP ID, variant positional ID (chr:pos:ref:alt),
                or genomic span. Please specific genomic spans as chrN:start-end or N:start-end"""
                
            case Feature.GENE:
                return """gene to query, may be one of the following:
                Official Gene Symbol, Ensembl ID, Entrez ID"""
                
            case Feature.VARIANT:
                return """variant to query, may be one of the following: 
                refSNP ID, variant positional ID (chr:pos:ref:alt)"""
            case Feature.SPAN:
                return """genomic region to query; please specify as chrN:start-end or N:start-end"""
            case _:
                raise NotImplementedError(f'Validation for feature type {featureType} not yet implemented.')
        
    def __call__(self, location):
        try:
            return location
        
        except Exception as e:
            raise e
                

```


* genomicsdb metadata
* FILER validate tracks <-> filter for data_store?
* collection data search endpoint (i.e., only search w/in a collection)
* feature scores: basic & annotated? can we generalize across the gene, dataset, and variant responses

* requestData messages & caching

```log
```

* **URGENT**: hg19 genome browser

* **URGENT**: custom error for zero-length responses for views - should we render a page?

```json
{
  "error": "zero-length response; cannot generate view",
  "msg": "An unexpected error occurred.  Please submit a `bug` GitHub issue containing this full error response at: https://github.com/NIAGADS/niagads-api/issues",
  "stack_trace": [
    "  File '/opt/venv/lib/python3.10/site-packages/starlette/_exception_handler.py', line 42, in wrapped_app    await app(scope, receive, sender)",
    "  File '/opt/venv/lib/python3.10/site-packages/starlette/routing.py', line 73, in app    response = await f(request)",
    "  File '/opt/venv/lib/python3.10/site-packages/fastapi/routing.py', line 301, in app    raw_response = await run_endpoint_function(",
    "  File '/opt/venv/lib/python3.10/site-packages/fastapi/routing.py', line 212, in run_endpoint_function    return await dependant.call(**values)",
    "  File '/app/api/routers/redirect/routes/view.py', line 36, in get_table_view    response = originatingResponse.to_view(ResponseFormat.TABLE, id=cacheKey)",
    "  File '/app/api/routers/filer/models/track_response_model.py', line 129, in to_view    return super().to_view(view, **kwargs)",
    "  File '/app/api/response_models/base_models.py', line 197, in to_view    return super().to_view(view, **kwargs)",
    "  File '/app/api/response_models/base_models.py', line 137, in to_view    return super().to_view(view, **kwargs)",
    "  File '/app/api/response_models/base_models.py', line 114, in to_view    raise RuntimeError('zero-length response; cannot generate view')"
  ],
  "request": "/redirect/view/table/7a93f493cc5eeb03cbf0566ab9b00c46"
}
```

## microservices

* don't limit site feature searches but limit the record pages -> if not in collection (FeatureCollection), then don't render and point to GenomicsDB

## GenomicsDB

### Table Views

* change `variant` and `gene` fields to `link` cells
* change `p_value` fields to `p_value` cells
* make sure `neg_log10_pvalue` is hidden and/or remove
* study groups
* cohorts & TextListDataCells; not working; see code
  
## Swagger

* sort order of tags; see <https://github.com/flasgger/flasgger/issues/487> for starters

## Pagination

* use [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) to prefetch and cache +/-2 pages (full result?)

## healthchecks

* check DB connections at app startup
* FILER API endpoints
* GenomicsDB? for gene/variant quick links

## browser config and session

* endpoint name?
* minimum required
* field mapping - at SQLModel level?

## models

* revisit and abstract out

## infrastructure questions

* rate limits
* server for live deployment (can it stay on webserver?)
* cron job for log clean up
* contact us email *resolved*
* robots.txt

## route roots

* return title, description, publication, record types, count of number of records

## Documentation

> get rid of redoc in next.js?

* FAST-API supports redoc: <http://localhost:8000/redoc>

* Add code samples to OpenAPI spec generated by FAST-API <https://github.com/fastapi/fastapi/discussions/8946>
  * depends on having a directory of code samples
  * see <https://github.com/fastapi/fastapi/issues/2111> for better answer

* java: <https://swagger.io/docs/open-source-tools/swagger-codegen/>
* npm

```text
Step 3: Generate Client Library

Use openapi-generator-cli to generate client libraries from your OpenAPI specification. This simplifies interacting with your API from various programming languages.

openapi-generator-cli generate -i path-to-your-openapi-spec.yaml -g javascript -o /path-to-output-director
```

## Caching

* internal cache key: from request (endpoing & alphabetized parameters)
* external cache key (view endpoints): request_id + `_view_data_element` and `namespace` = `view`

## parameters

* `page` should be a positive number or None

## IGV

* `session` endpoint

## Collections

* include assembly?
* allow keyword/filters searches within collections?

## FILER API

* sorting counts data request
* `hg38-lifted` genome build
* summary response review
* **URGENT**: limits?
  * span
  * number of tracks -> `counts` response format should return the total number of tracks and a message that further filtering is needed
* catch errors, especially w/parallel fetches:
  
```python
except aiohttp.ClientConnectionError as e:
    # deal with this type of exception
except aiohttp.ClientResponseError as e:
    # handle individually
except asyncio.exceptions.TimeoutError as e:
```

### FILER Cache DB

* eQTL (Catalogue) data source is not being parsed correctly
* update biosample_term to pull from `original_term` field in track description
* add antibody targets to searchable text during cache build
  > these should be added; need to debug to figure out why the aren't

### FILER - Raw

* what is an overlap? contained within vs overlap

## Error Handling

* response size too large; see `__page_data_query`; <http://localhost:8000/filer/data/search?content=full&page=1&assembly=GRCh38&loc=chr19%3A1038997-1066572&keyword=lung&format=JSON>

## ValidationErrors

* should format as follows

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

for example:

```json
{"error":"[{'type': 'enum', 'loc': ('query', 'format'), 'msg': \"Input should be 'json' or 'table'\", 'input': 'bob', 'ctx': {'expected': \"'json' or 'table'\"}}]","msg":"Invalid parameter value"}
```

## session storage / redirects

* use session to count requests and assign cache keys? maybe
* definitely use for credentials

## Overall great suggestions

* <https://github.com/zhanymkanov/fastapi-best-practices>
* <https://levelup.gitconnected.com/17-useful-middlewares-for-fastapi-that-you-should-know-about-951c2b0869c7>

## Security and Sanitizing

* Very good + rate limiter: <https://escape.tech/blog/how-to-secure-fastapi-api/#validate-and-sanitize-user-input>
* Middleware for `bleaching`: <https://github.com/tiangolo/fastapi/discussions/8354>
* generic for Python APIs: <https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4>

* nh3 for XSS <https://github.com/messense/nh3>

## Custom operators in query parameters

* <https://stackoverflow.com/questions/40618327/how-to-design-generic-filtering-operators-in-the-query-string-of-an-api>

## Error handling & field validation

* <https://stackoverflow.com/a/75545471>
* <https://stackoverflow.com/questions/61392633/how-to-validate-more-than-one-field-of-a-pydantic-model/71258131#71258131>
