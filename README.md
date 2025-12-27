# ProjetoFinalBDII

Projeto final de Base de Dados II

## Table of Contents
- [ProjetoFinalBDII](#projetofinalbdii)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [Setup](#setup)

## Technologies Used

- **Django**: Used framework for the website development.
- **PostgreSQL**: Main database engine.
- **MongoDB**: Used to store additional information about a concept of the platform.

## Setup

### Using Docker (Default & Supported Method)

> **Note:** Docker is the default and only supported way to run this project. Manual setup is not maintained.

1. **Clone the repository:**
  

2. **Configure environment variables:**
  ```bash
  cp .env.example .env
  # Edit .env file with your credentials
  ```

3. **Start with Docker Compose:**
  ```bash
  docker-compose up -d
  ```

4. **Access the application:**
  - Web app: http://localhost:8000
  - PostgreSQL: localhost:5432
  - MongoDB: localhost:27017

---

If you encounter issues or need to run management commands, you can use Docker Compose exec:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
