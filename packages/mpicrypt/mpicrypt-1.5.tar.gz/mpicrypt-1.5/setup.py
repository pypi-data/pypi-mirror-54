#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except:
    from distutils.core import setup, Extension

MODULES = [
    Extension(
        "_mpicrypt",
        ["_mpicrypt.c","mpi.c","AES.c","sha1.c","md5.c","py_aescounter.c","py_keyobj.c","py_sha.c"],
        extra_objects=["jsalloc.h","AES.h","bn_asm.h","md5.h","platform.h","starimpl.h","sha1.h"],
        include_dirs=[],
        library_dirs=[],
        libraries=[],
        )]

# build!
setup(
    name="mpicrypt",
    version="1.5",
    author="Jeff Senn",
    author_email= "jeffsenn@gmail.com",
    description="Python _mpicrypt helper",
    packages=[""],
    ext_modules = MODULES,
    )
