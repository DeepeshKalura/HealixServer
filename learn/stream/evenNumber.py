import asyncio


async def evenNumberGenerator():
    
    for i in range(50):
        if(i%2==0):
            yield i

async def main():
    async for i in evenNumberGenerator():
        print(i*2)




if __name__ == "__main__":
    asyncio.run(main())





