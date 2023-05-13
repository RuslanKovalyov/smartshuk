#before using, import MEDIA_ROOT in file where you include this lib.
from typing import Union, Tuple
from django.core.files.images import ImageFile
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageOps, ExifTags
import os

def max_size(image: ImageFieldFile, max_size: Union[Tuple[int, int], int]) -> ImageFieldFile:
    """
    Resize the image to the given maximum size while maintaining the aspect ratio.

    :param image: The ImageFieldFile object containing the image to resize.
    :param max_size: A tuple (width, height) specifying the maximum dimensions of the resized image
                     or a single integer to be used as the max size for both dimensions.
    :return: ImageFieldFile object of the resized image.
    """
    img = Image.open(image.path)

    if isinstance(max_size, int):
        max_size = (max_size, max_size)

    img.thumbnail(max_size)
    img.save(image.path)

    return image

def fix_orientation(image: ImageFieldFile) -> ImageFieldFile:
    """
    Fix the orientation of the image based on its EXIF data.

    :param image: The ImageFieldFile object containing the image to fix the orientation of.
    :return: ImageFieldFile object of the fixed image.
    """
    img = Image.open(image.path)
    img = ImageOps.exif_transpose(img)
    img.save(image.path)

    return image

def create_thumbnail(image: ImageFieldFile, max_size: Union[Tuple[int, int], int], thumbnail_prefix: str = "thumbnail_") -> ImageFieldFile:
    """
    Create a thumbnail of the given image.

    :param image: The ImageFieldFile object containing the image to create a thumbnail of.
    :param max_size: A tuple (width, height) specifying the maximum dimensions of the thumbnail
                     or a single integer to be used as the max size for both dimensions.
    :param thumbnail_prefix: A string to prepend to the filename of the thumbnail image.
                             Default is "thumbnail_".
    :return: ImageFieldFile object of the created thumbnail.
    """

    img = Image.open(image.path)

    if isinstance(max_size, int):
        max_size = (max_size, max_size)

    img.thumbnail(max_size)

    thumbnail_filename = thumbnail_prefix + os.path.basename(image.path)
    thumbnail_path = os.path.join(os.path.dirname(image.path), thumbnail_filename)

    img.save(thumbnail_path)

    image.field.upload_to = os.path.dirname(image.path).split(MEDIA_ROOT)[-1]
    thumbnail_image = ImageFieldFile(instance=image.instance, field=image.field, name=os.path.join(image.field.upload_to, thumbnail_filename))

    return thumbnail_image
