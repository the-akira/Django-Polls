# Django Polls

Django Polls is an App inspired by the [Django Documentation Tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).

## Installation

Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

### Clone the Repository

```
git clone https://github.com/the-akira/Django-Polls.git
```

### Inside the Main Directory

Build and run the application

```
docker-compose up --build
```

You can now open your Web Browser and navigate to `http://127.0.0.1:8000/` to see the Web Application.

### Unit Tests

Accessing the Docker container

```
docker exec -it polls /bin/sh
```

Running the tests

```
python manage.py test
```

### Database

Accessing the Docker container

```
docker exec -it polls_db_1 /bin/sh
```

Starting the command line prompt

```
psql -U postgres
```

Listing databases

```
\list
```

Connecting to a database

```
\connect postgres
```

Listing tables

```
\dt
```