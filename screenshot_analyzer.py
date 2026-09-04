from PIL import Image, ImageOps, ImageEnhance
import pytesseract


# Tell pytesseract where Tesseract is installed on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image):
    """
    Extract readable text from a screenshot using OCR.
    """

    # Convert image to grayscale
    image = ImageOps.grayscale(image)

    # Make the text larger for OCR
    image = image.resize(
        (image.width * 2, image.height * 2)
    )

    # Increase contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # Extract text
    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text.strip()