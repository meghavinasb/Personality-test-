# app.py
from flask import Flask, request, jsonify
import csv
import os  # Import the os module to check file existence
from personality_processor import process_personality_data

file = "Book1.csv"
output_file = 'output_quotes.csv'

app = Flask(__name__)

@app.route('/personalitytest', methods=["POST"])
def add_guide():
    data = request.json

    s_id = data.get('staff_id')
    s_name = data.get('staff_name')
    response_1 = data.get('response_1')
    response_2 = data.get('response_2')
    response_3 = data.get('response_3')
    response_4 = data.get('response_4','')
    response_5 = data.get('response_5','')

    # Validate that all required fields are present
    if not all([s_id, s_name, response_1, response_2, response_3]):
        return jsonify({"error": "All fields (staff_id, staff_name, response_1 to response_3) are required"}), 400

    # Check if the CSV file already exists
    file_exists = os.path.exists(file)

    # Open the CSV file in append mode with newline='' to ensure proper line endings
    with open(file, 'a', newline='', encoding='utf-8') as f_object:
        writer_object = csv.writer(f_object)

        # If the file doesn't exist, write the header first
        if not file_exists:
            writer_object.writerow(['staff_id', 'staff_name', 'response_1', 'response_2', 'response_3', 'response_4', 'response_5'])

        # Append the new row
        writer_object.writerow([s_id, s_name, response_1, response_2, response_3, response_4, response_5])

    # Process the personality data after adding the new row
    process_personality_data(file, output_file)

    return jsonify({
        "message": "Data added and processed successfully",
        "staff_id": s_id,
        "staff_name": s_name,
        "response_1": response_1,
        "response_2": response_2,
        "response_3": response_3,
        "response_4": response_4,
        "response_5": response_5
    }), 201 

@app.route('/get_staff_data/<staff_id>', methods=["GET"])
def get_staff_data(staff_id):
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['staff_id'] == staff_id:
                return jsonify(row), 200

    return jsonify({"error": "Staff ID not found"}), 404

if __name__ == '__main__':
    app.run(port='5001',debug=True)
