# coding=utf-8

from hashlib import md5
import shutil
import os

from django.test import TestCase
import Image

import imaging
import encode

path = lambda *args: os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)


class EncodeTest(TestCase):
    def testSimpleEncoding(self):
        self.assertEqual(encode.baseEncode(100, 10), '100')

    def testIncorrectBase(self):
        pass


class ImagePathFixTest(TestCase):
    def test_fix_image_path(self):
        example = lambda *args: (''.join((args[0], '.', args[1])), args[0], args[1])

        filename, name, extension = example('тестирование', 'JPEG')
        self.assertEqual(example(md5(name).hexdigest(), 'jpg')[0], imaging.fix_image_path(filename))
        filename = '098f6bcd4621d373cade4e832627b4f6.jpg'
        self.assertEqual(filename, imaging.fix_image_path(filename))

        filename, name, extension = example('098f6bcd46татататататаатататb4f6', 'GIF')
        self.assertEqual(example(md5(name).hexdigest(), 'gif')[0], imaging.fix_image_path(filename))


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


