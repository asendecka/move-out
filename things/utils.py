from PIL import Image
from django.core.files import File
import cStringIO


HEIGHT = 540
WIDTH = 405
QUALITY = 85
FORMAT = 'JPEG'


def resize_image(picture):
    if picture:
        image = Image.open(picture)
        image.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
        output = cStringIO.StringIO()
        image.save(output, format=FORMAT, quality=QUALITY)
        output.seek(0)
        picture = File(output, picture.name)
    return picture
