import os

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from app.route import user, session

origins = ["*"]

app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/etc/secrets/application_default_credentials.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(session.router)

@app.get("/")
async def root():
    return {"message": "Backend Client for the project"}



# @app.websocket("/text")
# async def text_webscoket_endpoint(websocket: WebSocket):

#     task = websocket.accept

#     chat_model = ChatWithModel()

#     await task()

#     while True:
#         data = await websocket.receive_text()
#         if(data == 'exit' or data == 'Exit'):
#             await websocket.close()
#             break
#         response = chat_model.Phykologist(message=data)
        
#         await websocket.send_text(response)


# class session(BaseModel):
#     name: str

# def changeTotalTime(timestamp, user):
#     with open(user+".txt", "r") as f:
#         lines = f.readlines()
#         timeTaken = ((timestamp))-float(lines[7])
#         lines[4] = str(float(lines[4]) +timestamp) + "\n"
#     with open(user+".txt", "w") as f:
#         f.writelines(lines)
#     return timeTaken


# @app.post("/sessionover")
# async def session_values(username: session):
#     timestamp = datetime.datetime.now().timestamp()
#     timeTaken = changeTotalTime(timestamp, username.name)
#     with open(username.name+".txt", "r") as f:
#         lines = [line.strip() for line in f.readlines()]
#         return {
#             "tag": 0,
#             "timeTaken": str(timeTaken),
#             "totalTime": lines[4]
#         }

# @app.post("/startsession")
# async def session_values(username: session):
#     numberOfSessions = 0
#     sessionTime = datetime.datetime.now()
#     startSession = sessionTime.timestamp()
#     tag = 0
#     pyq = ""
#     with open(username.name+".txt", "r") as f:
#         lines = f.readlines()
#         print(lines)
#         numberOfSessions = int(lines[1]) + 1
#         tag = int(lines[2])
#         pyq = lines[3]
#     with open(username.name+".txt", "w") as f:
#         f.write(username.name + "\n")
#         f.write(str(numberOfSessions) + "\n")
#         f.write(str(tag) + "\n")
#         f.write(pyq + "\n")
#         f.write("0" + "\n")
#         f.write(str(sessionTime) + "\n")
#         f.write(str(startSession) + "\n")

#     return {
#         "message": "Session Started",
#     }


