# World-map options

**Status:** Proposed

The simulator will eventually need a map for aircraft routes, vertiports, charging sites, airports, weather or no-fly overlays, and possibly terrain. A map library is only the rendering layer; we must also choose a basemap/data provider and keep operational calculations separate from the visual map.

## Recommendation

Start with **MapLibre GL JS** for the primary map and add **Turf.js** for client-side geometry calculations. MapLibre is open source, WebGL-based, supports vector tiles, globe projection, terrain, GeoJSON, clustering, and animated lines. That gives us a polished world view without committing the simulator to one commercial map vendor.

Use **deck.gl** later if the simulator needs dense operational overlays such as thousands of flight legs, aircraft positions, heatmaps, demand cells, or animated traffic. It works with MapLibre and is designed for high-performance data visualization rather than basic basemap display.

Use **CesiumJS** only for a dedicated 3D mission or terrain view. It is the strongest option when accurate WGS84 globe positioning, terrain, 3D buildings, 3D Tiles, time-dynamic playback, or realistic flight visualization is central to the experience, but it adds more complexity than the current charging workspace needs.

## Visual snapshots

These previews are linked to the projects' official examples or product pages. They are intended to make the trade-offs quickly legible; the preview service is external, so we should replace these with checked-in screenshots if this document becomes part of a published product brief.

### MapLibre GL JS — best default

[![MapLibre GL JS globe example](https://image.thum.io/get/width/1200/crop/800/https://maplibre.org/maplibre-gl-js/docs/examples/display-a-globe-with-a-vector-map/)](https://maplibre.org/maplibre-gl-js/docs/examples/display-a-globe-with-a-vector-map/)

**Pros:** polished vector styling, GPU rendering, globe/terrain support, and a vendor-neutral open-source core.

**Cons:** requires a separate basemap/style/tile decision; some advanced 3D workflows need plugins or additional tooling.

### deck.gl — best for dense operational data

[![deck.gl HexagonLayer example](https://image.thum.io/get/width/1200/crop/800/https://deck.gl/gallery/hexagon-layer)](https://deck.gl/gallery/hexagon-layer)

**Pros:** excellent for large datasets, animated routes, heatmaps, traffic, demand cells, and interactive picking.

**Cons:** it is not the basemap; it adds bundle/runtime complexity and should be introduced only when ordinary map layers stop being enough.

### CesiumJS — best for a true 3D globe

[![CesiumJS photorealistic globe](https://images.prismic.io/cesium/56015908-7b08-4858-8a95-e04e2b10b6bf_Google_Tiles_Globe.png?auto=compress%2Cformat&w=1320)](https://cesium.com/platform/cesiumjs)

**Pros:** high-precision WGS84 globe, terrain, 3D Tiles, models, imagery, and time-dynamic flight playback.

**Cons:** heaviest option here; more specialized camera/data concepts, and premium global content may involve Cesium ion or another paid provider.

### Leaflet — best for a lightweight 2D prototype

[![Leaflet interactive map example](https://image.thum.io/get/width/1200/crop/800/https://leafletjs.com/)](https://leafletjs.com/)

**Pros:** small, approachable, mobile-friendly, and very fast to prototype with markers, popups, GeoJSON, and simple route lines.

**Cons:** primarily a 2D renderer; globe, terrain, and very large animated overlays are less natural than in MapLibre or Cesium.

### OpenLayers — best for GIS and standards-heavy data

[![OpenLayers vector layers example](https://openlayers.org/theme/img/vector-layers.png)](https://openlayers.org/)

**Pros:** broad projection support and strong coverage of GeoJSON, vector tiles, WMS/WMTS, and other OGC/GIS formats.

**Cons:** broad API surface and steeper learning curve for a product that initially needs a focused operational map.

## Shortlist

| Option | Best fit for CHARGE | Strengths | Trade-offs |
| --- | --- | --- | --- |
| [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) | **Default world/route map** | Open source; GPU-accelerated vector rendering; globe, terrain, GeoJSON, clustering, custom styles, and 3D layers | We must select and operate a compatible tile/style provider; more setup than Leaflet |
| [deck.gl](https://deck.gl/docs/) + MapLibre | High-volume operational overlays | Excellent for large point/line/polygon datasets, heatmaps, animated routes, and data-driven layers | It is an overlay/visualization framework, not a complete basemap solution by itself |
| [CesiumJS](https://cesium.com/platform/cesiumjs) | **Optional 3D globe/terrain mode** | High-precision WGS84 globe; terrain, imagery, 3D Tiles, models, and time-dynamic visualization | Larger bundle and steeper learning curve; Cesium ion may add service/account costs |
| [Leaflet](https://leafletjs.com/) | Fast prototype or simple regional map | Small, familiar, mobile-friendly API; easy markers, popups, GeoJSON, and raster tiles | Primarily a 2D map; less suitable for a stylized globe, terrain, or very large animated datasets |
| [OpenLayers](https://openlayers.org/) | GIS-heavy or standards-heavy workflow | Strong support for projections, GeoJSON, vector tiles, WMS/WMTS, and other OGC services | Broader GIS API and more concepts than the first simulator release needs |

## Supporting libraries and data

- **[Turf.js](https://turfjs.org/):** distance, bearing, buffers, bounding boxes, interpolation, and GeoJSON helpers. Use it for display calculations and lightweight analysis; keep authoritative flight/energy calculations in the simulator domain model.
- **Basemap styles and tiles:** evaluate a hosted vector-tile provider or self-hosted/open data before implementation. MapLibre is not itself a map-data or tile-hosting service.
- **OpenStreetMap:** useful for global context and place data, but the public OSM tile servers are best-effort and have usage, caching, attribution, and no-bulk-download requirements. Do not treat `tile.openstreetmap.org` as a production CDN.
- **Natural Earth:** a good lightweight source for country and coastline outlines when we only need a low-zoom world backdrop and want to avoid loading detailed street data.
- **Aircraft/airport data:** keep airports, vertiports, charging stations, routes, and restricted areas in our own versioned GeoJSON/domain data with source date and provenance. Do not infer operational suitability from a generic basemap.

## Suggested rollout

1. **Prototype:** MapLibre GL JS with a low-detail vector style, a small GeoJSON fixture for airports/vertiports, and Turf.js for route distance and bearing.
2. **Operational map:** add route legs, charging-site status, selectable aircraft, range rings, and a clear legend. Keep route feasibility and energy results owned by the simulator model.
3. **Scale-up:** add deck.gl only when the number of overlays or animated objects makes ordinary MapLibre layers difficult to maintain.
4. **3D milestone:** introduce a separate CesiumJS view if terrain, obstacle clearance, realistic approach paths, or time-based flight playback becomes a confirmed requirement.

## Decision criteria

Before choosing a tile provider, record:

- license and attribution requirements;
- API-key, rate-limit, SLA, and cost model;
- vector versus raster availability;
- globe, terrain, satellite, and offline/self-hosting support;
- data freshness and geographic coverage;
- performance on a typical laptop and mobile device;
- whether the provider permits caching and production use.

### Initial decision

**Proposed stack:** MapLibre GL JS + a replaceable vector-tile provider + Turf.js, with deck.gl and CesiumJS as optional extensions. This keeps the first implementation lightweight while preserving a path to high-volume operational visualization and a high-fidelity 3D globe.

