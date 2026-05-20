#import necessary libraries
import json
import os

#define each eventtype in a dictionary
DISASTER_TYPES = {
    "EQ": "earthquake.geojson",
    "TC": "cyclone.geojson",
    "FL": "flood.geojson",
    "WF": "wildfire.geojson",
    "DR": "drought.geojson",
    "TS": "tsunami.geojson",
    "VO": "volcano.geojson"
}

#do not filter based on geometry as yet
GEOMETRY_FILTER = None

#this is just a conditional check, in case output folder does not exist, create it.
os.makedirs("output", exist_ok=True)

#this part is used to load the original geojson into python
with open("data/gdacs.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

#using for loop to handle each eventtype sequentially
#define filter_type and output file variables firsthand
for FILTER_TYPE, OUTPUT_FILE in DISASTER_TYPES.items():
    #create an empty list of features initially
    filtered_features = []
    #loop through earthquake feature, drought feature, cyclone feature, etc one by one.
    for feature in data["features"]:
        
        #reading of geometry happens below
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        
        #reading of eventtype happens below
        eventtype = properties.get("eventtype")
        geometry_type = geometry.get("type")

        #Filtering based on eventtype (flood, earthquake, cyclone) happens here
        if eventtype != FILTER_TYPE:
            continue

        #Optional Filtering based on geometry type (lineString, polygon, point) can happen here if required.
        #Right now all geometry types are taken
        if GEOMETRY_FILTER is not None:
            if geometry_type != GEOMETRY_FILTER:
                continue
        #below append function adds entire feature object to the original list
        filtered_features.append(feature)

    #now the result of above for loop needs to be stored somewhere, so create below geojson
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": filtered_features
    }

    #Save output in this path in the directory
    output_path = f"output/{OUTPUT_FILE}"

    #actual process of saving happens here using dump function
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_geojson, f)
        
#So your script preserved ALL geospatial components correctly.
    #Below summary results just to display in console
    print(f"Created: {OUTPUT_FILE}")
    print(f"Features: {len(filtered_features)}")
    print("-------------------------")

print("All disaster files created successfully.")
