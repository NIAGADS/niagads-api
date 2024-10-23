# TODOs

* correct DB so that server_app user has correct grants

```log
permission denied for schema serverapplication
```

## current

```log
```

* update biosample_term to pull from `original_term` field in track description

## Caching

* let's try <https://github.com/long2ice/fastapi-cache> - `fastapi-cache2` python package

## session storage / redirects

* look into `fastsession` as it lets you use your memory store
* use memory store / cache instead of session so that we can have multiple windows w/same viz endpoint
* use session to count requests and assign cache keys? maybe
* definitely use for credentials

## Overall great suggestions

* <https://github.com/zhanymkanov/fastapi-best-practices>
* <https://levelup.gitconnected.com/17-useful-middlewares-for-fastapi-that-you-should-know-about-951c2b0869c7>

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