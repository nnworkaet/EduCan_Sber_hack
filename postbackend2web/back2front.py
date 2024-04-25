from fastapi import BackgroundTasks, FastAPI
from maker import req_trans,req_termins,req_test,req_sum
from pydantic import BaseModel

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)



class TranscriptionRequest(BaseModel):
    identity: str
    audioPath: str

@app.post("/requestTranscription")
async def request_transcription(request: TranscriptionRequest, background_tasks: BackgroundTasks):
    print(request.audioPath)
    background_tasks.add_task(req_trans, request.identity, request.audioPath)
    return {"response": "success"}

class TerminationRequest(BaseModel):
    identity: str
    txt: str

@app.post("/requestTermins")
async def request_termins(request: TerminationRequest, background_tasks: BackgroundTasks):
    text = eval(request.txt)

    print(text)
    print("==============")
    print(text[0])

    background_tasks.add_task(req_termins, request.identity, text)
    return {"response": "success"}

class TestRequest(BaseModel):
    identity: str
    txt: str

@app.post("/requestTest")
async def request_test(request: TestRequest, background_tasks: BackgroundTasks):
    text=[''.join(inner_list) for inner_list in eval(''.join(request.txt))]
    print(text)
    print("==============")
    print(text[0])
    background_tasks.add_task(req_test, request.identity,eval(''.join(request.txt)) )
    return {"response": "success"}





class SumRequest(BaseModel):
    identity: str
    txt: str

@app.post("/requestSum")
async def request_sum(request: SumRequest, background_tasks: BackgroundTasks):

    text = [''.join(inner_list) for inner_list in eval(''.join(request.txt))]
    print(text)
    print("==============")
    print(text[0])
    background_tasks.add_task(req_sum, request.identity, eval(''.join(request.txt)))
    return {"response": "success"}
