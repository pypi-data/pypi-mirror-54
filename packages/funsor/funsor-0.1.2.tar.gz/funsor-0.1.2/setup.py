import sys

from setuptools import find_packages, setup

# READ README.md for long description on PyPi.
# This requires uploading via twine, e.g.:
# $ python setup.py sdist bdist_wheel
# $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*  # test version
# $ twine upload dist/*
try:
    long_description = open('README.md', encoding='utf-8').read()
except Exception as e:
    sys.stderr.write(f'Failed to convert README.md to rst:\n  {e}\n')
    sys.stderr.flush()
    long_description = ''

# Remove badges since they will always be obsolete.
# This assumes the first 4 lines contain badge info.
long_description = '\n'.join(line for line in long_description.split('\n')[4:])

setup(
    name='funsor',
    version='0.1.2',
    description='A tensor-like library for functions and distributions',
    packages=find_packages(include=['funsor', 'funsor.*']),
    url='https://github.com/pyro-ppl/funsor',
    project_urls={
        "Documentation": "https://funsor.pyro.ai",
    },
    author='Uber AI Labs',
    author_email='fritzo@uber.com',
    python_requires=">=3.6",
    install_requires=[
        'multipledispatch',
        'numpy>=1.7',
        'opt_einsum>=2.3.2',
        'pyro-ppl>=0.5',
        'pytest>=4.1',
        'torch>=1.3.0',
    ],
    extras_require={
        'test': [
            'flake8',
            'pandas',
            'pyro-api>=0.1',
            'pytest-xdist==1.27.0',
            'torchvision==0.2.1',
        ],
        'dev': [
            'flake8',
            'isort',
            'pandas',
            'pytest-xdist==1.27.0',
            'sphinx>=2.0',
            'sphinx_rtd_theme',
            'torchvision==0.2.1',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='probabilistic machine learning bayesian statistics pytorch',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.6',
    ],
)
