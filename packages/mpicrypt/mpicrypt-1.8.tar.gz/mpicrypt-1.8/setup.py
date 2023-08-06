#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except:
    from distutils.core import setup, Extension

MODULES = [
    Extension(
        "_mpicrypt",
        ["_mpicrypt.c","mpi.c","AES.c","sha1.c","md5.c","py_aescounter.c","py_keyobj.c","py_sha.c"],
        include_dirs=[],
        library_dirs=[],
        libraries=[],
        )]

# build!
setup(
    name="mpicrypt",
    version="1.8",
    author="Jeff Senn",
    author_email= "jeffsenn@gmail.com",
    description="Python _mpicrypt helper",
    packages=[""],
    ext_modules = MODULES,
    )
