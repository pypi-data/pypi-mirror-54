import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name="little-pwny",
        version="0.1",
        description="Check whether your password has been pwnd",
        long_description=read('README.rst') + '\n\n\n',
        long_description_content_type='text/x-rst',
        url="https://github.com/ulif/little-pwny",
        author="ulif",
        author_email="uli@gnufix.de",
        license="GPL3",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: System Administrators",
            "Topic :: Utilities",
            "Topic :: Security :: Cryptography",
            (
                "License :: OSI Approved :: "
                "GNU General Public License v3 or later (GPLv3+)"),
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
        packages=["pwny"],
        zip_safe=False,
        entry_points={
            'console_scripts': ['pwny = pwny:main']}
        )
