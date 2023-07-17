# Notes

## Section 1 & 2: Intro and Setup

### Virtual Environment

Create virtual environment:

|OS|Command|
|:-:|:-:|
|Windows|`py -3 -m venv <name>`|
|macOS/Linux|`python3 -m venv <name>`|

The virtual environment is isolated in the project folder. Thus, `<name>` is often `venv`.

Disadvantages of using `venv`:

- Because the destination name and the module name are often the same, new users might be confused. Consider what a beginner might make of this: `python -m venv venv`. If that’s obtuse to you, the first `venv` is the module name, and the second is a path we’re passing to it as an argument.
- The commands to activate environments are different in Windows and Linux-like environments.
- If you use `.venv` as the directory name, be aware that VS Code may not be able to locate your Python interpreter. You may have to switch to “venv” to make that happen.
- You’ll need to add `.venv` or `venv` to your `.gitignore` file if you use `git`.

## Section 3: FastAPI

### Path Operations (Route - Other Frameworks)

Example of a path operation:

<img src="images/path_operation.png" width=800>

```python
@app.get("/")
async def root():
    return {"message": "hello world"}
```

It consists of 2 components:

- The function: `async def root()`.
- The decorator: `@app.get("/")` turns the function into an API endpoint.
  - `/` is the path.
  - `get` is the HTTP method.

### HTTP Requests

<img src="images/get_vs_post_http_request.png" width=800>

### Schema Validation with Pydantic

Why do we need schema?

- It's a pain to get all the values from the body.
- The client can send whatever data they want.
- The data isn't getting validated.
- We ultimately want to force the client to send data in a schema that we expect.

If we want to convert a `Pydantic` model to a `dict`, we can use the `model_dump()` function. Previously, it's the `dict()` method but it has been deprecated.

```python
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool

post = Post()

post.model_dump()
```

### Best practices from [REST Resource Naming Guide](https://restfulapi.net/resource-naming/)

#### Use nouns to represent resources

```endpoint
http://api.example.com/device-management/managed-devices
http://api.example.com/device-management/managed-devices/{device-id}
http://api.example.com/user-management/users
http://api.example.com/user-management/users/{id}
```

A **document** resource is a singular concept that is akin to an object instance or database record. Use **singular name** to denote document resource archetype.

```endpoint
http://api.example.com/device-management/managed-devices/{device-id}
http://api.example.com/user-management/users/{id}
http://api.example.com/user-management/users/admin
```

A **collection** resource is a server-managed directory of resources. Use **plural noun** to denote collection resource archetype.

```endpoint
http://api.example.com/device-management/managed-devices
http://api.example.com/user-management/users
http://api.example.com/user-management/users/{id}/accounts
```

A **store** is a client-managed resource repository. A store resource lets an API client put resources in, get them back out, and decide when to delete them. Use a **plural noun** to denote a store resource archetype.

```endpoint
http://api.example.com/song-management/users/{id}/playlists
```

A **controller** resource models a procedural concept. Controller resources are like executable functions, with parameters and return values; inputs and outputs. Use **verb** to denote controller resource archetype.

```endpoint
http://api.example.com/cart-management/users/{id}/cart/checkout http://api.example.com/song-management/users/{id}/playlist/play
```

#### Consistency is key

- Use forward slash (`/`) to indicate hierarchical relationships.
- Do not use trailing forward slash (`/`) in URIs.
- Use hyphens (`-`) to improve the readability of URIs.
- Do not use underscores (`_`) in URIs.
- Use lowercase letters in URIS.

#### Do not use file extensions

File extensions look bad and do not add any advantage. Removing them decreases the length of URIs as well. No reason to keep them

```endpoint
http://api.example.com/device-management/managed-devices.xml /*Do not use it*/

http://api.example.com/device-management/managed-devices /*This is correct URI*/
```

#### Never use CRUD function names in URIs

We should use HTTP request methods to indicate which CRUD function is performed.

```endpoint
HTTP GET http://api.example.com/device-management/managed-devices  //Get all devices
HTTP POST http://api.example.com/device-management/managed-devices  //Create new Device

HTTP GET http://api.example.com/device-management/managed-devices/{id}  //Get device for given Id
HTTP PUT http://api.example.com/device-management/managed-devices/{id}  //Update device for given Id
HTTP DELETE http://api.example.com/device-management/managed-devices/{id}  //Delete device for given Id
```

#### Use query component to filter URI collections

