from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/", include_in_schema=False)
@app.get("/posts",include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"posts": posts, "title": "Home"}
    )

@app.get("/api/posts")
def get_all_posts():
    return posts

@app.get("/api/post/{post_id}")
def get_post_by_id(post_id: int):
    for post in posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "post not found"})

