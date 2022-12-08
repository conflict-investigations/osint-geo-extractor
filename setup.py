from pathlib import Path
from setuptools import setup, find_packages

parent = Path(__file__).parent
long_description = (parent / "README.md").read_text()

setup(
    name='osint-geo-extractor',
    author='conflict-investigations',
    version='0.0.8',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/conflict-investigations/osint-geo-extractor',
    license='MIT',
    description='Geo-related info extraction library for Bellingcat, Cen4InfoRes etc',  # noqa
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    install_requires=None,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)
