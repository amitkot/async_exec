import asyncio
import httpx


async def send_request(x, y):
    async with httpx.AsyncClient() as client:
        print(f"calling with {x}, {y}")
        response = await client.get(
            f"http://127.0.0.1:8000/calculate?x={x}&y={y}", timeout=10
        )
        res = response.json()
        print(f"--- result: {res}")
        return res


async def main():
    tasks = [
        send_request(4, 15),
        send_request(1, 90),
        send_request(2, 45),
        send_request(3, 20),
        send_request(4, 10),
        send_request(1, 70),
        send_request(4, 15),
        send_request(1, 90),
        send_request(2, 45),
        send_request(3, 20),
        send_request(4, 10),
        send_request(1, 70),
        send_request(4, 15),
        send_request(1, 90),
        send_request(2, 45),
        send_request(3, 20),
        send_request(4, 10),
        send_request(1, 70),
        send_request(5, 5),
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
