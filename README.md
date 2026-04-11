# 🧠 Task Manager

Full-stack task manager application with categories, built using FastAPI and React.

---

## 🚀 Description

This project is a simple but production-like full-stack application where users can:

* ✅ Create, update and delete tasks
* ✅ Mark tasks as completed
* ✅ Create and manage categories

The backend follows a clean architecture pattern:
**Router → Service → Repository → Database**

---

## 🛠 Tech Stack

### 🔹 Backend

* FastAPI
* SQLAlchemy (ORM)
* Uvicorn
* Pydantic

### 🔹 Frontend

* React
* Axios

### 🔹 Other

* Docker (work in progress)

---

## ⚙️ Run Locally

### 1. Clone repository

```bash
git clone https://github.com/NIkitaPonomariov/Task-Manager-fastApi-app.git
cd  Task-Manager-fastApi-app
```

---

### 2. Run Backend

```bash
cd backend

poetry install
poetry shell

uvicorn backend.main:app --reload --port 8080
```

📍 Backend URL:
http://localhost:8080

---

### 3. Run Frontend

```bash
cd frontend

npm install
npm start
```

📍 Frontend URL:
http://localhost:3000

---

## 📡 API Endpoints

### 📝 Tasks

* `GET /tasks` → Get all tasks
* `POST /tasks` → Create task
* `PATCH /tasks/{id}` → Update task
* `DELETE /tasks/{id}` → Delete task

### 📂 Categories

* `GET /categories` → Get all categories
* `POST /categories` → Create category
* `PATCH /categories/{id}` → Update category
* `DELETE /categories/{id}` → Delete category

---

## 🧠 Architecture

The backend is structured using a layered approach:

* **Router** → handles HTTP requests
* **Service** → business logic & validation
* **Repository** → database operations
* **Models** → SQLAlchemy ORM

This structure makes the project scalable and easy to maintain.

---

## 🐳 Docker

Docker setup is currently in progress.

Planned:

* Backend container
* Frontend container
* Database container

---


## 💡 Future Improvements

* 🔗 Add relationship: Task → Category
* 🔐 Add authentication (JWT)
* 📄 Pagination & filtering
* ☁️ Deploy to cloud (Render / Railway)

---

## 👨‍💻 Author

**Nikita Ponomarov**

---

## ⭐ Notes

This project was built as a learning project to understand how real backend applications are structured and how frontend communicates with APIs.
