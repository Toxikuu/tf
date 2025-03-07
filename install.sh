#!/bin/bash

LIBDIR="/usr/lib/tf"

# checks
[[ $EUID -ne 0 ]] && { echo "Run this as root." >&2; exit 1; }

[[ -e tf.py ]] || { echo "Could not find tf.py. Are you running install.sh from the extracted source directory?"; exit 1; }

[[ -e "$LIBDIR" ]] && {
  read -p "$LIBDIR exists. Would you like to overwrite it? (y/n) " response

  case "$response" in
    [Nn]* ) 
        echo "Aborting!"
        exit 1
        ;;
    * ) 
        echo "Continuing with install..."
        rm -rvf "$LIBDIR"
        ;;
  esac
}

# install
pushd . > /dev/null
cd ..
cp -rvf tf "$LIBDIR"

python3 -m venv "$LIBDIR"/venv
"$LIBDIR"/venv/bin/pip install psutil
sed -i "1s|^#!.*|#!$LIBDIR/venv/bin/python|" "$LIBDIR"/tf.py

ln -sfv "$LIBDIR"/tf.py /usr/bin/tf

popd > /dev/null
echo "tf has installed to $LIBDIR and symlinked to /bin/tf"
