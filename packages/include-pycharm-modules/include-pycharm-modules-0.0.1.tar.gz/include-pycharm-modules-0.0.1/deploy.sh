#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "You need to provide the target like: testpypi|pypi"
fi

sed -i 's/(.\/images\//(https:\/\/raw.githubusercontent.com\/KIC\/include-pycharm-modules\/master\/images\//' README.md
flit --repository $1 publish
git checkout README.md
