# coding=utf-8

import shutil
import os

from django.test import TestCase
from PIL import Image

import imaging
import encode
from watermarker.utils import watermark

path = lambda *args: os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)


def errorOccurred(err, f, *args):
    try:
        f(*args)
        return False
    except err:
        return True


class EncodeTest(TestCase):
    def testSimpleEncoding(self):
        self.assertEqual(encode.baseEncode(100, 10), '100')
        self.assertEqual(encode.baseEncode('199', 10), '199')
        self.assertEqual(encode.baseEncode('', 10), '0')
        self.assertEqual(encode.baseEncode('1'), '1')

    def testExceptions(self):
        self.assertTrue(errorOccurred(TypeError, encode.baseEncode, None, 10))
        self.assertTrue(errorOccurred(ValueError, encode.baseEncode, -1, -1))
        self.assertTrue(errorOccurred(ValueError, encode.baseEncode, 0, -1))
        self.assertTrue(errorOccurred(ValueError, encode.baseEncode, 115, 2000))


class ImagePathFixTest(TestCase):
    def test_fix_image_path(self):
        SIZE = 22
        example = lambda *args: (''.join((args[0], '.', args[1])), args[0], args[1])

        filename, name, extension = example('тестирование', 'JPEG')
        #self.assertEqual(example(md5(name).hexdigest(), 'jpg')[0], imaging.fix_image_path(filename))
        # TODO: Implement smarter checks
        self.assertTrue(len(imaging.fix_image_path(filename).split('.')[0]) == SIZE)
        print imaging.fix_image_path(filename)

        filename, name, extension = example(u'тестирование', 'JPEG')
        self.assertTrue(len(imaging.fix_image_path(filename).split('.')[0]) == SIZE)
        #self.assertEqual(example(md5(name.encode('utf8')).hexdigest(), 'jpg')[0], imaging.fix_image_path(filename))
        print imaging.fix_image_path(filename)
        filename = '098f6bcd4621d373cade4e832627b4f6.jpg'
        #self.assertEqual(filename, imaging.fix_image_path(filename))
        self.assertTrue(len(imaging.fix_image_path(filename).split('.')[0]) == SIZE)
        print imaging.fix_image_path(filename)
        filename, name, extension = example('098f6bcd46татататататаатататb4f6', 'GIF')
        #self.assertEqual(example(md5(name).hexdigest(), 'gif')[0], imaging.fix_image_path(filename))
        filename = imaging.fix_image_path(filename)
        self.assertTrue(len(filename.split('.')[0]) == SIZE)
        self.assertEqual('gif', filename.split('.')[-1])
        print imaging.fix_image_path(filename)


class ImageSizeFixTest(TestCase):
    def setUp(self):
        self.images = [
            'test1.jpg',
            'test2.gif',
            'test3.png',
            'test4.bmp'
        ]
        self.new_images = []
        for i in self.images:
            _i_split = i.split('.')
            new_name = '%snew.%s' % (_i_split[0], _i_split[-1])
            shutil.copy(path('images/%s') % i, path('images/%s') % new_name)
            self.new_images.append(path('images/%s') % new_name)
        self.max_size = 500

    def test_fix_image_size(self):
        for image_path in self.new_images:
            imaging.normalize_image_size(image_path, self.max_size)
            image_object = Image.open(image_path)
            self.assertTrue(max(image_object.size) <= self.max_size,
                            "Image size of %s (%s) is not less than max (%s)" %
                            (image_path, max(image_object.size), self.max_size))

    def tearDown(self):
        for image_path in self.new_images:
            os.remove(image_path)


class WatermarkerTest(TestCase):
    def test_watermarker(self):
        im = Image.open(path('watermarker/test.png'))
        mark = Image.open(path('watermarker/overlay.png'))
        watermark(im, mark,
                  tile=True,
                  opacity=0.5,
                  rotation=30).save(path('images/test1.png'))

        watermark(im, mark,
                  scale='F').save(path('images/test2.png'))

        watermark(im, mark,
                  position=(100, 100),
                  opacity=0.5,
                  greyscale=True,
                  rotation=-45).save(path('images/test3.png'))

        watermark(im, mark,
                  position='C',
                  tile=False,
                  opacity=0.2,
                  scale=2,
                  rotation=30).save(path('images/test4.png'))

