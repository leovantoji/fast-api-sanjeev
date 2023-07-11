# Notes

## Virtual Environment

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

## Path Operations (Route - Other Frameworks)

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

## HTTP Requests

<img src="images/get_vs_post_http_request.png" width=800>

## Schema Validation with Pydantic

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

## Best practices from [REST Resource Naming Guide](https://restfulapi.net/resource-naming/)

### Use nouns to represent resources

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

### Consistency is key

- Use forward slash (`/`) to indicate hierarchical relationships.
- Do not use trailing forward slash (`/`) in URIs.
- Use hyphens (`-`) to improve the readability of URIs.
- Do not use underscores (`_`) in URIs.
- Use lowercase letters in URIS.

### Do not use file extensions

File extensions look bad and do not add any advantage. Removing them decreases the length of URIs as well. No reason to keep them

```endpoint
http://api.example.com/device-management/managed-devices.xml /*Do not use it*/

http://api.example.com/device-management/managed-devices /*This is correct URI*/
```

### Never use CRUD function names in URIs

We should use HTTP request methods to indicate which CRUD function is performed.

```endpoint
HTTP GET http://api.example.com/device-management/managed-devices  //Get all devices
HTTP POST http://api.example.com/device-management/managed-devices  //Create new Device

HTTP GET http://api.example.com/device-management/managed-devices/{id}  //Get device for given Id
HTTP PUT http://api.example.com/device-management/managed-devices/{id}  //Update device for given Id
HTTP DELETE http://api.example.com/device-management/managed-devices/{id}  //Delete device for given Id
```

### Use query component to filter URI collections

Often, you will encounter requirements where you will need a collection of resources sorted, filtered, or limited based on some specific resource attribute. For this requirement, do not create new APIs – instead, enable sorting, filtering, and pagination capabilities in resource collection API and pass the input parameters as query parameters. e.g.

```endpoint
http://api.example.com/device-management/managed-devices
http://api.example.com/device-management/managed-devices?region=USA
http://api.example.com/device-management/managed-devices?region=USA&brand=XYZ
http://api.example.com/device-management/managed-devices?region=USA&brand=XYZ&sort=installation-date
```

## CRUD Operations

<img src="images/crud_operation.png" width=800>

Change default status code by supplying the `status_code` parameter.

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED)
```

## Automatic Documentation

FastAPI automatically generates documentation for all the endpoints.

- Swagger UI: `http://{host}:{port}/docs`
- ReDoc: `http://{host}:{port}/redoc`

## Database

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

## Recap of Concepts

**Primary Key** is a column or group of columns that uniquely identifies each row in a table. A table can have one and only one primary key.

- The primary key does not have to be the `id` column. It's up to you to decide which column uniquely defines each record.
- In the below example, since an email can only be registered once, the email column can also be used as the primary key.

<img src="images/primary_key.png" width=800>

**UNIQUE** constraint can be applied to any column to make sure every record has a unique value for that column.

<img src="images/unique_constraint.png" width=800>

**NULL** constraint: by default, when adding a new entry to a database, any column can be left blank. When a column is left blank, it has a `null` value. If you need column to be properly filled in to create a new record, a **NOT NULL** constraint can be applied to the column to ensure that the column is never left blank.

<img src="images/null_constraint.png" width=800>

## Connecting to Postgres Using Python

We'll use `psycopg2` library to connect to `postgres` database. `psycopg2` is the most popular PostgreSQL database adapter for the Python programming language.

**IMPORTANT**: In order to avoid `sql injection` attacks, we should never use string concatenation / f-string to build SQL queries. Instead, we should use parameterised queries (also known as **prepared statements** with variable binding) with the `%` operator when using user-supplied data. Read more about this [here](https://help.securityjourney.com/en/articles/6719498-python-string-formatting-and-sql-injection-attacks).

```python
# DO THIS
cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)", (post.title, post.content, post.published))

# DO NOT DO THIS
cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
```
