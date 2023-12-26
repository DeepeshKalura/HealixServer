import asyncio
import requests # use the aiohttp library instead
import aiohttp


async def fetch_data():
    url = 'https://www.boredapi.com/api/activity'
    async with aiohttp.ClientSession() as seesion:
        async with seesion.get(url) as response:
            response.raise_for_status() # raise an exception if the status code is not 200
            return await response.json()


# async def fetch_data():
#     url = 'https://www.boredapi.com/api/activity'
#     response = requests.get(url)


#     try:
#         if(response.status_code == 200):
#             return response.json()
#         else:
#             return {"Error": "Unsuccessful request"}
    
#     except Exception as e:
#         print(e)

async def main():
    task = asyncio.create_task(fetch_data())

    print("Task created")

    value = await task

    print(value)

if __name__ == "__main__":
    asyncio.run(main())