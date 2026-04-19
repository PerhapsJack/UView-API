import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store seeded with mock data for two devices
_next_id = 1
_readings = []

def _seed():
    global _next_id
    now = datetime.now()
    mock = [
        # badge-01 — 5 readings
        {"device_id": "badge-01", "uva": 2.10, "uvb": 0.85, "uvc": 0.02, "temperature": 26.1},
        {"device_id": "badge-01", "uva": 2.45, "uvb": 0.91, "uvc": 0.03, "temperature": 26.4},
        {"device_id": "badge-01", "uva": 1.98, "uvb": 0.78, "uvc": 0.01, "temperature": 25.9},
        {"device_id": "badge-01", "uva": 3.02, "uvb": 1.10, "uvc": 0.04, "temperature": 27.2},
        {"device_id": "badge-01", "uva": 2.67, "uvb": 0.99, "uvc": 0.03, "temperature": 26.8},
        # badge-02 — 5 readings
        {"device_id": "badge-02", "uva": 1.55, "uvb": 0.60, "uvc": 0.01, "temperature": 24.3},
        {"device_id": "badge-02", "uva": 1.80, "uvb": 0.72, "uvc": 0.02, "temperature": 24.7},
        {"device_id": "badge-02", "uva": 2.20, "uvb": 0.88, "uvc": 0.02, "temperature": 25.5},
        {"device_id": "badge-02", "uva": 1.40, "uvb": 0.55, "uvc": 0.01, "temperature": 23.9},
        {"device_id": "badge-02", "uva": 1.95, "uvb": 0.76, "uvc": 0.02, "temperature": 24.9},
    ]
    for i, row in enumerate(mock):
        _readings.append({
            "id": _next_id,
            "timestamp": (now - timedelta(minutes=len(mock) - i)).isoformat(timespec="seconds"),
            **row,
        })
        _next_id += 1

_seed()


class Reading(BaseModel):
    device_id: str
    uva: float
    uvb: float
    uvc: float
    temperature: float


@app.post("/data")
def post_reading(reading: Reading):
    global _next_id
    _readings.append({
        "id": _next_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        **reading.model_dump(),
    })
    _next_id += 1
    return {"status": "ok"}


@app.get("/data")
def get_readings(device_id: str = None, limit: int = 100):
    rows = _readings if device_id is None else [r for r in _readings if r["device_id"] == device_id]
    return list(reversed(rows))[:limit]


if __name__ == "__main__":
    print("Running dummy API (no database) at http://localhost:8000")
    print("Seeded with 5 readings each for badge-01 and badge-02")
    uvicorn.run(app, host="0.0.0.0", port=8000)
