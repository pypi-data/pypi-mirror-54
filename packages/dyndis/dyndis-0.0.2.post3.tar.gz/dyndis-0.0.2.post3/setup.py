import setuptools

import dyndis.__data__ as dyndis

setuptools.setup(
    name=dyndis.__name__,
    version=dyndis.__version__,
    url=dyndis.__url__,
    author=dyndis.__author__,
    packages=['dyndis'],
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('', ['README.md', 'CHANGELOG.md']),
    ],
    install_requires=["sortedcontainers"],
    extras_require={
        "testing": ['numpy']
    }
)
