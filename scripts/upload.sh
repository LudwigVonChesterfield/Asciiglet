#!/bin/sh
cd ..
echo "You are about to upload to PyPi."

function upload
{
	twine upload dist/*
	read -p "$*"
}

while true; do
    read -p "Do you wish to install this program? " yn
    case $yn in
        [Yy]* ) upload; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

cd scripts
