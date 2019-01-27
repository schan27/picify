from google.cloud import vision
from google.cloud.vision import types


def parse_image(image, gcp_credentials, confidence_threshold=0.69):
    """Parse an image and return label and web entity data.

    Args:
        image (string): Raw binary image data.
        gcp_credentials (google.auth.credentials.Credentials):
            Credentials for Google Cloud Platform.
        confidence_threshold (float, optional): An optional confidence
            threshold (between 0 and 1) below which data will not be
            considered.

    Returns (dict):
        The labels, web entities, and summary title (technically the
        "best_guess_labels") parsed from Google Cloud Vision API.
    """
    # Instantiate a client
    client = vision.ImageAnnotatorClient(credentials=gcp_credentials)

    # Instantiate an image
    image = types.Image(content=image)

    # Get response data for the image
    label_response = client.label_detection(image=image)
    web_response = client.web_detection(image=image)

    # Grab the confidence-threshold filtered labels, web entities, and
    # summary title
    labels = []
    web_entities = []

    for annotated_label in label_response.label_annotations:
        if annotated_label.score >= confidence_threshold:
            labels += [annotated_label.description.lower()]

    for web_entity in web_response.web_detection.web_entities:
        if web_entity.score >= confidence_threshold:
            web_entities += [web_entity.description.lower()]

    return {
        "labels": labels,
        "web_entities": web_entities,
        "title": web_response.web_detection.best_guess_labels[0].label,
    }
