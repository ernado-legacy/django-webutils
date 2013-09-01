# coding=utf-8
import os
import hashlib
import shutil


from django.db.models import ImageField
from django.core.files.images import ImageFile
from django.conf import settings
from PIL import Image


def get_parameters(image_path):
    """
    Parses the image path to dictionary
    :param str image_path: image path
    :rtype dict
    """
    image_directory = os.path.dirname(image_path)
    image_filename = os.path.basename(image_path)
    image_name = image_filename.split('.')[0]
    image_extension = image_filename.split('.')[-1]
    return {
        'directory': image_directory,
        'extension': image_extension,
        'name': image_name,
        'filename': image_filename,
        'path': image_path
    }


def fix_image_path(image_path):
    """
    Fixes the image path, transforming it to {md5hash}.{extension}

    :param str image_path: image path
    :rtype str
    """
    image = get_parameters(image_path)

    # early extension fix
    image['extension'] = image['extension'].lower().replace('jpeg', 'jpg')

    wrong_name = False
    try:                          # check ascii characters in filename
        image['name'].decode('ascii')
    except UnicodeEncodeError:
        wrong_name = True
    except UnicodeDecodeError:
        wrong_name = True

    if len(image['name']) != 32:  # check image name length
        wrong_name = True

    if wrong_name:
        image['name'] = hashlib.md5(image['name'].encode("utf-8")).hexdigest()

    return os.path.join(image['directory'], ''.join([image['name'], '.', image['extension']]))


def normalize_image_size(image_path, max_size):
    """
    Reduces image size to max_size
    :param image_path: path to image
    :param max_size: maximum size
    """
    try:
        image_object = Image.open(image_path)
    except IOError:
        raise IOError("No image found at %s" % image_path)
    image = get_parameters(image_path)
    if max(image_object.size) > max_size:
        resize_rate = max(image_object.size) / float(max_size)
        new_size = (int(image_object.size[0] / resize_rate), int(image_object.size[1] / resize_rate))
        image_object.thumbnail(new_size, Image.ANTIALIAS)
        new_path = os.path.join(image['directory'], ''.join([image['name'], '_thumbnail.jpg']))
        try:
            if image_object.mode != "RGB":
                image_object = image_object.convert("RGB")
            image_object.save(new_path, quality=70)
            shutil.copy(new_path, image['path'])
        except (IOError, KeyError, ValueError):
            try:
                os.remove(new_path)
            except IOError:
                pass
            raise


def save(image_field):
    image_path = image_field.path.encode("utf-8")

    try:
        image_exists = os.path.isfile(image_path)
    except (UnicodeEncodeError, UnicodeDecodeError):
        raise IOError('Incorrect locale settings')

    if not image_exists:
        return

    image_path = image_field.path
    new_image_path = fix_image_path(image_path)
    if new_image_path != image_path:
        image_content = ImageFile(open(image_path))
        try:
            image_field.save(os.path.basename(image_path), image_content, save=True)
        except IOError:
            pass    # TODO: process error
        image_path = new_image_path

    if not os.path.isfile(image_path):
        raise IOError('Failed to create %s' % image_path)
    try:
        normalize_image_size(image_path, settings.MAX_IMAGE_SIZE)
    except IOError:
        raise IOError('Failed to process %s' % image_path)


def upload_to(path):
    """
    Возвращает функцию генерации пути
    """

    def update_filename(instance, filename):
        f = fix_image_path(filename)
        return os.path.join(path, f)

    return update_filename


class ImageFieldHash(ImageField):
    def __init__(self, **kwargs):
        if 'upload_to' in kwargs:
            kwargs['upload_to'] = upload_to(kwargs['upload_to'])
        super(ImageFieldHash, self).__init__(**kwargs)


