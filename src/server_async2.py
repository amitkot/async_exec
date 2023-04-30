from fastapi import FastAPI
import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

app = FastAPI()

async_code_template = """
import asyncio

async def async_task(x, y):
    print(f'running with {x}, {y}')
    await asyncio.sleep(x)
    return x * y

async def main(x, y):
    result = await async_task(x, y)
    return result

result = asyncio.get_event_loop().run_until_complete(main({x}, {y}))
"""

executor = ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())


def run_async_code(async_code):
    global result
    exec(async_code, globals())
    return result


async def run_in_executor(async_code):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, run_async_code, async_code)
    return result


@app.get("/calculate")
async def calculate(x: int, y: int):
    if 1 <= x <= 5 and 1 <= y <= 100:
        async_code = async_code_template.format(x=x, y=y)
        result = await run_in_executor(async_code)
        return {"result": result}
    else:
        return {"error": "Invalid input. X must be between 1-5 and Y must be between 1-100."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_async2:app", host="127.0.0.1", port=8000, log_level="info")
