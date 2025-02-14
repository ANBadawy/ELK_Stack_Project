import json
from collections import defaultdict

with open('_annotations_output.json', 'r') as f:
    lines = f.readlines()

data = []
for i in range(1, len(lines), 2):
    data.append(json.loads(lines[i].strip())) 

grouped_data = defaultdict(lambda: {"annotations": [], "width": None, "height": None, "date": "2024-01-01", "year": 2024, "month": 1, "day": 1})

for doc in data:
    filename = doc["filename"]
    if grouped_data[filename]["width"] is None:
        grouped_data[filename]["width"] = int(doc["width"])
        grouped_data[filename]["height"] = int(doc["height"])

    annotation = {
        "class": doc["class"],
        "xmin": int(doc["xmin"]),
        "ymin": int(doc["ymin"]),
        "xmax": int(doc["xmax"]),
        "ymax": int(doc["ymax"]),
    }
    grouped_data[filename]["annotations"].append(annotation)

bulk_data = []
for filename, doc in grouped_data.items():
    bulk_data.append({"index": {"_index": "annotate_pics_grouped"}})
    bulk_data.append({
        "filename": filename,
        "width": doc["width"],
        "height": doc["height"],
        "annotations": doc["annotations"],
        "date": doc["date"],
        "year": doc["year"], 
        "month": doc["month"],
        "day": doc["day"]      
    })

with open('bulk_grouped_data_es.json', 'w') as f:
    for entry in bulk_data:
        f.write(json.dumps(entry) + '\n')

print("Transformation completed. Data saved to bulk_grouped_data.json.")








# import json
# from collections import defaultdict

# # Load the bulk data
# with open('_annotations_output.json', 'r') as f:
#     lines = f.readlines()

# # Parse the bulk data
# data = []
# for i in range(1, len(lines), 2):  # Skip metadata lines (every other line)
#     data.append(json.loads(lines[i].strip()))  # Parse the actual document lines

# # Group annotations by filename
# grouped_data = defaultdict(lambda: {"annotations": [], "width": None, "height": None})

# for doc in data:
#     filename = doc["filename"]
#     # Initialize width and height for the group (assuming all documents for the same filename have the same dimensions)
#     if grouped_data[filename]["width"] is None:
#         grouped_data[filename]["width"] = doc["width"]
#         grouped_data[filename]["height"] = doc["height"]

#     # Add the annotation
#     annotation = {
#         "class": doc["class"],
#         "xmin": int(doc["xmin"]),
#         "ymin": int(doc["ymin"]),
#         "xmax": int(doc["xmax"]),
#         "ymax": int(doc["ymax"]),
#     }
#     grouped_data[filename]["annotations"].append(annotation)

# # Prepare the bulk upload format for Elasticsearch
# bulk_data = []
# for filename, doc in grouped_data.items():
#     bulk_data.append({"index": {"_index": "annotate_pics_grouped"}})
#     bulk_data.append({
#         "filename": filename,
#         "width": doc["width"],
#         "height": doc["height"],
#         "annotations": doc["annotations"]
#     })

# # Save the transformed data to a new file
# with open('bulk_grouped_data.json', 'w') as f:
#     for entry in bulk_data:
#         f.write(json.dumps(entry) + '\n')

# print("Transformation completed. Data saved to bulk_grouped_data.json.")



