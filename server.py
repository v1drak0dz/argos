from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.paths import STATIC_DIR, TEMPLATES_DIR
from core.state import tasks
from core.version import APP_VERSION
from routes.jobs import jobs_routes
from routes.status import status_routes
from services.task_storage import load_tasks

load_tasks(tasks)

app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    return templates.TemplateResponse(
        request,
        name="index.html",
    )


@app.get("/version/")
async def get_version():
    return {"version": APP_VERSION}


app.include_router(status_routes)
app.include_router(jobs_routes)


if __name__ == "__main__":
    import threading
    import webbrowser

    import uvicorn

    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
