import asyncio
from fastapi import FastAPI

app = FastAPI()

async_module_code = """
import asyncio

async def async_task(x, y):
    print(f'running with {x}, {y}')
    await asyncio.sleep(x)
    return x * y
"""


def load_async_code(module_code):
    locals = {}
    globals = {
        "asyncio": asyncio,
    }
    exec(module_code, globals, locals)
    return locals["async_task"]


TOPICS = {}
for name, code in {
    "demo": async_module_code,
}.items():
    TOPICS[name] = load_async_code(code)


async def run_topic(topic_name, x, y):
    result = await TOPICS[topic_name](x, y)
    return result


@app.get("/calculate")
async def calculate(x: int, y: int):
    if 1 <= x <= 5 and 1 <= y <= 100:
        result = await run_topic("demo", x, y)
        return {"result": result}
    else:
        return {
            "error": "Invalid input. X must be between 1-5 and Y must be between 1-100."
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_async7:app", host="127.0.0.1", port=8000, log_level="info")
