# map2print
Simple python script for downloading map tiles of selected area and comleting them into big image. This image is cutted into A4 sheets for print.

## TODO:
- make web application frontend for easy selection of area
- create install.sh for easy installation (including systemd services in the future)
- import GPX and draw it as a line

## HOW TO INSTALL
- install imagemagick: `apt install imagemagick`
- enable PDF conversion in policy settings: 
  - set imversion variable to your imagemagick version, f.e.: `imversion=6` (you can get it from `convert -version`, only first number)
  - open file f.e. in Vim `vim /etc/ImageMagick-$imversion/policy.xml`
  - add `<policy domain="coder" rights="read | write" pattern="PDF" />` to the end of content in the main XML tag (`</policymap>`)
- cd into cloned directory
- make python virtual environment: `python3 -m venv venv`
- activate venv: `source venv/bin/activate`
- install dependencies into venv: `pip install -r requirements.txt`
- make script executable: `chmod +x bigmap.py`
- run: `./bigmap.py`
