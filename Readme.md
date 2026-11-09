## 🛠️ Docker Development & Production Workflow

We use an optimized, pure-Python architecture featuring **PyMySQL** and **Pillow (Binary Wheels)**. This setup completely eliminates the need for heavy C-compilers or system-level dependencies. 

Our local environment runs on **Docker Compose** for instant code updates, while using a clean, production-ready image for deployments.

---

###  Local Development Setup

Follow these steps to get up and running on your local machine in under a minute.

#### 1. Initial Build & Start
To build the image and start the application services for the first time, run:
```bash
docker compose up --build
```
*Note: This will finish in seconds because all dependencies are pre-compiled or pure Python!*

#### 2. Standard Daily Workflow
For daily development, you do not need to rebuild the image. Simply run:
```bash
docker compose up
```
Container logs
```bash
docker compose logs -f web
```

* **Live Code Updates:** Your local directory is mounted live into the container. Any changes you make to your Python/Django files will trigger an **instant reload** without needing a container restart.
* **Accessing the App:** Open your browser and go to [http://localhost:8000](http://localhost:8000).

#### 3. Adding New Python Packages
If you add or update a package in `requirements.txt`, let the team know to trigger a fast dependency update:
```bash
docker compose build
```

#### 4. Stopping the Environment
To safely shut down the running containers, press `Ctrl + C` in your terminal, or run:
```bash
docker compose down
```

#### 5.Creating SuperUser
```bash
docker compose exec web python manage.py createsuperuser --settings=config.settings.development
```

#### 6.Making migrations -eg products
Make migration
```bash
docker compose exec web python manage.py makemigrations products --settings=config.settings.development
```
Migrate
```bash
docker compose exec web python manage.py migrate --settings=config.settings.development
```

---

###  Production Deployment

Our `Dockerfile` is optimized to be lightweight and highly secure for live production environments. 

* **Production Server:** In production, the container automatically spins up using **Gunicorn** for optimal performance and concurrency.
* **Dev Override:** Locally, our `docker-compose.yml` automatically overrides this to use Django's `runserver` for debug mode and logging.

To build or test the production image target locally, you can run a standard build:
```bash
docker build -t my-django-app:latest .
```
