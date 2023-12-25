import asyncio
import requests 


async def fetch_data():
    url = 'https://www.boredapi.com/api/activity'
    response = requests.get(url)


    try:
        if(response.status_code == 200):
            return response.json()
        else:
            return {"Error": "Unsuccessful request"}
    
    except Exception as e:
        print(e)

async def main():
    task = asyncio.create_task(fetch_data())

    print("Task created")

    value = await task

    print(value)

if __name__ == "__main__":
    asyncio.run(main())