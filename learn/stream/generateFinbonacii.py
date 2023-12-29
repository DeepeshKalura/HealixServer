import asyncio

async def generateFiboanicii():
    a = 0 
    b = 1

    for _ in range(1, 100):
        yield a    
        a, b = b, a + b # it also mean like c = a+b, a = b, b = c


async def main():
    async for num in generateFiboanicii():
        print(num)

if __name__ == "__main__":
    asyncio.run(main())