#include "mpi.h"

#undef CHK
#define CHK(fc) if( ( fc ) != 0 ) goto cleanup
#ifdef _WIN32
#include <windows.h>
#endif

typedef struct {
  PyObject_HEAD
  mpi e,n,d,rr;
} keyobject;
static PyTypeObject KeyObjectType;

static void
keyobject_dealloc(keyobject *self)
{
  mpi_op('F',&self->n,&self->e,&self->d,&self->rr,(mpi*)0);
  PyObject_Del(self);
}

static PyObject *
py_keyobj_new(PyObject* self)
{
  keyobject *bo;
  bo = PyObject_New(keyobject, &KeyObjectType);
  if(bo) {
    mpi_op('A',&bo->n,&bo->e,&bo->d,&bo->rr,(mpi*)0);
  }
  return (PyObject*) bo;
}

static PyObject *
py_key_import(PyObject *self, PyObject *args) {
  unsigned char *a=0,*b=0,*c=0;
    keyobject *ret = 0;
    int al=0,bl=0,cl=0;
    int bad = 0;
    if (!PyArg_ParseTuple(args, "s#s#s#:key_import",&a,&al,&b,&bl,&c,&cl)) return NULL;
    ret = (keyobject*) py_keyobj_new(self);
    if(mpi_op('R',&ret->n,a,al)) bad = 1;
    if(mpi_op('R',&ret->e,b,bl)) bad = 1;
    if(c && mpi_op('R',&ret->d,c,cl)) bad = 1;
    if(bad) { keyobject_dealloc(ret); ret = 0; }
    return (PyObject*) ret;
}

static PyObject* mpi_to_str(mpi *n) {
  PyObject *ret = 0;
  int buflen = mpi_op('S',n);
  ret  = PyString_FromStringAndSize(0,buflen);
  if(ret) mpi_op('W',n,(unsigned char*) PyString_AS_STRING(ret),buflen);
  return ret;
}

static void my_random(void *rock, unsigned char* buf, int blen) {
  PyObject *ret, *pArgs = PyTuple_New(1);
  if(pArgs) {
    PyTuple_SetItem(pArgs, 0, PyInt_FromLong(blen));
    if ((ret = PyObject_CallObject((PyObject*) rock, pArgs)) != NULL) {
      if(PyString_Check(ret) && PyString_GET_SIZE(ret) == blen) {
	memcpy(buf,PyString_AS_STRING(ret), blen);
      }
      Py_DECREF(ret);
    }
    Py_DECREF(pArgs);
  }
}

static PyObject *
py_key_generate(PyObject *self,  PyObject *args) {
  PyObject *ret = 0, *rand;
    mpi p, q, g, phi,n,e,d;
    int bits,i;
    if (!PyArg_ParseTuple(args, "iO:key_generate",&bits,&rand)) return NULL;
    if (!PyCallable_Check(rand)) return NULL;
    mpi_op('A',&n,&e,&d,&p,&q,&phi,&g,(mpi*)0);
    bits = bits / 2;
    if(mpi_op('s',&e,65537)) return NULL;
    do {
      CHK(mpi_op('P',&p,bits,0,my_random,rand));
      CHK(mpi_op('P',&q,bits,0,my_random,rand));
      i = mpi_op('=',&p,&q);
      if(i == 0) continue; /*oops, the same*/
      if(i < 0) mpi_op('x',&p,&q); /*swap p/q*/
      CHK(mpi_op('*',&n,&p,&q)); /* n = p * q */
      CHK(mpi_op('m',&p,&p,1)); /* p -= 1 */
      CHK(mpi_op('m',&q,&q,1)); /* q -= 1 */
      CHK(mpi_op('*',&phi, &p, &q)); /* phi = p * q */
      CHK(mpi_op('G',&g, &e, &phi)); /* g = gcd(e,phi) */
    } while( mpi_op('i', &g, 1 ) != 0 ); /* g == 1 */
    CHK(mpi_op('H',&d, &e, &phi)); /* d = inv_mod(e, phi) */
    ret = PyTuple_New(3);
    PyTuple_SetItem(ret,0,mpi_to_str(&e));
    PyTuple_SetItem(ret,1,mpi_to_str(&n));
    PyTuple_SetItem(ret,2,mpi_to_str(&d));
 cleanup:
    mpi_op('F',&n, &e, &d, &p,&q,&phi,&g,(mpi*)0);
    return ret;
}

static PyObject *
py_keyobj_encrypt(keyobject* self,  PyObject *args) {
  int dir;
  unsigned char *buf;
  int buflen;
  PyObject *ret = 0;
  mpi v;
  if (!PyArg_ParseTuple(args, "is#:key_encrypt",&dir,&buf,&buflen)) return NULL;
  mpi_op('A',&v,(mpi*)0);
  if(dir == 0 /*decrypt*/ && mpi_op('i',&self->d,0)==0) return 0; /*no decrypt key*/
  if(mpi_op('R',&v, buf,buflen)) goto cleanup;
  if(mpi_op('=',&v, &self->n) >= 0) goto cleanup;
  CHK(mpi_op('E', &v, &v, ((dir == 0) ? (&self->d) : (&self->e)), &self->n, &self->rr));
  ret = mpi_to_str(&v);
 cleanup:
  mpi_op('F',&v,(mpi*)0);
  return ret;
}

static PyObject *
py_keyobj_check(keyobject* self,  PyObject *args) {
  unsigned char *buf;
  int buflen;
  PyObject *ret = 0;
  mpi v;
  if (!PyArg_ParseTuple(args, "s#:key_check",&buf,&buflen)) return NULL;
  if(mpi_op('R',&v, buf,buflen)) goto cleanup;
  ret = PyBool_FromLong(mpi_op('=',&v,&self->d) == 0);
 cleanup:
  mpi_op('F',&v,(mpi*)0);
  return ret;
}

static PyMethodDef keyobj_methods[] = {
	{"encrypt",     (PyCFunction)py_keyobj_encrypt, METH_VARARGS},
	{"check",     (PyCFunction)py_keyobj_check, METH_VARARGS},
	{NULL,	       	NULL}		/* sentinel */
};

static PyObject *
keyobject_getattr(PyObject *dp, char *name)
{
  return Py_FindMethod(keyobj_methods, dp, name);
}

static PyTypeObject KeyObjectType = {
	PyObject_HEAD_INIT(NULL)
	0,
	"_mpicrypt.key",
	sizeof(keyobject),
	0,
	(destructor)keyobject_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)keyobject_getattr, /*tp_getattr*/
	0,			/*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,	/*tp_as_mapping*/
};

