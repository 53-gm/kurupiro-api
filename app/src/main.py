from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import gtfs_static
import json


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World2"}


@app.get("/api/{stop_id}/{dest_stop_id}")
def next_bus(stop_id: str, dest_stop_id: str, opt: bool = False):
    return gtfs_static.next_bus_time(stop_id, dest_stop_id, opt)
