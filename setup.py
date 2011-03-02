from setuptools import setup


setup(
        name = 'extractframes',
        version = '0.10',
        author = 'Thomas Grenfell Smith',
        author_email = 'thomathom@gmail.com',
        description = 'A script to extract frames from a video file using ffmpeg',
        license = 'BSD',
        keywords = 'ffmpeg video frames extract',
        packages = ['extractframes'],
        scripts = ['extract.py'],

        requires = ['progressbar'],

        test_suite = 'nose.collector',
        tests_require = ['Nose', 'progressbar'],
        setup_requires = ['Nose'],
        )
