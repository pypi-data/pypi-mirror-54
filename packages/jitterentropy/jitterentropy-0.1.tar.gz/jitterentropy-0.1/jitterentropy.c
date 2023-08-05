#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <jitterentropy.h>

static PyObject *JitterEntropyReqError;
static PyObject *JitterEntropySysError;

static PyObject *
jitterentropy_version(PyObject *self, PyObject *args)
{
	unsigned int jv = 0;
	jv = jent_version();
	return PyLong_FromDouble((double)jv);
}

static PyObject *
jitterentropy_getrandbytes(PyObject *self, PyObject *args)
{
	int nbytes = 0;
	int jvh;
	void *mrd;
	int br;
	char *randbuf = NULL;
	PyObject *res;

	if (!PyArg_ParseTuple(args, "i", &nbytes))
		return NULL;

	if (nbytes < 1) {
		PyErr_SetString(JitterEntropyReqError, "invalid request");
		return NULL;
	}

	randbuf = PyMem_RawMalloc(nbytes * sizeof(char));
	if (randbuf == NULL)
		return PyErr_NoMemory();
	jvh = jent_entropy_init();
	mrd = jent_entropy_collector_alloc(1, 0);
	br = jent_read_entropy(mrd, randbuf, nbytes);
	if (br < 0) {
		PyErr_SetString(JitterEntropySysError, "jitterentropy Error");
		return NULL;
	}
	jent_entropy_collector_free(mrd);
	res = PyBytes_FromStringAndSize(randbuf, nbytes);
	PyMem_RawFree(randbuf);
	return res;
}

static PyMethodDef JitterEntropyMethods[] = {
	{ "version", jitterentropy_version, METH_VARARGS,
	    "Return jitterentropy version" },
	{ "getrandbytes", jitterentropy_getrandbytes, METH_VARARGS,
	    "Return random bytes" },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef jitterentropymodule = { PyModuleDef_HEAD_INIT,
	"jitterentropy", NULL, -1, JitterEntropyMethods };

PyMODINIT_FUNC
PyInit_jitterentropy(void)
{
	PyObject *module = PyModule_Create(&jitterentropymodule);
	JitterEntropyReqError = PyErr_NewException(
	    "JitterEntropy.ReqError", PyExc_ValueError, NULL);
	PyModule_AddObject(module, "ReqError", JitterEntropyReqError);
	JitterEntropySysError = PyErr_NewException(
	    "JitterEntropy.SysError", PyExc_ValueError, NULL);
	PyModule_AddObject(module, "SysError", JitterEntropySysError);
	return module;
}
