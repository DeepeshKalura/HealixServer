import time


def  stream(file_path) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            processFile(line)
            time.sleep(1)

def processFile(data):
    print(f"Processing data: {data.strip()}")

def main():
    file_path = 'sample_data.txt'
    stream(file_path)


if __name__ == "__main__":
    main()