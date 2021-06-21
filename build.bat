python setup.py sdist bdist_wheel
twine check dist/*
rmdir -r dist /s /q
rmdir -r build /s /q
rmdir -r asciiglet.egg-info /s /q
pause
