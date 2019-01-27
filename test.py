import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

# Instantiates a client
credentials = service_account.Credentials.from_service_account_file(
    "gcp_credentials.json"
)
client = vision.ImageAnnotatorClient(credentials=credentials)

# The name of the image file to annotate
file_name = os.path.join(os.path.dirname(__file__), "testimage.jpg")

# Loads the image into memory
with io.open(file_name, "rb") as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Look at the image
label_response = client.label_detection(image=image)
print(label_response)

web_response = client.web_detection(image=image)
print(web_response)
