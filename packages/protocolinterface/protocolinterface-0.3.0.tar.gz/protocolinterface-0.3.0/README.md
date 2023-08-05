# protocolinterface

## Releasing

First, test the code:

```
python -m pytest tests/test_protocolinterface.py
```

If it passes the tests, it can be released with:

```
git tag 0.X.Y # tag the version of the release
make
git push --tags
```

builds and uploads the package

## Installing:


```
conda install protocolinterface -c acellera
```
