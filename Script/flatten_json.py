import json

def flatten_annotations(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    flattened_data = []

    for i in range(0, len(lines), 2):
        try:
            index_line = lines[i].strip()
            document_line = lines[i + 1].strip()

            index_entry = json.loads(index_line)
            document_entry = json.loads(document_line)

            filename = document_entry.get("filename")
            width = document_entry.get("width")
            height = document_entry.get("height")
            date = document_entry.get("date")
            year = document_entry.get("year")
            month = document_entry.get("month")
            day = document_entry.get("day")

            annotations = document_entry.get("annotations", [])
            for annotation in annotations:
                flattened_entry = {
                    "filename": filename,
                    "width": width,
                    "height": height,
                    "class": annotation.get("class"),
                    "xmin": annotation.get("xmin"),
                    "ymin": annotation.get("ymin"),
                    "xmax": annotation.get("xmax"),
                    "ymax": annotation.get("ymax"),
                    "date": date,
                    "year": year,
                    "month": month,
                    "day": day
                }

                flattened_data.append(index_entry)
                flattened_data.append(flattened_entry)

        except json.JSONDecodeError as e:
            print(f"Error processing lines {i}-{i+1}: {e}")
            print(f"Index Line: {index_line}")
            print(f"Document Line: {document_line}")
            break
        except IndexError:
            print(f"Uneven lines in input file: Could not process lines {i} and {i+1}")
            break

    with open(output_file, 'w') as outfile:
        for entry in flattened_data:
            json.dump(entry, outfile)
            outfile.write('\n')


input_file = "bulk_grouped_data_es.json"   
output_file = "flattened.json" 

flatten_annotations(input_file, output_file)
