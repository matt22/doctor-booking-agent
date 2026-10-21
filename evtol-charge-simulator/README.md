# CHARGE / EVTOL Energy Simulation

A lightweight browser-based simulator for eVTOL charging sessions, energy draw, session cost, and turnaround readiness.

## Run locally

Open `index.html` in a browser, or serve the folder with any static server:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Model

Energy required is calculated from battery capacity and the state-of-charge delta. Grid energy is adjusted by charger efficiency, charging time is derived from charger power, and session cost is derived from the energy tariff.

## Mapping direction

The proposed default for a future world/route map is MapLibre GL JS with Turf.js for GeoJSON and geospatial calculations. See [World-map options](docs/world-map-options.md) for the library shortlist, basemap considerations, and the proposed path to deck.gl or CesiumJS when the simulator needs denser overlays or a 3D globe.
