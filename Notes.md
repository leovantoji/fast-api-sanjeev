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