Often, you will encounter requirements where you will need a collection of resources sorted, filtered, or limited based on some specific resource attribute. For this requirement, do not create new APIs – instead, enable sorting, filtering, and pagination capabilities in resource collection API and pass the input parameters as query parameters. e.g.

```endpoint
http://api.example.com/device-management/managed-devices
http://api.example.com/device-management/managed-devices?region=USA
http://api.example.com/device-management/managed-devices?region=USA&brand=XYZ
http://api.example.com/device-management/managed-devices?region=USA&brand=XYZ&sort=installation-date
```

### CRUD Operations

<img src="images/crud_operation.png" width=800>

Change default status code by supplying the `status_code` parameter.

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED)
```

### Automatic Documentation

FastAPI automatically generates documentation for all the endpoints.

- Swagger UI: `http://{host}:{port}/docs`
- ReDoc: `http://{host}:{port}/redoc`

## Section 4: Databases

### Database

Database is a collection of organised data that can be easily accessed and managed.

We don't work or interact with databases directly. Instead, we use a Database Management System (DBMS) to interact with the database.

<img src="images/dbms.png" width=800>

Popular DBMS:

|Type|DBMS|
|:-:|:-:|
|Relational|MySQL, PostgreSQL, Oracle, SQL Server|
|NoSQL|MongoDB, DynamoDB, Oracle, SQL Server|

**Postgres**: Each instance of `postgres` can be carved into multiple separate databases.

- By default, every `postgres` installation comes with one database already created called `postgres`.
- This is important because `postgres` requires you to specify the name of the database to make a connection. So there needs to be always one database.

Postgres DataTypes:

|Data Type|Postgres|Python|
|:-|:-|:-|
|Numeric|`int`, `decimal`, `precision`|`int`, `float`|
|Text|`varchar`, `text`|`str`|
|Boolean|`bool`|`bool`|
|Sequence|`array`|`list`|

For `postgres`, if you want to return a newly created/updated item, you need to use `RETURNING` keyword.

```sql
INSERT INTO products (name, price, inventory)
VALUES ('RTX-4070', 1000, 10), ('RTX-4080', 1500, 10)
RETURNING *;
```

### Recap of Concepts

**Primary Key** is a column or group of columns that uniquely identifies each row in a table. A table can have one and only one primary key.

- The primary key does not have to be the `id` column. It's up to you to decide which column uniquely defines each record.
- In the below example, since an email can only be registered once, the email column can also be used as the primary key.

<img src="images/primary_key.png" width=800>

**UNIQUE** constraint can be applied to any column to make sure every record has a unique value for that column.

<img src="images/unique_constraint.png" width=800>

**NULL** constraint: by default, when adding a new entry to a database, any column can be left blank. When a column is left blank, it has a `null` value. If you need column to be properly filled in to create a new record, a **NOT NULL** constraint can be applied to the column to ensure that the column is never left blank.

<img src="images/null_constraint.png" width=800>

## Section 5: Python & Raw SQL

### Connecting to Postgres Using Python

We'll use `psycopg2` library to connect to `postgres` database. `psycopg2` is the most popular PostgreSQL database adapter for the Python programming language.

```python
while True:
    try:
        conn = psycopg2.connect(
            host=f"{host}",
            database=f"{database}",
            user=f"{username}",
            password=f"{password}",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        time.sleep(2)
```

