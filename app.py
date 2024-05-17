"""
FastAPI test application
"""
# Builtins
import os
import signal
import platform
# Installed
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles


def shutdown_server():
    """Shutdown the server by brute force"""
    pid = os.getpid()
    if platform.system() != 'Windows':
        pgid = os.getpgid(pid)
    if platform.system() != 'Windows':
        os.killpg(pgid, signal.SIGKILL)
    else:
        os.kill(pid, signal.SIGTERM)

# Main application
app = FastAPI(root_path="/fastapi")


@app.get('/')
def app_home(request: Request):
    img_url = request.url_for('static', path='img.png').path
    subapp_url = request.url_for('subapp', path="/").path
    return HTMLResponse('\n'.join((
        r"<!DOCTYPE html>",
        r"<html>",
        r"  <head>",
        r"  </head>",
        r"  <body>",
        f"    <h1>Main application with root_path {request.scope['root_path']}</h1>",
        f'    <img src="{img_url}">',
        f'    <form action="{subapp_url}" method="POST" target="result">',
        r'      <input type="submit" value="submit">',
        r"    </form>",
        r'    <iframe id="result" name="result"></iframe>',
        r"  </body>",
        r"</html>"
    )))


subapp = FastAPI()
@subapp.post('/')
def subapp_home(request: Request):
    return PlainTextResponse(
        f"Requested subapplication endpoint '{request.url}' with root_path "
        f"{request.scope['root_path']}"
    )


# Mounts
app.mount("/subapp/", subapp, 'subapp')
app.mount("/static/", StaticFiles(directory='static'), name="static")


if __name__ == "__main__":
    # Run Server
    try:
        uvicorn.run(
            "__main__:app",
            host="0.0.0.0",
            port=40002,
            reload=True
        )
    except KeyboardInterrupt:
        print('⛔ Shutting down application ⛔')
    shutdown_server()
