#!/bin/bash

LIBDIR="/usr/lib/tf"

# checks
[[ $EUID -ne 0 ]] && { echo "Run this as root." >&2; exit 1; }

[[ -e tf.py ]] || { echo "Could not find tf.py. Are you running install.sh from the extracted source directory?"; exit 1; }

if [[ -e "$LIBDIR" ]]; then
    read -rp "$LIBDIR exists. Would you like to overwrite it? (Y/n) " response

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
fi

# install
pushd . &> /dev/null
install -vDm755 tf.py -t "$LIBDIR"

if python3 -c "import psutil" &>/dev/null; then
    sed -i "1s|^#!.*|#!/usr/bin/python3|" "$LIBDIR"/tf.py
else
    python3 -m venv "$LIBDIR"/venv
    "$LIBDIR"/venv/bin/pip install psutil
    sed -i "1s|^#!.*|#!$LIBDIR/venv/bin/python|" "$LIBDIR"/tf.py
fi

ln -sfv "$LIBDIR"/tf.py /usr/bin/tf

popd &> /dev/null || exit 1
echo "tf has installed to $LIBDIR and symlinked to /usr/bin/tf"
