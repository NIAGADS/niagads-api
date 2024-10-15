# TODOs



## current

```log
2024-10-15 12:55:48,755 INFO sqlalchemy.engine.Engine SELECT serverapplication.filertrack.track_id 
FROM serverapplication.filertrack 
WHERE serverapplication.filertrack.genome_build = $1::VARCHAR AND (serverapplication.filertrack.searchable_text ~* $2::VARCHAR OR serverapplication.filertrack.antibody_target ~* $3::VARCHAR) ORDER BY serverapplication.filertrack.track_id
2024-10-15 12:55:48,756 INFO sqlalchemy.engine.Engine [cached since 42.94s ago] ('GRCh38', 'brain', 'brain')
2024-10-15 12:55:52,835 INFO sqlalchemy.engine.Engine ROLLBACK
```

> ? huh ? why is it searching searchable text & antibody target -- revisit `keyword search`?

* update biosample_term to pull from `original_term` field in track description

## Multiple Database Connections

* <https://stackoverflow.com/questions/70081977/multiple-database-connections-using-fastapi>

## Security and Sanitizing

* Very good + rate limiter: <https://escape.tech/blog/how-to-secure-fastapi-api/#validate-and-sanitize-user-input>
* Middleware for `bleaching`: https://github.com/tiangolo/fastapi/discussions/8354
* generic for Python APIs: https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4

* nh3 for XSS <https://github.com/messense/nh3>

## Custom operators in query parameters

* <https://stackoverflow.com/questions/40618327/how-to-design-generic-filtering-operators-in-the-query-string-of-an-api>

## Error handling & field validation

* <https://stackoverflow.com/a/75545471>
* <https://stackoverflow.com/questions/61392633/how-to-validate-more-than-one-field-of-a-pydantic-model/71258131#71258131>