# UView API

REST API server for the UView UV badge system. Receives readings from docking stations and serves them to the web interface.

---

## Setup

### Prerequisites

**Python must be installed** before proceeding. Download it from [python.org](https://www.python.org/downloads/) and ensure it is added to your PATH during installation.

### Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the server

### Dummy mode (web interface development)

`run_dummy.py` runs the API with an **in-memory store** seeded with mock data for two devices (`badge-01` and `badge-02`). No database or docking station is required. Use this mode when developing or testing the web interface. Both `GET /data` and `POST /data` are fully functional — posted readings are stored in memory and will appear in subsequent GET requests.

```bash
python run_dummy.py
```

### Production mode (docking station + database)

`run.py` connects to a MySQL database and is intended for **actual deployment** with a physical docking station. A running MySQL instance is required with a `uv_badge` database and an `API` user.

```bash
python run.py
```

The server starts on `http://0.0.0.0:8000` in both modes.

---

## Test page

Open `test.html` in a browser while the server is running. It displays a table of all current readings from the dummy data and also accepts POST requests to submit new readings, which is useful for quickly verifying the API is working before building out the full web interface.

---

## API Endpoints

### `POST /data`

Submit a UV reading from a badge device.

**Request body (JSON):**

| Field | Type | Description |
|---|---|---|
| `device_id` | string | Unique identifier for the badge |
| `uva` | float | UVA reading |
| `uvb` | float | UVB reading |
| `uvc` | float | UVC reading |
| `temperature` | float | Temperature reading |

**Example:**
```json
{
  "device_id": "badge-01",
  "uva": 2.45,
  "uvb": 0.91,
  "uvc": 0.03,
  "temperature": 26.4
}
```

**Response:**
```json
{ "status": "ok" }
```

**Full example:**
```bash
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{"device_id":"badge-01","uva":2.45,"uvb":0.91,"uvc":0.03,"temperature":26.4}'
```

---

### `GET /data`

Retrieve stored readings, ordered by most recent first.

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `device_id` | string | *(all devices)* | Filter readings by device |

**Example:**
```
GET /data?device_id=badge-01
```

**Response:** Array of reading objects including `id` and `timestamp`.

```json
[
  {
    "id": 5,
    "timestamp": "2026-04-19T14:32:00",
    "device_id": "badge-01",
    "uva": 2.67,
    "uvb": 0.99,
    "uvc": 0.03,
    "temperature": 26.8
  },
  {
    "id": 4,
    "timestamp": "2026-04-19T14:31:00",
    "device_id": "badge-01",
    "uva": 3.02,
    "uvb": 1.10,
    "uvc": 0.04,
    "temperature": 27.2
  }
]
```
