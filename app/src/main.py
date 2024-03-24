from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import gtfs_static
import json


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World2"}


@app.get("/api/{stop_id}/{dest_stop_id}")
def next_bus(
    stop_id: str, dest_stop_id: str, response_size: int = 5, opt: bool = False
):
    return gtfs_static.next_bus_times(stop_id, dest_stop_id, response_size, opt)
