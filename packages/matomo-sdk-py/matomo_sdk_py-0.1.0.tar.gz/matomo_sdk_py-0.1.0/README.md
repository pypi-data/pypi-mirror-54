# matomo-sdk-py

[![PyPI version](https://badge.fury.io/py/matomo_sdk_py.svg)](https://badge.fury.io/py/matomo_sdk_py)

A simple wrapper of `requests` against matomo's API


## Installation

```
pip3 install matomo_sdk_py
```


## Usage

```
from matomo_sdk_py import ping_matomo
ping_matomo("/test", "https://example.com", 1, "abcdef", "https://example.matomo.cloud")
```

## Dev notes

New release

```
update version in matomo_sdk_py/__init__.py
update version in changelog
commit with 'version bump 0.1.0'
git tag 0.1.0
git push origin 0.1.0
```

To publish to pypi

```
pip3 install twine
rm build/* -rf
rm dist/* -rf
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Install locally for development

```
pip3 install -e .
pip3 install -r requirements_dev.txt
```

Run test

```
pytest
```


## Changelog

Check [CHANGELOG.md](CHANGELOG.md)


## License

Apache License 2.0. Check file [LICENSE](LICENSE)


## Author

`matomo_sdk_py` is brought to you by [AutofitCloud](https://www.autofitcloud.com),
seeking to cut cloud waste on our planet  🌎.


## Security contact information

<!-- inspired from https://github.com/pytest-dev/pytest-mock/#security-contact-information -->

To report a security vulnerability, please use the AutofitCloud [contact page](https://autofitcloud.com/contact).

We will coordinate the fix and disclosure.

