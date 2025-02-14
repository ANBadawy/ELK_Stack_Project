import json

def validate_bulk_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i % 2 == 1:
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Error on line {i+1}: {e}")
                    return
    print("Bulk file is valid.")

validate_bulk_file("flattened.json")


# def count_documents_in_bulk(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         doc_count = sum(1 for i in range(len(lines)) if i % 2 == 1)  # Count only data lines
#         print(f"Total documents in bulk file: {doc_count}")

# count_documents_in_bulk("flattened.json")
