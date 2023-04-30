"""This does not really run in async"""

from fastapi import FastAPI
import asyncio
import concurrent.futures
import multiprocessing

app = FastAPI()

async_code_template = """
import asyncio

async def main(x, y):
    print(f'running with {x}, {y}')
    await asyncio.sleep(x)
    return x * y

result = asyncio.run(main({x}, {y}))
"""


def run_async_code(async_code):
    global result
    exec(async_code, globals())
    return result


def run_in_process(async_code):
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:
        future = executor.submit(run_async_code, async_code)
        return future.result()


@app.get("/calculate")
async def calculate(x: int, y: int):
    if 1 <= x <= 5 and 1 <= y <= 100:
        async_code = async_code_template.format(x=x, y=y)
        result = run_in_process(async_code)
        return {"result": result}
    else:
        return {"error": "Invalid input. X must be between 1-5 and Y must be between 1-100."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_async:app", host="127.0.0.1", port=8000, log_level="info")
