import json

def convert_to_ndjson(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        if not isinstance(data, list):
            raise ValueError("The input JSON must contain an array of objects.")

        with open(output_file, 'w') as outfile:
            for idx, item in enumerate(data, start=1):
                index_metadata = {
                    "index": {"_index": "annotate_pics", "_id": str(idx)}
                }
                outfile.write(json.dumps(index_metadata) + '\n')

                outfile.write(json.dumps(item) + '\n')

        print(f"Conversion complete! NDJSON saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

input_file = "_annotations.json"
output_file = "_annotations_output.json"  
# output_file = "_annotations_output_try.ndjson"

convert_to_ndjson(input_file, output_file)
