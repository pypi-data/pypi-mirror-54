# py_package_template (Python 3.7+)
######Author: [Joe Tilsed](http://linkedin.com/in/joetilsed) | Created: 28.10.2019 | Last Updated: 28.10.2019

### Requirements:
- setuptools
- wheel
- twine

### Helpful Articles:
- [Packaging Python Projects — Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/)

### File Structure:
- [package_name](./package_name)
- [LICENSE](./LICENSE)
- [README.md](./README.md)

### Generating the distribution:
*python setup.py sdist bdist_wheel*

### Uploading the distributions to PyPi:
- TEST
    - *python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/**
- PROD
    - *python -m twine upload dist/**
