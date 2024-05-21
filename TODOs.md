# TODOs

## current

```log
psycopg2.errors.UndefinedColumn: column "life_stage" of relation "filertrack" does not exist
LINE 1: ...filer_release_date", "genome_build", "is_lifted", "life_stag..."
```

## Multiple Database Connections

* <https://stackoverflow.com/questions/70081977/multiple-database-connections-using-fastapi>

## Security and Sanitizing

* Very good + rate limiter: <https://escape.tech/blog/how-to-secure-fastapi-api/#validate-and-sanitize-user-input>
* Middleware for `bleaching`: https://github.com/tiangolo/fastapi/discussions/8354
* generic for Python APIs: https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4

## Custom operators in query parameters

* <https://stackoverflow.com/questions/40618327/how-to-design-generic-filtering-operators-in-the-query-string-of-an-api>