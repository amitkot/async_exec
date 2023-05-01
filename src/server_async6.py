import importlib.util
import sys

from fastapi import FastAPI

app = FastAPI()

async_module_code = """
import asyncio

async def async_task(x, y):
    print(f'running with {x}, {y}')
    await asyncio.sleep(x)
    return x * y
"""


def import_async_module():
    module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader("my_module", loader=None)
    )
    exec(async_module_code, module.__dict__)
    sys.modules["my_module"] = module


import_async_module()
import my_module


async def run_in_executor(async_code):
    result = await my_module.async_task(x, y)
    return result


@app.get("/calculate")
async def calculate(x: int, y: int):
    if 1 <= x <= 5 and 1 <= y <= 100:
        result = await my_module.async_task(x, y)
        return {"result": result}
    else:
        return {
            "error": "Invalid input. X must be between 1-5 and Y must be between 1-100."
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_async6:app", host="127.0.0.1", port=8000, log_level="info")
