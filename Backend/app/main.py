
from fastapi import FastAPI, HTTPException
import networkx as nx

app = FastAPI(title="MetroGraph API")

# Temporary sample network.
# Edge weights are illustrative travel times in minutes.
metro = nx.Graph()

connections = [
    ("Rajiv Chowk", "New Delhi", 3),
    ("New Delhi", "Chawri Bazar", 4),
    ("Chawri Bazar", "Kashmere Gate", 5),
    ("Rajiv Chowk", "Patel Chowk", 2),
    ("Patel Chowk", "Central Secretariat", 4),
    ("Central Secretariat", "Kashmere Gate", 8),
]

for station_a, station_b, minutes in connections:
    metro.add_edge(
        station_a,
        station_b,
        time=minutes
    )


@app.get("/")
def home():
    return {
        "message": "Welcome to MetroGraph!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/stations")
def get_stations():
    return {"stations": sorted(metro.nodes())}


@app.get("/route")
def get_route(source: str, destination: str):
    if source not in metro:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown source station: {source}"
        )

    if destination not in metro:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown destination station: {destination}"
        )

    path = nx.shortest_path(
        metro,
        source=source,
        target=destination,
        weight="time"
    )

    total_minutes = nx.shortest_path_length(
        metro,
        source=source,
        target=destination,
        weight="time"
    )

    return {
        "source": source,
        "destination": destination,
        "stations": path,
        "station_count": len(path),
        "intermediate_stops": max(0, len(path) - 2),
        "estimated_time_minutes": total_minutes,
        "note": "Illustrative sample data, not actual DMRC timings."
    }