**IMPORTANT**: In order to avoid `sql injection` attacks, we should never use string concatenation / f-string to build SQL queries. Instead, we should use parameterised queries (also known as **prepared statements** with variable binding) with the `%` operator when using user-supplied data. Read more about this [here](https://help.securityjourney.com/en/articles/6719498-python-string-formatting-and-sql-injection-attacks).

```python
# DO THIS
cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)", (post.title, post.content, post.published))

# DO NOT DO THIS
cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
```

## Section 6: Object Relational Mapper (ORM)

### Object Relational Mapper (ORM)

ORM is a layer of abstraction that sits between the database and the API application. In the context of databases, an ORM translates data between an object-oriented programming language and a relational database. We can **perform all database operations through traditional python code**. No more SQL!

<img src="images/object_relational_mapper.png" width=800>

What can ORMs do?

- Instead of manually defining tables in `postgres`, we can define our tables as python models.

```python
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
```

- Queries can be made exclusively through python code. No SQL is necessary.

```python
db.query(models.Post).filter(models.Post.id == id).first()
```

### SQLAlchemy - ORM for Python

**SQLAlchemy** is one of the most popular ORMs for python. It is a standalone library and has no association with FastAPI. It can be used with any other python web frameworks or any python-based applications. **SQLAlchemy** (or ORM in general) has no way of talking directly to the database, we'll still need to install the specific database driver (`psycopg2` in this case).

Database URL for SQLAlchemy:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<postgresserver>/<database_name>
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
```

Read more about how to **use SQL (Relational) Databases with FastAPI** [here](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Section 7: Pydantic Models

### Pydantic Models

Schema/Pydantic Model vs. ORM Model:

- **Schema/Pydantic Models** define the structure of a request & response. This ensures that when a user wants to create a post, the request will only go through if it has a `title` and `content` in the body.

<img src="images/schema_pydantic_model.png" width=800>

- **SQLAlchemy Models** are responsible for defining the columns of our `posts` table within `postgres`. The models are used to query, create, delete and update entries within the database.

### Response Models

To define the response model, we can use the `response_model` parameter in the `@app.get()` decorator.

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
```

Pydantic's `from_attributes` (changed from `orm_mode`) will tell the Pydantic model to read the data even if it's not a `dict`, but an ORM model (or any other arbitrary object with attributes).

Use `from typing import List` to return a list of items.

```python
from typing import List

@app.get("/posts", response_model=List[schemas.Post])
```

## Section 8: Authentication & Users

`passlib` is a great Python package to handle password hashes. It supports many secure hashing algorithms and utilities to work with them. The recommended algorithm is `bcrypt`.

```bash
pip install passlib[bcrypt]
```

### Router Prefix & Tags

We can use `prefix` parameter in the `APIRouter` to add a prefix to all the endpoints in the router.

```python
from fastapi import APIRouter

router = APIRouter(prefix="/posts")
```

We can use `tags` parameter in the `APIRouter` to add tags to all the endpoints in the router. This will result in separate section in the docs for the endpoints in the router.

```python
router = APIRouter(prefix="/posts", tags=["Posts"])
```

### Authentication

[More about this](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

There's nothing stored in the server. The server only verifies the validity of the token. If the token is valid, the server will return the data.

<img src="images/jwt_token_authentication.png" width=800>

**JWT** means `JSON Web Tokens`. It's standard to codify a JSON object in a long dense string without spaces. It looks like this:

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

<img src="images/jwt_example.png" width=800>

The token consists of 3 parts:

- **Header**: contains the algorithm used to generate the signature.
- **Payload**: contains the data that we want to transmit. We can send whatever data we want.
- **Verify Signature**: used to verify the token.

**DO NOTE THAT THE TOKEN IS NOT ENCRYPTED**, so anyone can read it. Nonetheless, it's **signed**, so when you receive a token that you emitted, you can verify that you actually emitted it. That way, you can create a token with an expiration of, let's say, 1 week. And then when the user comes back the next day with the token, you know that the user is still logged in to your system. After a week, the token will expire, and the user will not be authorised anymore and will have to sign in again to get a new token. And if the user (or a third party) tried to modify the token to change the expiration, you would be able to discover it, because the signature wouldn't match.

[Check out how JWT works](https://jwt.io/)

The **purpose of Signature** is to verify that the token was emitted by the server and that it wasn't modified by anyone else. The **super secret password** resides on the API server.

<img src="images/purpose_of_signature.png" width=800>

### Login Process

<img src="images/login_process.png" width=800>

### OAuth2

Generate a `SECRET_KEY` by running `openssl rand -hex 32` in the terminal.

```python
SECRET_KEY = "c8f8cca94e761b7c2bb286899f9952a9ae5637cd258f37901917e82646018274"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Postman Advanced Feature

Set an environment variable in Postman:

```postman
pm.environment.set("JWT", pm.response.json().access_token);
```

## Section 9: Relationships

### Foreign Keys

<img src="images/one_to_many.png" width=800>

### Postgres Foreign Keys

<img src="images/pgadmin4_fkey_setup.png" width=800>

### SQLAlchemy Foreign Keys

```python
class Post(Base):
    __tablename__ = "posts"

    ...
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
```

### SQLAlchemy Relationship

```python
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    ...
    owner = relationship("User")
```

### Query Parameters

Examples:

- `http://localhost:8000/posts?limit=10`
- `http://localhost:8000/posts?limit=10&skip=2`
- `http://localhost:8000/posts?limit=10&search=new%20new` (`%20` means space in URL)

```python
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    ...
    posts = (
        db.query(models.Post)
        .where(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
```

### Environment Variables

We can use environment variables to store sensitive information such as database credentials. This is a better practice than hardcoding the credentials in the code.

```bash
export ENV_VAR_EXAMPLE="example"
```

Environment variables will always be read as strings. If we want to use them as other data types, we need to convert them. `Pydantic` can be used to perform this conversion for us.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

In `development-mode`, it's best practice to store the environment variables in a `.env` file. In `production`, we'll set the environment variables in the server.


## Section 10: Vote/Like System

Requirements:

- Users should be able to like a post.
- Users should only be able to like a post once.
- Retrieving posts should also fetch the total number of likes.

Solution: We should have a table to store the number of likes for each post.

- Column referencing `posts.id`.
- Column referencing `users.id` who liked the post.
- Every combination of `posts.id` and `users.id` should be unique since a user can only like the post once.

<img src="images/vote_like.png" width=800>

In order to implement this solution, we will use **composite keys** meaning:

- Primary key that spans multiple columns.
- Since primary keys must be unique, this will ensure no user can like a post twice.

<img src="images/composite_key.png">

**Vote Route**:

- Path will be at `/vote`.
- The `users.id` will be extracted from the JWT token.
- The body will contain the `posts.id` the user is voting on as well as the direction of the vote.
  - A vote direction of `1` means we want to add a vote.
  - A vote direction of `0` means we want to delete a vote.

    ```json
    {
        "post_id": 1432,
        "vote_dir": 0
    }
    ```

## Section 11: Database Migration with Alembic

### Database Migration

Developers can track changes to code and rollback code easily with `git`. However, it's not easy to track changes to the database. This is where **database migration** comes in. Database migration **allows us to incrementally track changes to database schemas and rollback changes to any point in time**.

### Alembic

For migration purpose, we'll use a tool called `alembic` to make changes to our database. `alembic` can also automatically pull database models from `SQLAlchemy` and generate the proper tables.

Steps to use `alembic`:

**Step 1**: we'll start by initialising `alembic` in a folder (called `alembic` in this example).

```bash
alembic init alembic
```

**Step 2**: we'll need to give `alembic` access to the `Base` object found in `app/models.py`. This will allow `alembic` to have access to all our models. In addition, we'll import `Base` inside `env.py` and update `target_metadata`

```python
## env.py file created by alembic init alembic

from app.models import Base

target_metadata = Base.metadata
```

**Step 3**: We'll need to update the `sqlalchemy.url` in `alembic.ini` file. This is exactly the same as the `SQLALCHEMY_DATABASE_URL` in `app/database.py`. We can either choose to hardcode the `sqlalchemy.url` or override `sqlalchemy.url` option in `env.py` file.

```python
config.set_main_option(
    name="sqlalchemy.url",
    value=(
        f"""postgresql://{settings.database_username}:{settings.database_password}"""
        f"""@{settings.database_hostname}:{settings.database_port}/"""
        f"""{settings.database_name}"""
    ),
)
```

**Step 4**: We'll start with creating the `posts` table from scratch. The `upgrade` and `downgrade` functions are automatically generated by `alembic`. `upgrade()` runs the commands for whatever changes we want to perform, while `downgrade()` handles rolling back the changes.

```bash
alembic revision -m "create posts table"
```

```python
## {revision}_create_posts_table.py
def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
```

**Step 5**: Since the last revision is the `head`, we can just use the following command to run the migration.

```bash
alembic upgrade head
```

```bash
alembic upgrade [REVISION]
```

**Step 6**: If we want to roll back changes, we can just run the following command.

```bash
alembic downgrade -1
```

```bash
alembic downgrade [REVISION]
```

**Step 7**: We can also use `alembic` to generate a new revision file. This will automatically generate a new revision file with the `upgrade` and `downgrade` functions.

```bash
alembic revision --autogenerate -m "auto-vote"
```

## Section 12: Pre-deployment Checklist

**Cross Origin Resource Sharing (CORS)** allows you to make requests from a web browser on one domain to a server on a different domain. By default, our API will only allow web browsers running on the same domain as our server to make requests to it.

<img src="images/cors.png" width=800>

[Read more about CORS](https://fastapi.tiangolo.com/tutorial/cors/)

It's best practice to limit the number of origins that can make requests to our API. We can do this by specifying the `origins` parameter in the `CORS` middleware.

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"] # all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
