#!/usr/bin/env python3
"""
Setup script for YUV NV12 Image Converter
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='yuv-nv12-converter',
    version='1.0.0',
    description='Convert images to/from YUV420 NV12 format',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/yuv-nv12-converter',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[
        'Pillow>=10.0.0',
        'numpy>=1.24.0',
    ],
    entry_points={
        'console_scripts': [
            'yuv-convert=yuv_nv12.cli.convert:main',
            'yuv-read=yuv_nv12.cli.read:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='yuv nv12 image converter video',
)
