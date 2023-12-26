import asyncio
import aiohttp

async def fetch_user_data():
    url = 'https://randomuser.me/api/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            response.raise_for_status()
            return await response.json()

async def fetch_post_data():
    url = 'https://catfact.ninja/fact' # using random cat fats
    async with aiohttp.ClientSession() as seesion:
        async with seesion.get(url=url) as response:
            response.raise_for_status()
            return await response.json()
        

async def main():
    task = asyncio.gather(
        fetch_user_data(),
        fetch_post_data()
    )

    print("Asyncio Gather is Created:       ")
    await task 
    print(task)


if __name__ == "__main__":
    asyncio.run(main())




