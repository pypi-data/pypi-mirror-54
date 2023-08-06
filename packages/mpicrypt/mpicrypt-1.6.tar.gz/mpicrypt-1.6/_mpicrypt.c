#include <Python.h>
#include <stdlib.h>

#ifdef _WIN32
#  pragma comment(lib, "advapi32.lib")
#endif

/*avoid the DLL spec import stuff on windows - we just want locally compiled symbols*/
#define JSALLOC_IMPORT
#include "jsalloc.h"

void* js_alloc(int op, void* p, size_t sz, int align) {
  void *ret = 0;
  int zero = 0;
  switch(op) {
  case JSALLOC_FREE:
    free(p);
    break;
  case JSALLOC_NEW: 
  case JSALLOC_NEWARRAY:
  case JSALLOC_ALLOCZ: zero = 1;
  case JSALLOC_ALLOC:
    if(!p) {
      ret = malloc(sz);
      if(ret && zero) memset(ret,0,sz);
    } else {
      ret = realloc(p,sz);
      /*zeroing doesn't work on base platform*/
    }
    break;
  case JSALLOC_STRCOPY:
    if(p) { 
      size_t s = strlen((char*) p);
      ret = malloc(s+1);
      if(ret) memcpy(ret,p,s+1);
    }
    break;
  default:;
  }
  return ret;
}

#include "py_keyobj.c"
#include "py_sha.c"
#include "py_aescounter.c"

#include <fcntl.h>
#include <sys/stat.h>
#ifdef _WIN32
  static HCRYPTPROV hProv = 0;
#else
  static int urandom_fp = -1;
#endif

static PyObject* py_urandom(PyObject *self, PyObject *args) {
  int l;
  if (!PyArg_ParseTuple(args, "i:urandom",&l)) return NULL;
  if(urandom_fp != -1) {
    PyObject *ret = PyString_FromStringAndSize(0,l);
    if(ret) {
#     ifdef _WIN32
      if(!CryptGenRandom(hProv,l,PyString_AS_STRING(ret)) {
	  Py_DECREF(ret); ret = 0;
#     else
        if(read(urandom_fp, PyString_AS_STRING(ret), l) != l) {
	  Py_DECREF(ret); ret = 0;
        }
#     endif
      return ret;
    }
  }
  return 0;
}

#ifndef WITHOUT_RANDOM
# define URANDOM_STOMP 6
#else
# define URANDOM_STOMP 5
#endif

static PyMethodDef module_methods[] = {
	{"key_import",	(PyCFunction)py_key_import, METH_VARARGS},
#ifndef WITHOUT_RANDOM
	{"key_generate",(PyCFunction)py_key_generate, METH_VARARGS},
#endif
	{"aes_encrypt",(PyCFunction)py_aes_encrypt, METH_VARARGS},
	{"aes_counter",(PyCFunction)py_aes_counter, METH_NOARGS},

	{"sha1",(PyCFunction)py_sha1, METH_VARARGS},
	{"sha256",(PyCFunction)py_sha256, METH_VARARGS},
	{"md5",(PyCFunction)py_md5, METH_VARARGS},
	{"HMAC",(PyCFunction)py_HMAC, METH_VARARGS},
	{"urandom",(PyCFunction)py_urandom, METH_VARARGS},
	{0,		0},
};


PyMODINIT_FUNC
init_mpicrypt(void)
{
  PyObject *module;
  /* Create the module and add the functions */
  KeyObjectType.ob_type = &PyType_Type;
  SHA1ObjectType.ob_type = &PyType_Type;
  AESCounterObjectType.ob_type = &PyType_Type;
#ifdef _WIN32
  /*TODO: test Windows version of urandom....based on CryptGenRandom*/
  if(!::CryptAcquireContextW(&hProv, 0, 0, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT | CRYPT_SILENT)) {
    module_methods[URANDOM_STOMP].ml_name = 0;
    module_methods[URANDOM_STOMP].ml_meth = 0;
  }
#else
  {
    struct stat s;
    urandom_fp = open("/dev/urandom",O_RDONLY);
    if(urandom_fp != -1) {
      if(fstat(urandom_fp,&s) || (s.st_mode & S_IFCHR) == 0) {
	close(urandom_fp); urandom_fp = -1;
      }
    }
  }
  if(urandom_fp == -1) {
    module_methods[URANDOM_STOMP].ml_name = 0;
    module_methods[URANDOM_STOMP].ml_meth = 0;
  }
#endif
  module = Py_InitModule("_mpicrypt", module_methods);
}
