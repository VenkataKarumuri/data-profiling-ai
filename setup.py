# setup.py

from setuptools import setup, find_packages

setup(
    name='data-profiling-ai',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'pandas',
        'scikit-learn',
        'openai',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'data-profiling-ai = scripts.validate_data:main',
        ],
    },
)
