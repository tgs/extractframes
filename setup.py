from setuptools import setup
from version import __version__

setup(
        name = 'extractframes',
        version = __version__,
        author = 'Thomas Grenfell Smith',
        author_email = 'thomathom@gmail.com',
        description = 'A script to extract frames from a video file using ffmpeg',
        license = 'BSD',
        keywords = 'ffmpeg video frames extract',
        packages = ['extractframes'],
        scripts = ['extract.py', 'numcp.py'],

        install_requires = ['progressbar'],

        test_suite = 'nose.collector',
        tests_require = ['Nose', 'progressbar'],
        setup_requires = ['Nose'],
        )
