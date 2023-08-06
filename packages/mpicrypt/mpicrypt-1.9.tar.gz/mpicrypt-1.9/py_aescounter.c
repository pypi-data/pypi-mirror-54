#include "AES.h"

typedef struct {
  PyObject_HEAD
  unsigned char counter[16];
  int keylen;
  unsigned char key[32];
} aescounterobject;

static PyObject *
py_aescounter_encrypt(PyObject *self, PyObject *args) {
  PyObject *ret = 0;
  int kl;
  aescounterobject *bo = (aescounterobject*) self;
  if (!PyArg_ParseTuple(args, "i:encrypt",&kl)) return NULL;
  if(bo->keylen) ret  = PyString_FromStringAndSize(0,kl);
  if(ret) {
    int s = AES_crypt(bo->key,bo->keylen,2,(char*)bo->counter,16,PyString_AS_STRING(ret),kl);
    if(s < 0) {
      Py_DECREF(ret); ret = 0;
    }
  } 
  return ret;
}
static PyObject *
py_aescounter_setkey(PyObject *self, PyObject *args) {
  char *k;
  int kl;
  aescounterobject *bo = (aescounterobject*) self;
  if (!PyArg_ParseTuple(args, "s#:set_key",&k,&kl)) return NULL;
  if (kl != 16 && kl != 24 && kl != 32) return NULL;
  bo->keylen = kl;
  memcpy(bo->key,k,kl);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
py_aescounter_incr(PyObject *self) {
  int j;
  aescounterobject *bo = (aescounterobject*) self;
  unsigned char *in = &bo->counter[0];
  for(j=0; j < 16 && (++in[j]) == 0; j++); 
  if(j == 16) in[0]++; /*increment counter*/
  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef aescounter_methods[] = {
	{"encrypt",     (PyCFunction)py_aescounter_encrypt, METH_VARARGS},
	{"set_key",     (PyCFunction)py_aescounter_setkey, METH_VARARGS},
	{"incr",        (PyCFunction)py_aescounter_incr, METH_NOARGS},
	{NULL,	       	NULL}		/* sentinel */
};

static PyObject *
aescounter_getattr(PyObject *dp, char *name)
{
  return Py_FindMethod(aescounter_methods, dp, name);
}

static void
aescounter_dealloc(aescounterobject *self)
{
  PyObject_Del(self);
}

static PyTypeObject AESCounterObjectType = {
	PyObject_HEAD_INIT(NULL)
	0,
	"_mpicrypt.AESCounter",
	sizeof(aescounterobject),
	0,
	(destructor)aescounter_dealloc,   /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)aescounter_getattr, /*tp_getattr*/
	0,			/*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,	/*tp_as_mapping*/
};

static PyObject *
py_aes_counter(PyObject* self) {
  aescounterobject *bo;
  bo = PyObject_New(aescounterobject, &AESCounterObjectType);
  if(bo) {
    int j;
    for(j=0; j<16; j++) { bo->counter[j] = 0; }
    bo->keylen = 0;
  }
  return (PyObject*) bo;
}

static PyObject *
py_aes_encrypt(PyObject *self, PyObject *args) {
  char *k, *buf, *iv;
  int kl,buflen,ivlen,dir,s,extra=0;
  PyObject *ret = 0;
  iv = 0; ivlen = 0;
  if (!PyArg_ParseTuple(args, "s#is#|s#:aes_encrypt",&k,&kl,&dir,&buf,&buflen,&iv,&ivlen,&iv,&ivlen)) return NULL;
  if(dir & 1) { /*encrypt needs more bytes*/ 
    extra = 16-(buflen%16); 
    if(extra==0) { extra = 16; }
    dir &= ~2; /*make sure is not counter mode; WHY!!!!!????*/
  } else if((buflen % 16) != 0) return NULL;
  ret  = PyString_FromStringAndSize(0,buflen + extra);
  if(iv && ivlen) {
    if(ivlen > buflen+extra) ivlen = buflen+extra;
    memcpy(PyString_AS_STRING(ret), iv, ivlen);
  }
  s = AES_crypt((unsigned char*) k,kl,dir,buf,buflen,PyString_AS_STRING(ret),buflen + extra);
  if(s < 0) {
    Py_DECREF(ret); ret = 0;
  } else if(s < buflen+extra) {
    /*would like to use string resize here*/
    PyObject *ret2 = PyString_FromStringAndSize(PyString_AS_STRING(ret),s);
    Py_DECREF(ret); ret = ret2;
  }
  return ret;
}

