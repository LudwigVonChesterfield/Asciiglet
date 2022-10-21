#!/bin/sh
cd ..
rm -r dist /s /q
python setup.py sdist bdist_wheel
twine check dist/*
rm -r build /s /q
rm -r asciiglet.egg-info /s /q
cd scripts
