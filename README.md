> ⚠  This repo is just an easy example of a FastAPI application running behind NGINX Proxy. It is meant to illustrate this discussion


## This are my findings

I have not been able to make a working configuration similar to yours, and I think that FastAPI's `root_path` behaviour is odd.

I think the expected behaviour of FastAPI users:

- Use ApiRouter with some prefix when you want to "group" endpoints under a specific path beginning
- Use the FastAPI `root_path` argument when you are accessing the application behind a proxy using that `path` in the URL

FastAPI application has four things:
1. A `root_path` defined as `/fastapi`
2. A sub-application mounted at `/app_mount/` path
3. A static files application mounted at `/static/` path (with just a test image inside)
4. An `APIRouter` included in the main application under the prefix `/app_router`

By running this application with the following code:
```python
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=40001,
        reload=True,
        #  root_path=app.root_path  # More on this later
    )
```

We find the following situation:

1. ☑ All the paths created with `request.url_for(...)` are prefixed by the `root_path`. *Correct because this method is used to redirect or render URLs in templates, so this way, both will work when working behind a proxy*
2. ❓All the paths work. *NOT Correct because the `root_path` is going to be removed from the URLs when calling the proxy*
3. ❓The main application and the `APIRouter` are served through the path that starts without the `root_path` and the path that starts with the `root_path`. *NOT Correct because `root_path` might be duplicating your endpoints unnecessarily*
3. ❓Both mounted applications are only served through the path that starts with the `root_path`. *NOT Correct (same as 2.)*

When running a proxy that redirects calls to the running application, you find the following situation:
- ☑ All the calls (when they reach the application) have the `root_path` removed from the URL. *Correct because this is how a proxy is supposed to work*
- ☑ Only the APIRouter paths work.
- ☠ None of the mounted applications work. as their endpoints are only reachable with `root_path` prefix.

Things I do not understand:

- Why are mounted applications only accessible to paths prefixed with `root_path`?
- How do you refer to API endpoints in the front when working behind a proxy?

I think the following schema is relatively straightforward and must be kept in mind when implementing the "composition" of applications:

![diagrama](https://github.com/tiangolo/fastapi/assets/45438989/77953f24-73f3-4bf7-9fd9-00bb951fdce8)

Finally, as a comment, I would like more detail in the documentation about how FastAPI deals with APIRouter vs. Mounted Applications. Also, I think there are sentences in the documentation that should be avoided, like [this one](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#mounting-a-sub-application), because when that is not the reality, they feel quite awkward and feed users' frustration.

