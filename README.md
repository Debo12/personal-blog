# Getting Started

Follow the steps below to set up and run the project locally.

## Prerequisites

Ensure you have the following installed:

- Docker Desktop
- Visual Studio Code
- Dev Containers extension for VS Code

---

## Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

## Open in Dev Container

1. Open the project in Visual Studio Code.
2. Press `Ctrl + Shift + P`.
3. Select **Dev Containers: Reopen in Container**.
4. Wait for the container to build and start.

---

## Activate the Virtual Environment

From the `backend` directory:

```bash
cd backend
source .venv/bin/activate
```

---

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see output similar to:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## Access the Application

Open the following URLs in your browser:

| Endpoint | URL |
|----------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI Specification | http://localhost:8000/openapi.json |
| Home Page | http://localhost:8000/ |
| Posts API | http://localhost:8000/api/posts |

---

## Stopping the Server

Press:

```text
Ctrl + C
```

---

## Troubleshooting

### Swagger UI is not accessible

- Ensure the server has started successfully.
- Verify the application is running on port `8000`.
- If using a Dev Container, make sure port `8000` is forwarded in Visual Studio Code.

### Verify the server is running

```bash
curl http://127.0.0.1:8000/docs
```

If HTML is returned, the application is running successfully.

### Restart the server

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```