# 🧠 Pydantic-main — FastAPI + MongoDB + WebSockets + Pydantic V2

A complete Python 3.13+ project demonstrating modern API development using:
- **FastAPI** (REST + WebSockets)
- **MongoDB** (via Motor)
- **Pydantic V2** models generated from JSON Schema
- **HTTP Basic Auth**
- **Modern Python packaging** with `pyproject.toml`

---

## 🚀 Features
✅ REST CRUD for Cars (MongoDB)  
✅ WebSocket chat with token auth  
✅ In-memory CRUD for demo Items  
✅ Schema-driven models via `datamodel-code-generator`  
✅ Live Swagger UI at `/swagger`  

---

## 🧩 Tech Stack
| Layer | Technology |
|--------|-------------|
| Language | Python 3.13+ |
| Framework | FastAPI + Uvicorn |
| Database | MongoDB 7 (Docker) |
| Async ORM / Driver | Motor |
| Validation | Pydantic V2 |
| Auth | HTTP Basic Auth / Base64 token for WS |
| Packaging | pyproject.toml (PEP 621) |
| Tests | pytest + httpx + websockets |

---

## ⚙️ 1️⃣ Setup MongoDB Container
Pull and run Mongo locally:

```bash
docker pull mongo:7
docker run -d   --name mongo   -p 27017:27017   mongo:7
```

Verify it’s running:
```bash
docker ps
# Look for "mongo" Up and listening on 0.0.0.0:27017
```

---

## ⚙️ 2️⃣ Clone and Enter Project
```bash
git clone <your-repo-url> Pydantic-main
cd Pydantic-main
```

---

## ⚙️ 3️⃣ Create Virtual Environment
```bash
python3.13 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
```

---

## ⚙️ 4️⃣ Install Dependencies
Editable install with dev extras:
```bash
pip install -e .[dev]
```

---

## ⚙️ 5️⃣ Environment Variables
Create a `.env` file in the project root:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=realtime_api
```

*(These defaults match your local Docker Mongo container.)*

---

## ⚙️ 6️⃣ (Optionally) Generate Pydantic Models
If you modify JSON schemas, regenerate models:

```bash
python -m scripts.generate_models
```

This uses `datamodel-code-generator` to produce updated Pydantic V2 classes.

---

## ⚙️ 7️⃣ Run the API Server
```bash
uvicorn realtime_api.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🔍 8️⃣ Explore Swagger Docs
Open: **http://127.0.0.1:8000/swagger**

Authenticate (top-right “Authorize” button):  
```
username: admin
password: changeme
```

---

## 🧪 9️⃣ Example Requests

### Create a Car
```bash
curl -u admin:changeme -X POST http://127.0.0.1:8000/cars   -H "Content-Type: application/json"   -d '{"make":"Tesla","model":"Model 3","year":2023,"color":"White","price":39999.0}'
```

### List Cars
```bash
curl -u admin:changeme http://127.0.0.1:8000/cars
```

### WebSocket Chat
Get a token:
```bash
curl http://127.0.0.1:8000/token
```

Connect in browser console:
```js
let ws = new WebSocket("ws://127.0.0.1:8000/ws?room=general&token=YWRtaW46Y2hhbmdlbWU=");
ws.onmessage = (e) => console.log(e.data);
ws.onopen = () => ws.send(JSON.stringify({ text: "hello world" }));
```

---

## 🧩 10️⃣ Run Tests
```bash
pytest -v
```

---

## 📦 11️⃣ Freeze Dependencies
After everything works:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Freeze dependencies"
```

---

## 🧱 Folder Structure
```
src/realtime_api/
├── main.py                 # FastAPI entrypoint
├── auth/                   # Auth (Basic + WS token)
├── db/mongo.py             # Async Mongo init + counters
├── models/                 # Pydantic models + schemas
├── routes/                 # REST + WebSocket endpoints
├── services/               # CRUD + WS manager logic
└── ...
scripts/
└── generate_models.py
tests/
└── pytest tests
```

---

## 🧾 Default Credentials
| Type | Username | Password |
|------|-----------|-----------|
| HTTP Basic | `admin` | `changeme` |
| WS Token | `base64("admin:changeme")` |

---

## ⚙️ Troubleshooting
| Symptom | Fix |
|----------|-----|
| `ServerSelectionTimeoutError` | Mongo container not running → `docker ps` |
| `Mongo not initialized` | App started before Mongo was reachable → wait 5s or retry |
| 401 Unauthorized | Wrong credentials in Basic Auth or WS token |
| Port in use | Change with `uvicorn --port 8001` or `-p 27018:27017` for Mongo |

---

## 🧾 License
MIT License © 2025 Your Name
