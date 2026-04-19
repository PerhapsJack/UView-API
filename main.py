from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from mysql.connector import pooling
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_pool = pooling.MySQLConnectionPool(
    pool_name="uview_pool",
    pool_size=5,
    host="localhost",
    user="API",
    password="API",
    database="uv_badge"
)
class Reading(BaseModel):
    device_id: str
    uva: float
    uvb: float
    uvc: float
    temperature: float

@app.post("/data")
def post_reading(reading: Reading):
    db = db_pool.get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO readings (device_id, uva, uvb, uvc, temperature) VALUES (%s, %s, %s, %s, %s)",
        (reading.device_id, reading.uva, reading.uvb, reading.uvc, reading.temperature)
    )
    db.commit()
    cursor.close()
    db.close()
    return {"status": "ok"}

@app.get("/data")
def get_readings(device_id: str = None, limit: int = 100):
    db = db_pool.get_connection()
    cursor = db.cursor(dictionary=True)
    if device_id:
        cursor.execute("SELECT * FROM readings WHERE device_id = %s ORDER BY timestamp DESC LIMIT %s", (device_id, limit))
    else:
        cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT %s", (limit,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results