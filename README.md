# FastAPI crud app


### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Azadron228/fastapi-crud.git

2. Copy .env.exmample to .env

   
3. Build and run the Docker container:
    ```bash
    docker-compose up --build

4. Migrate database:
    ```bash
    docker-compose run app alembic upgrade head


### Usage

- Access the FastAPI application at `http://localhost:8000/docs` to view the Swagger UI.

### Admin User credentials
- email: shoqan@mail.com
- password: password