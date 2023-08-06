
#include "sha1.h"
typedef struct {
  PyObject_HEAD
  int hashsize;
  char sha_ctx[SHA_CTX_SIZE];
} sha1object;
static PyTypeObject SHA1ObjectType;

static PyObject *
py_sha1obj_new(PyObject* self, unsigned char* a, int al, int hashsize)
{
  sha1object *bo;
  bo = PyObject_New(sha1object, &SHA1ObjectType);
  if(bo) {
    bo->hashsize = hashsize;
    sha_op((hashsize == 32 ? '2' : (hashsize == 16 ? '5': '1')),(SHA_CTX) &(bo->sha_ctx),a,al);
  }
  return (PyObject*) bo;
}

static void
sha1object_dealloc(keyobject *self)
{
  PyObject_Del(self);
}

static PyObject *
py_sha1_digest(PyObject *self) {
  sha1object *bo = (sha1object*) self;
  int siz = bo->hashsize;
  PyObject *sha = PyString_FromStringAndSize(0,siz);
  sha_op('F',(SHA_CTX) &(bo->sha_ctx),(unsigned char*)PyString_AS_STRING(sha), siz);
  return sha;
}

static PyObject *
py_sha1_update(PyObject *self, PyObject *args) {
  unsigned char *k;
  int kl;
  sha1object *bo = (sha1object*) self;
  if (!PyArg_ParseTuple(args, "s#:sha1_update",&k,&kl)) return NULL;
  sha_op('U',(SHA_CTX)  &(bo->sha_ctx),k,kl);
  Py_INCREF(self);
  return self;
}

static PyMethodDef sha1obj_methods[] = {
	{"update",     (PyCFunction)py_sha1_update, METH_VARARGS},
	{"digest",     (PyCFunction)py_sha1_digest, METH_NOARGS},
	{NULL,	       	NULL}		/* sentinel */
};

static PyObject *
sha1object_getattr(PyObject *dp, char *name)
{
  return Py_FindMethod(sha1obj_methods, dp, name);
}

static PyTypeObject SHA1ObjectType = {
	PyObject_HEAD_INIT(NULL)
	0,
	"_mpicrypt.sha",
	sizeof(sha1object),
	0,
	(destructor)sha1object_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)sha1object_getattr, /*tp_getattr*/
	0,			/*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,	/*tp_as_mapping*/
};

static PyObject *
py_sha1(PyObject *self, PyObject *args) {
    sha1object *ret = 0;
    unsigned char *a = 0;
    int al=0;
    if (!PyArg_ParseTuple(args, "|s#:sha1",&a,&al)) return NULL;
    ret = (sha1object*) py_sha1obj_new(self,a,al,20);
    return (PyObject*) ret;
}

static PyObject *
py_sha256(PyObject *self, PyObject *args) {
    sha1object *ret = 0;
    unsigned char *a = 0;
    int al=0;
    if (!PyArg_ParseTuple(args, "|s#:sha256",&a,&al)) return NULL;
    ret = (sha1object*) py_sha1obj_new(self,a,al,32);
    return (PyObject*) ret;
}

static PyObject *
py_md5(PyObject *self, PyObject *args) {
    sha1object *ret = 0;
    unsigned char *a = 0;
    int al=0;
    if (!PyArg_ParseTuple(args, "|s#:md5",&a,&al)) return NULL;
    ret = (sha1object*) py_sha1obj_new(self,a,al,16);
    return (PyObject*) ret;
}

typedef struct {
  PyObject_HEAD
  int hashsize;
  char sha_ctxi[SHA_CTX_SIZE];
  char sha_ctxo[SHA_CTX_SIZE];
} hmacobject;
static PyTypeObject HMACObjectType;

