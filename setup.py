import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="realtycloud",
    version="0.0.1",
    author="Realtycloud",
    author_email="help@realtycloud.ru",
    description="Thin Python wrapper over Realtycloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RealtyCloud-Company/realtycloud-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ],
    install_requires=['httpx'],
    python_requires='>3.7',
)