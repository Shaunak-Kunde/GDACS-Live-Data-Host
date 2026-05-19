import json
import os

# ==============================
# DISASTER TYPE MAPPING
# ==============================

DISASTER_TYPES = {
    "EQ": "earthquake.geojson",
    "TC": "cyclone.geojson",
    "FL": "flood.geojson",
    "WF": "wildfire.geojson",
    "DR": "drought.geojson",
    "TS": "tsunami.geojson",
    "VO": "volcano.geojson"
}

# Optional:
# None = keep all geometry types

GEOMETRY_FILTER = None

# ==============================
# CREATE OUTPUT FOLDER
# ==============================

os.makedirs("output", exist_ok=True)

# ==============================
# LOAD MASTER GDACS FILE
# ==============================

with open("data/gdacs.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

# ==============================
# PROCESS EACH DISASTER TYPE
# ==============================

for FILTER_TYPE, OUTPUT_FILE in DISASTER_TYPES.items():

    filtered_features = []

    for feature in data["features"]:

        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        eventtype = properties.get("eventtype")
        geometry_type = geometry.get("type")

        # Filter disaster type
        if eventtype != FILTER_TYPE:
            continue

        # Optional geometry filtering
        if GEOMETRY_FILTER is not None:
            if geometry_type != GEOMETRY_FILTER:
                continue

        filtered_features.append(feature)

    # Create GeoJSON
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": filtered_features
    }

    # Save output
    output_path = f"output/{OUTPUT_FILE}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_geojson, f)

    # Summary
    print(f"Created: {OUTPUT_FILE}")
    print(f"Features: {len(filtered_features)}")
    print("-------------------------")

print("All disaster files created successfully.")