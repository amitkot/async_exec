import os
import types
from typing import Any
from fastapi import FastAPI
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# TODO: replace use of template with locals as it fucks up the f'{}' calls
sync_code_template = """
import math
# import random
import time

def sync_task(x, y):
    pp = math.pow(2, 2)
    # pp = random.randint(0, 10)
    print(f'running with {x}, {y} -', pp)
    time.sleep(x)
    return x * y

def main(x, y):
    result = sync_task(x, y)
    return result

RESULT = main({x}, {y})
"""

# executor = ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())
# executor = ThreadPoolExecutor(min(32, os.cpu_count() + 4))


def run_sync_code(sync_code):
    sandbox = _prepare_sandbox()
    exec(sync_code, sandbox)
    return sandbox["RESULT"]


def custom_function():
    print("This is a custom function")


ALLOWED_MODULES = ["asyncio", "math", "datetime", "time"]


def _prepare_sandbox():
    import datetime

    def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
        base_module_name = name.split(".")[0]
        if base_module_name not in ALLOWED_MODULES:
            raise ImportError(f"Module {name} is not allowed.")
        return original_import(name, globals, locals, fromlist, level)

    original_import: types.BuiltinFunctionType = (
        getattr(__builtins__, "__import__")
        if isinstance(__builtins__, types.ModuleType)
        else __builtins__["__import__"]
    )

    allowed_builtins = {
        "print": print,
        "len": len,
        "range": range,
        "type": type,
        "object": object,
        "int": int,
        "str": str,
        # "Message": Message,
        "datetime": datetime,
        # "Step": Step,
        # "StepResult": StepResult,
        "__build_class__": __build_class__,
        "__name__": __name__,
        "__import__": custom_import,
    }

    return {
        **allowed_builtins,
        "custom_function": custom_function,
        "__builtins__": allowed_builtins,
    }


async def run_to_thread(async_code):
    result = await asyncio.to_thread(run_sync_code, async_code)
    return result


@app.get("/calculate")
async def calculate(x: int, y: int) -> dict[str, Any]:
    if 1 <= x <= 5 and 1 <= y <= 100:
        async_code = sync_code_template.format(x=x, y=y)
        result = await run_to_thread(async_code)
        return {"result": result}
    else:
        return {
            "error": "Invalid input. X must be between 1-5 and Y must be between 1-100."
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_async5:app", host="127.0.0.1", port=8000, log_level="info")
