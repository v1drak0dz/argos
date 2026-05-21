
import uvicorn
from fastapi import  FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.task_storage import load_tasks
from routes.jobs import jobs_routes
from routes.status import status_routes


load_tasks()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
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


app.include_router(status_routes)
app.include_router(jobs_routes)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=8000,
        reload=True,
    )
