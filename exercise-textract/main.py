import glob
import boto3
import json
import csv
import sys

csv_array = []
client = boto3.client('textract')
for filename in glob.glob('raw_images/*.jpg'):
    csv_row = {}
    print(f"Processing: {filename}")
    with open(filename, 'rb') as fd:
        file_bytes = fd.read()

    response = client.analyze_document(
        Document={'Bytes': file_bytes},
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            'Queries': [
                {'Text': 'What is the response id', 'Alias': 'ResponseId'},
                {'Text': 'What are the notes?', 'Alias': 'Notes'},
            ]
        }
    )

    # uncomment this to see the format of the reponse
    # print(json.dumps(response, indent=2))
    i = 0
    response_id = ''
    notes = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'QUERY_RESULT' and i == 0:
            response_id = block['Text']
            i += 1
        if block['BlockType'] == 'QUERY_RESULT' and i == 1:
            notes = block['Text']
    #####
    # Replace this code with a solution to populate a dictionary with the results from textract
    #####
    csv_row["ResponseId"] = response_id
    csv_row["Notes"] = notes
    csv_array.append(csv_row)

writer = csv.DictWriter(sys.stdout, fieldnames=["ResponseId", "Notes"], dialect='excel')
writer.writeheader()
for row in csv_array:
    writer.writerow(row)

