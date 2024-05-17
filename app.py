"""
FastAPI test application
"""
# Installed
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles


# Main application
app = FastAPI(root_path="/fastapi")


@app.get('/')
def app_home(request: Request):
    img_url = request.url_for('static', path='img.png').path
    app_mount_url = request.url_for('app_mount', path="/").path
    app_router_url = request.url_for('app_router_home').path
    return HTMLResponse('\n'.join((
        r"<!DOCTYPE html>",
        r"<html>",
        r"  <head>",
        r"  </head>",
        r"  <body>",
        f"    <h1>Main application with root_path '{request.scope['root_path']}'</h1>",
        f'    <img src="{img_url}" height="100px">',
        f'    <form action="{app_mount_url}" method="POST" target="app_mount_result">',
        r'      <input type="submit" value="submit">',
        r"    </form>",
        r'    <iframe id="app-mount-result" name="app_mount_result" height="100px" width="100%"></iframe>',
        f'    <form action="{app_router_url}" method="POST" target="app_router_result">',
        r'      <input type="submit" value="submit">',
        r"    </form>",
        r'    <iframe id="app-router-result" name="app_router_result" height="100px" width="100%"></iframe>',
        r"  </body>",
        r"</html>"
    )))


# Mounts
# -----------------------------------------------------------------------------
app_mount = FastAPI()


@app_mount.post('/')
def app_mount_home(request: Request):
    return PlainTextResponse(
        f"Requested subapplication endpoint '{request.url}' with root_path "
        f"{request.scope['root_path']}"
    )


app.mount("/app_mount/", app_mount, 'app_mount')
app.mount("/static/", StaticFiles(directory='static'), name="static")


# Routers
# -----------------------------------------------------------------------------
app_router = APIRouter()


@app_router.post('/')
def app_router_home(request: Request):
    return PlainTextResponse(
        f"Requested subapplication endpoint '{request.url}' with root_path "
        f"{request.scope['root_path']}"
    )


app.include_router(app_router, prefix="/app_router")


if __name__ == "__main__":
    # Run Server
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=40001,
        reload=True,
        root_path=app.root_path
    )
