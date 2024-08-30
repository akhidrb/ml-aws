import glob
import pytesseract
from PIL import Image
import boto3
import spacy
from spacy.training import Example

# csv_array = []
# client = boto3.client('textract')
# for filename in glob.glob('files/*.png'):
#     csv_row = {}
#     print(f"Processing: {filename}")
#     with open(filename, 'rb') as fd:
#         file_bytes = fd.read()
#
#     response = client.detect_document_text(
#         Document={'Bytes': file_bytes})
#
#     for item in response["Blocks"]:
#         if item["BlockType"] == "LINE":
#             print(item["Text"])


image = Image.open('files/cr-1.png')
text = pytesseract.image_to_string(image, lang='ara')

# output_file_path = 'extracted_text.txt'
#
# # Write the extracted text to the file
# with open(output_file_path, 'w', encoding='utf-8') as file:
#     file.write(text)
#
# print(f"Text has been written to {output_file_path}")

# comprehend = boto3.client('comprehend')
#
# # Call the Comprehend API to detect entities
# response = comprehend.detect_entities(
#     Text=text,
#     LanguageCode='ar'  # Use 'ar' for Arabic if needed
# )
#
# # Extract and print entities
# entities_data = ""
# for entity in response['Entities']:
#     if entity['Type'] == 'PERSON' and entity['Score'] > 0.8:
#         entities_data += f"{entity['Text']}\n"


# Load a spaCy model (e.g., an Arabic model)
from farasa.ner import FarasaNamedEntityRecognizer

# Initialize Farasa NER
farasa_ner = FarasaNamedEntityRecognizer(interactive=True)

# Example Arabic text

# Extract named entities
result = farasa_ner.recognize(text)
# print(result)
# for entity in result:
#     print(f"Entity: {entity}")
    # print(f"Entity: {entity['word']}, Type: {entity['tag']}")
lines = text.split("\n")
words_tags = ""
for line in lines:
    elements = line.split(" ")
    for element in elements:
        if "/" in element:
            print(element)
            word, tag = element.rsplit("/", 1)
            # print(f"{word} - {tag}")
            if "PERS" in tag:
                words_tags += word


output_file_path = 'entities.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(words_tags)
