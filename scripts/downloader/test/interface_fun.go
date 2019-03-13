package main

/*
#cgo pkg-config: python3
#define Py_LIMITED_API
#include <Python.h>


C.PyObject* docker_download(PyObject *, PyObject *);

//int PyArg_ParseTuple_String(PyObject * args, const char** a, const char** b, char** c, char** d) {
//	return PyArg_ParseTuple(args, "ssss", a, b, c, d);
//}
//
//PyObject* Py_String(char *pystring){
//	return Py_BuildValue("s", pystring);
//}

static PyMethodDef downloadMethods[] = {
    {"docker_download", docker_download, METH_VARARGS, "downloading manifests or blobs."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef downloadmodule = {
   PyModuleDef_HEAD_INIT, "download", NULL, -1, DownloadMethods
};

PyMODINIT_FUNC
PyInit_download(void)
{
    return PyModule_Create(&downloadmodule);
}
*/
import "C"

func main() {}