static PyObject *
py_hmacobj_new(PyObject* self, int hashsize, unsigned char* k, int kl, 
	       unsigned char* a, int al) 
{
  int i;
  hmacobject *bo;
  char keyblock[64];
  bo = PyObject_New(hmacobject, &HMACObjectType);
  if(bo) {
    bo->hashsize = hashsize;
    sha_op((hashsize == 32 ? '2' : (hashsize == 16 ? '5': '1')),(SHA_CTX) &(bo->sha_ctxi),0,0);
    sha_op((hashsize == 32 ? '2' : (hashsize == 16 ? '5': '1')),(SHA_CTX) &(bo->sha_ctxo),0,0);
    //add in KEY
    bzero(keyblock,64);
    memcpy(keyblock,k,kl);
    for(i=0;i<64;i++) keyblock[i] ^= 0x5C; //XOR key
    sha_op('U',(SHA_CTX)  &(bo->sha_ctxo),(unsigned char*) keyblock,64); //update outer hash
    for(i=0;i<64;i++) keyblock[i] ^= (0x5C ^ 0x36); //re-XOR key
    sha_op('U',(SHA_CTX)  &(bo->sha_ctxi),(unsigned char*)  keyblock,64); //update inner hash
    //update content
    if(a && al) {
      sha_op('U',(SHA_CTX)  &(bo->sha_ctxi),a,al); //update inner hash
    }
  }
  return (PyObject*) bo;
}

static void
hmacobject_dealloc(keyobject *self)
{
  PyObject_Del(self);
}

static PyObject *
py_hmac_digest(PyObject *self) {
  hmacobject *bo = (hmacobject*) self;
  int siz = bo->hashsize;
  PyObject *hmac = PyString_FromStringAndSize(0,siz);
  //copy outer ctx
  char sha_ctx[SHA_CTX_SIZE];
  memcpy(sha_ctx,&(bo->sha_ctxo),SHA_CTX_SIZE);
  //get inner digest, update outer copy, and digest
  sha_op('F',(SHA_CTX) &(bo->sha_ctxi),(unsigned char*)PyString_AS_STRING(hmac), siz);
  sha_op('U',(SHA_CTX) sha_ctx,(unsigned char*)PyString_AS_STRING(hmac), siz);
  sha_op('F',(SHA_CTX) sha_ctx,(unsigned char*)PyString_AS_STRING(hmac), siz);  
  return hmac;
}

static PyObject *
py_hmac_update(PyObject *self, PyObject *args) {
  unsigned char *a;
  int al, i;
  hmacobject *bo = (hmacobject*) self;
  if (!PyArg_ParseTuple(args, "s#:hmac_update",&a,&al)) return NULL;
  if(a && al) {
    sha_op('U',(SHA_CTX)  &(bo->sha_ctxi),a,al); //update inner hash
  }
  Py_INCREF(self);
  return self;
}

static PyMethodDef hmacobj_methods[] = {
	{"update",     (PyCFunction)py_hmac_update, METH_VARARGS},
	{"digest",     (PyCFunction)py_hmac_digest, METH_NOARGS},
	{NULL,	       	NULL}		/* sentinel */
};

static PyObject *
hmacobject_getattr(PyObject *dp, char *name)
{
  return Py_FindMethod(hmacobj_methods, dp, name);
}

static PyTypeObject HMACObjectType = {
	PyObject_HEAD_INIT(NULL)
	0,
	"_mpicrypt.HMAC",
	sizeof(hmacobject),
	0,
	(destructor)hmacobject_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)hmacobject_getattr, /*tp_getattr*/
	0,			/*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,	/*tp_as_mapping*/
};

static PyObject *
py_HMAC(PyObject *self, PyObject *args) {
    hmacobject *ret = 0;
    unsigned char *a = 0, *k;
    int al=0, keysize, kl;
    if (!PyArg_ParseTuple(args, "is#|s#:HMAC",&keysize,&k,&kl,&a,&al)) return NULL;
    ret = (hmacobject*) py_hmacobj_new(self,keysize,k,kl,a,al);
    return (PyObject*) ret;
}
