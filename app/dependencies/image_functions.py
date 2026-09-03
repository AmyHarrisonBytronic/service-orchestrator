from base64 import b64decode
from cv2 import IMREAD_UNCHANGED, imdecode
from numpy import frombuffer, uint8

class ImageFunctions:

    def extract_image(encoded_image):
        '''extracts the image from the encoded array into a ndarray
        Arga:
            encoded_image: a string containing the image packet encoded as base64
        Returns:
            image: an ndarray containing valid image data
        '''
        if isinstance(encoded_image, str) and "," in encoded_image:
            encoded_image = encoded_image.split(",", 1)[1]
    
        image_bytes = b64decode(encoded_image)
        depth_image = imdecode(frombuffer(image_bytes, dtype=uint8), IMREAD_UNCHANGED)
        if depth_image is None:
            raise ValueError("The image payload could not be decoded by OpenCV.")
        return depth_image