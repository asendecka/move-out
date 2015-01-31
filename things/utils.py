from PIL import Image
from django.core.files import File
import StringIO


def resize_image(picture):
    if picture:
        image = Image.open(StringIO.StringIO(picture.read()))
        image.thumbnail((540, 405), Image.ANTIALIAS)
        output = StringIO.StringIO()
        image.save(output, format='JPEG', quality=75)
        output.seek(0)
        picture = File(output, picture.name)
    return picture
