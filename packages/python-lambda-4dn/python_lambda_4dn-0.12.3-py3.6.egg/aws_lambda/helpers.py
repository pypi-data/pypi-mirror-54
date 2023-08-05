# -*- coding: utf-8 -*-
import os
import zipfile
import datetime as dt


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def read(path, loader=None, binary_file=False):
    open_mode = 'rb' if binary_file else 'r'
    with open(path, mode=open_mode) as fh:
        if not loader:
            return fh.read()
        return loader(fh.read())


def archive(src, dest, filename):
    output = os.path.join(dest, filename)
    zfh = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)

    for root, _, files in os.walk(src):
        for file in files:
            print('ROOT --> %s\nFILE --> %s\n' % (root, file))
            zfh.write(os.path.join(root, file))
    zfh.close()
    return os.path.join(dest, filename)


def timestamp(fmt='%Y-%m-%d-%H%M%S'):
    now = dt.datetime.utcnow()
    return now.strftime(fmt)
