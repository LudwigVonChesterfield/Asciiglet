cd ..
rmdir -r dist /s /q
python setup.py sdist bdist_wheel
twine check dist/*
rmdir -r build /s /q
rmdir -r asciiglet.egg-info /s /q
cd scripts
