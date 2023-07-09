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

<img src="images/path_operation.png" width=600>

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
