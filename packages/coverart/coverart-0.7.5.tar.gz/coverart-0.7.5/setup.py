#!/usr/bin/env python

from setuptools import setup

setup(

    name='coverart',
    version='0.7.5',

    description='Cover art downloader.',

    author='Jeremy Cantrell',
    author_email='jmcantrell@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Sound/Audio',
    ],

    install_requires=[
        'gtkutils',
        'imageutils',
        'scriptutils',
    ],

    entry_points={
        'gui_scripts': [
            'coverart=coverart.gui:main',
        ]
    },

    packages=[
        'coverart',
    ],

    package_data={
        'coverart': [
            'icons/*.svg',
            'sources/*.py',
            'ui/*.ui',
        ]
    },

)
