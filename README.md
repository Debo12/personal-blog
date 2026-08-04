---

# Tutorial Notes

This section contains notes from the FastAPI tutorial series. The goal is not just to document the code but also to explain **why** each change was made.

---

# Part 2 - HTML Frontend using Jinja2 Templates

**Video:** HTML Frontend for Your API – Jinja2 Templates

**Objective**

Convert the existing REST API into a web application capable of rendering HTML pages while still exposing JSON APIs.

---

# 1. New Concepts Learned

## 1.1 Jinja2 Template Engine

FastAPI uses **Jinja2** to render HTML pages.

Instead of writing HTML inside Python code, HTML is kept inside template files.

Benefits

- Separation of concerns
- Easier maintenance
- Dynamic HTML generation
- Reusable layouts

---

## 1.2 Templates Folder

Project structure

```text
backend/
│
├── app/
│   ├── main.py
│   └── templates/
│       └── home.html
```

All HTML pages should be stored inside the `templates` directory.

---

## 1.3 HTMLResponse

Normally FastAPI returns JSON.

Example

```python
@app.get("/api/posts")
def get_posts():
    return posts
```

Response

```json
[
    {
        "title": "FastAPI"
    }
]
```

To return HTML instead,

```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
```

FastAPI now returns HTML instead of JSON.

---

## 1.4 Request Object

Every endpoint rendering a template must receive a Request object.

```python
from fastapi import Request

def home(request: Request):
```

The request object allows Jinja2 to access routing information and helper methods like `url_for()`.

---

## 1.5 Jinja2Templates

Create a template renderer.

```python
templates = Jinja2Templates(directory="app/templates")
```

This object loads HTML files from the templates folder.

---

# 2. Code Changes Made

## Before

Application only returned JSON.

```python
@app.get("/")
def home():
    return posts
```

---

## After

Application renders HTML.

```python
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "posts": posts
        }
    )
```

---

# 3. Passing Data to Templates

Python

```python
context={
    "posts": posts
}
```

Everything inside the context dictionary becomes available in HTML.

HTML

```html
{{ posts }}
```

---

# 4. Jinja Syntax

## Display Variable

```html
{{ post.title }}
```

---

## For Loop

Python

```python
for post in posts:
```

Jinja

```html
{% for post in posts %}

<h2>{{ post.title }}</h2>

{% endfor %}
```

---

## If Statement

```html
{% if posts %}

Posts Available

{% else %}

No Posts

{% endif %}
```

---

## Difference

Display value

```html
{{ }}
```

Execute logic

```html
{% %}
```

---

# 5. HTML + REST API Together

The application now exposes both HTML pages and REST APIs.

| Endpoint | Returns |
|----------|----------|
| / | HTML |
| /posts | HTML |
| /api/posts | JSON |

---

# 6. Dynamic Routes

Instead of creating

```
/posts/1

/posts/2

/posts/3
```

Create one dynamic route.

```python
@app.get("/posts/{post_id}")
def post(post_id: int):
```

FastAPI extracts

```
/posts/5
```

into

```python
post_id = 5
```

---

# 7. URL Generation

## Problem

Hardcoding links

```html
<a href="/posts/1">
```

Suppose tomorrow the route changes.

Old

```
/posts/{post_id}
```

New

```
/blog/posts/{post_id}
```

Every HTML page must be updated.

---

## Solution

Generate URLs automatically.

```html
<a href="{{ url_for('post', post_id=post.id) }}">
```

Generated URL

```
/posts/1
/posts/2
/posts/3
```

No hardcoded paths.

---

# 8. How url_for() Works

Suppose

```python
@app.get("/posts/{post_id}")
def post():
```

The function name becomes the route name.

Therefore

```html
{{ url_for("post", post_id=post.id) }}
```

means

> Generate the URL for the route whose function name is **post**.

---

# 9. Multiple URLs for Same Function

Example

```python
@app.get("/")
@app.get("/posts")
def home():
```

Question

What should

```html
{{ url_for("home") }}
```

generate?

```
/
```

or

```
/posts
```

Both point to the same function.

---

# 10. Route Name

To remove ambiguity

```python
@app.get("/", name="home")
@app.get("/posts")
def home():
```

Now

```html
{{ url_for("home") }}
```

always generates

```
/
```

Another example

```python
@app.get("/")
@app.get("/posts", name="posts-home")
def home():
```

Now

```html
{{ url_for("posts-home") }}
```

generates

```
/posts
```

---

# 11. Rule

Without route name

```html
{{ url_for("function_name") }}
```

With route name

```html
{{ url_for("route_name") }}
```

Whenever the `name` attribute exists, `url_for()` uses it instead of the function name.

---

# 12. Common Errors Encountered

## ModuleNotFoundError

```
No module named app
```

Cause

Running uvicorn from the wrong directory.

Solution

```bash
cd backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Missing jinja2

```
AssertionError:
jinja2 must be installed
```

Cause

Dependency missing.

---

## TemplateNotFound

```
home.html not found
```

Cause

Wrong template directory.

Incorrect

```python
templates = Jinja2Templates(directory="templates")
```

Correct

```python
templates = Jinja2Templates(directory="app/templates")
```

---

## HTMLResponse Missing

```
NameError:
HTMLResponse
```

Solution

```python
from fastapi.responses import HTMLResponse
```

---

## Incorrect TemplateResponse

Wrong

```python
TemplateResponse(request=request, "home.html")
```

Correct

```python
TemplateResponse(
    request=request,
    name="home.html"
)
```

Reason

Python does not allow positional arguments after keyword arguments.

---

# 13. Commands Used During This Tutorial

Start server

```bash
cd backend

source .venv/bin/activate

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify server

```bash
curl http://127.0.0.1:8000/docs
```

Swagger

```
http://localhost:8000/docs
```

---

# 14. Key Takeaways

- FastAPI can return both HTML and JSON.
- Jinja2 is the template engine used by FastAPI.
- Store HTML inside the `templates` directory.
- Every template-rendering endpoint requires a `Request` object.
- Use `HTMLResponse` for HTML pages.
- Pass variables through the `context` dictionary.
- `{{ }}` displays values.
- `{% %}` executes logic.
- Prefer `url_for()` instead of hardcoded URLs.
- When multiple routes map to the same function, use the `name` attribute to specify which URL should be generated.
- Keep presentation (HTML) separate from application logic (Python).

---

# Interview Questions

### Why is Request required while rendering templates?

Because Jinja2 uses the Request object for routing information, URL generation (`url_for()`), and other request-specific context.

---

### Why should we use `url_for()` instead of hardcoding URLs?

- Prevents broken links when routes change.
- Centralizes route management.
- Makes templates easier to maintain.

---

### Difference between JSONResponse and HTMLResponse?

| JSONResponse | HTMLResponse |
|--------------|--------------|
| Returns JSON | Returns HTML |
| Used for APIs | Used for webpages |

---

### Difference between `{{ }}` and `{% %}`?

| `{{ }}` | `{% %}` |
|----------|----------|
| Display data | Execute logic |
| Variables | Loops, if, blocks |