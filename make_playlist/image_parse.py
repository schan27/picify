from google.cloud import vision
from google.cloud.vision import types


def parse_image(image, gcp_credentials):
    """Parse an image and return label and web entity data.

    Args:
        image (string): Raw binary image data.
        gcp_credentials (google.auth.credentials.Credentials):
            Credentials for Google Cloud Platform.

    Returns (dict):
        The label and web response from Google Cloud Vision API.
    """
    # Instantiate a client
    client = vision.ImageAnnotatorClient(credentials=gcp_credentials)

    # Instantiate an image
    image = types.Image(content=image)

    # Look at the image
    label_response = client.label_detection(image=image)
    web_response = client.web_detection(image=image)

    return {"label": label_response, "web": web_response}
