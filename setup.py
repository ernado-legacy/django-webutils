import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-webutils',
    version='0.4.1a',
    packages=['webutils', 'webutils.captcha', 'webutils.watermarker'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Combined common toolkit/api for cygame projects.',
    long_description=README,
    url='http://www.cygame.ru/',
    author='Ernado',
    author_email='ernado@ya.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
        'PIL>=1.1.7',
        'Django>=1.4'
    ],
)