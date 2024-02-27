from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import gtfs_static
import json


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World2"}


@app.get("/api/{stop_name}")
def next_bus(stop_name: str):
    df_test = gtfs_static.today_bus_times(stop_name=stop_name)
    return Response(df_test.iloc[1].to_json(), media_type="application/json")
