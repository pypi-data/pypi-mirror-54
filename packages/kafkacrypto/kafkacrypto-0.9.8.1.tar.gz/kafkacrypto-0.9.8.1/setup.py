import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="kafkacrypto",
  version="0.9.8.1",
  license="GNU GPLv2",
  keywords="kafka kafka-crypto kafka-security security crypo",
  author="Tyrel M. McQueen",
  author_email="tmcqueen-pypi@demoivre.com",
  description="Message layer security/crypto for Kafka",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/tmcqueen-materials/kafkacrypto",
  packages=setuptools.find_packages(),
  install_requires=['pysodium','msgpack','kafka-python'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent",
  ],
)
