#  Cosmetics Ecommerce System

## Running the Project
This project uses Docker Compose to orchestrate Django and MySQL with automated health checks, ensuring zero race conditions on startup.

### Prerequisites
Docker Desktop installed and running on your machine.

Git.

### Step 1: Clone the Repository & Setup Environment Variables
Clone the repository and create your local environment file from the provided template.

git clone https://github.com/techies-arise/cosmetics_ecommerce_system.git
cd cosmetics_ecommerce_system

 Create your local environment file

cp .env.example .env 

Open .env and fill in your local database credentials:

DB_NAME=cosmetics_db
DB_USER=cosmetics_user
DB_PASSWORD=secure_password_123
DB_ROOT_PASSWORD=root_secure_password_456


### Step 2: Build and Spin Up Containers
Build the containers and start the services in detached mode:

`docker compose up --build -d`

Note: The database container features an automated health check. The Django web container will wait until MySQL is fully initialized and accepting connections before starting up.

### Step 3: Run Database Migrations
Once the containers are running, apply your initial database migrations:

`docker compose exec web python manage.py migrate --settings=config.settings.development`

### Step 4: Create a Superuser
Create an administrator account to access the Django admin panel:

`docker compose exec web python manage.py createsuperuser --settings=config.settings.development`

### Step 5: Verify & Access
Web App: Open your browser and navigate to http://localhost:8000

Django Admin: Navigate to http://localhost:8000/admin

### View Container Logs:
To check application logs or debug errors, run:

`docker compose logs -f web`

### Tearing Down Environment: 
To stop all containers without losing persistent database data:

`docker compose down`