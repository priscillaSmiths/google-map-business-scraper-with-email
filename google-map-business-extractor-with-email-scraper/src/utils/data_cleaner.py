thonimport json

def clean_data(data):
    cleaned_data = []
    for item in data:
        if item.get('businessName') and item.get('address'):
            cleaned_data.append(item)
    return cleaned_data

def save_cleaned_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)