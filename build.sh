#!/usr/bin/bash

poetry build
cd ..
pip install --force-reinstall ./IP-Reveal/dist/ip_reveal-1.2-py3-none-any.whl
cd -
