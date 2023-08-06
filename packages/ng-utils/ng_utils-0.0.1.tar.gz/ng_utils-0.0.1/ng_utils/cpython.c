/*
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 */

#define PY_SSIZE_T_CLEAN

#include <errno.h>
#include <stdarg.h>
#include <string.h>
#include <stdbool.h>
#include <pthread.h>
#include <sys/stat.h>

#include "Python.h"
#include "structmember.h"


/* Inlining control for compatible compilers. */
#if (__GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4))
#   define NOINLINE __attribute__((noinline))
#else
#   define NOINLINE
#endif


/** Static data. */
static PyObject *py_u__class__;
static PyObject *py_u__loader;
static PyObject *py_u__variable_manager;
static PyObject *py_u__validated;
static PyObject *py_u__finalized;
static PyObject *py_u__uuid;
static PyObject *py_u__ds;
static PyObject *py_u__attributes;
static PyObject *py_u__attr_defaults;
static PyObject *py_u__alias_attrs;
static PyObject *py_u__valid_attrs;

static PyObject *py_u__copy;

static PyObject *py_copy__copy;
static PyObject *py_ansible__sentinel;
static PyObject *py_ansible__unicode;

static PyObject *py_LatchError;
static PyObject *py_TimeoutError;
static PyObject *py_deque;
static PyObject *py_deque__append;
static PyObject *py_deque__popleft;

static PyObject *py_u_ansible;
static PyObject *py_b_ansible;

static PyObject *py_unicode_startswith;
static PyObject *py_bytes_startswith;


/* ------------------------ */
/* Python 3.x Compatibility */
/* ------------------------ */

#if PY_MAJOR_VERSION >= 3

#   define MOD_RETURN(mod) return mod;
#   define MODINIT_NAME PyInit_cpython

#   define MAKE_ID(id) PyCapsule_New((void *) (1 + (id)), NULL, NULL)
#   define READ_ID(obj) (((int) (long) PyCapsule_GetPointer(obj, NULL)) - 1)

#else

#   define MOD_RETURN(mod) return
#   define MODINIT_NAME initcpython

#   define MAKE_ID(id) PyInt_FromLong((long) id)
#   define READ_ID(obj) PyInt_AS_LONG(obj)

#   define PyUnicode_InternFromString PyString_InternFromString
#   define PyBytes_AS_STRING PyString_AS_STRING
#   define PyBytes_GET_SIZE PyString_GET_SIZE
#   define PyBytes_CheckExact PyString_CheckExact
#   define PyBytes_FromStringAndSize PyString_FromStringAndSize
#   define _PyBytes_Resize _PyString_Resize
#   define PyMemoryView_FromMemory(x, y, z) PyBuffer_FromMemory(x, y)

#   ifndef PyBUF_READ
#       define PyBUF_READ 0
#   endif

/* Python 2.5 */
#   ifndef Py_TYPE
#       define Py_TYPE(ob) (((PyObject*)(ob))->ob_type)
#   endif

#   ifndef PyVarObject_HEAD_INIT
#       define PyVarObject_HEAD_INIT(x, y) \
            PyObject_HEAD_INIT(x) y,
#   endif

#endif


/*** Forward struct declarations. */
typedef struct LatchObject LatchObject;

/** lmdb.Transaction */
struct LatchObject {
    PyObject_HEAD
    PyObject *weaklist;
    PyObject *notify;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    PyObject *deque;
    Py_ssize_t size;
    int closed;
};


/*
 * mitogen.core.Latch
 */


/**
 * Latch() -> new instance.
 */
static PyObject *
latch_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    LatchObject *self;
    if(! ((self = PyObject_New(LatchObject, type)))) {
        return NULL;
    }

    self->weaklist = NULL;
    self->deque = NULL;
    self->notify = Py_None;
    Py_INCREF(Py_None);
    self->closed = 0;
    self->size = 0;
    pthread_mutex_init(&self->mutex, NULL);
    if(pthread_cond_init(&self->cond, NULL)) {
        PyErr_Format(PyExc_SystemError, "could not initialize condvar");
        return NULL;
    }

    if(! ((self->deque = PyObject_CallFunctionObjArgs(py_deque, NULL)))) {
        Py_DECREF(self);
        return NULL;
    }

    return (PyObject *) self;
}

static int
latch_clear(LatchObject *self)
{
    Py_CLEAR(self->notify);
    Py_CLEAR(self->deque);
    return 0;
}

/**
 * Latch.__del__()
 */
static void
latch_dealloc(LatchObject *self)
{
    if(self->weaklist) {
        PyObject_ClearWeakRefs((PyObject *) self);
        self->weaklist = NULL;
    }

    latch_clear(self);
    PyObject_Del(self);
}

/**
 * Latch.close()
 */
static PyObject *
latch_close(LatchObject *self)
{
    Py_BEGIN_ALLOW_THREADS
    (void) pthread_mutex_lock(&self->mutex);
    if(! self->closed) {
        self->closed = 1;
        (void) pthread_cond_broadcast(&self->cond);
    }
    (void) pthread_mutex_unlock(&self->mutex);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

/**
 * Latch.size()
 */
static PyObject *
latch_size(LatchObject *self)
{
    if(self->closed) {
        PyErr_Format(py_LatchError, "Latch is closed");
        return NULL;
    }
    return PyLong_FromSsize_t(self->size);
}

/**
 * Latch.empty()
 */
static PyObject *
latch_empty(LatchObject *self)
{
    if(self->closed) {
        PyErr_Format(py_LatchError, "Latch is closed");
        return NULL;
    }
    return PyBool_FromLong(self->size == 0);
}

/**
 * Latch.get(timeout=None, block=True)
 */
static PyObject *
latch_get(LatchObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *py_timeout = NULL;
    double timeout;
    int block = -1;

    static char *keywords[] = {"timeout", "block", NULL};
    if(! PyArg_ParseTupleAndKeywords(args, kwds, "|Oi", keywords,
                                     &py_timeout, &block)) {
        return NULL;
    }

    struct timespec ts;
    if(py_timeout) {
        if(py_timeout == Py_None) {
            py_timeout = NULL;
        } else {
            PyObject *f = PyNumber_Float(py_timeout);
            if(! f) {
                return NULL;
            }

            timeout = PyFloat_AsDouble(f);
            Py_DECREF(f);
        }

        double i, f;
        f = modf(timeout, &i);
        ts.tv_sec = time(NULL) + (time_t) i;
        ts.tv_nsec = (long) (1e9 * f);
    }

    for(;;) {
        if(self->closed) {
            PyErr_Format(py_LatchError, "Latch is closed");
            return NULL;
        }

        PyObject *ret = PyObject_CallFunctionObjArgs(py_deque__popleft,
            self->deque, NULL);
        if(ret) {
            self->size--;
            return ret;
        }
        PyErr_Clear(); // IndexError

        if(! block) {
            PyErr_Format(py_TimeoutError, "Latch is empty");
            return NULL;
        }

        int rc;
        Py_BEGIN_ALLOW_THREADS
            (void) pthread_mutex_lock(&self->mutex);
            if(! py_timeout) {
                ts.tv_sec = time(NULL) + (time_t) 2;
                ts.tv_nsec = 0;
            }

            rc = pthread_cond_timedwait(&self->cond, &self->mutex, &ts);
            if(rc != EINTR) {
                (void) pthread_mutex_unlock(&self->mutex);
            }
        Py_END_ALLOW_THREADS

        if(PyErr_CheckSignals()) {
            return NULL;
        }

        if(rc == EINTR) {
            continue;
        } else if(rc == ETIMEDOUT) {
            if(! py_timeout) {
                continue;
            }
            PyErr_Format(py_TimeoutError, "get() timed out");
            return NULL;
        }
    }
}

/**
 * Latch.put(obj=None)
 */
static PyObject *
latch_put(LatchObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *obj = NULL;

    static char *keywords[] = {"obj", NULL};
    if(! PyArg_ParseTupleAndKeywords(args, kwds, "|O", keywords, &obj)) {
        return NULL;
    }

    if(self->closed) {
        PyErr_Format(py_LatchError, "Latch is closed");
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
        (void) pthread_mutex_lock(&self->mutex);
    Py_END_ALLOW_THREADS

    if(! obj) {
        obj = Py_None;
    }

    PyObject *ret = PyObject_CallFunctionObjArgs(py_deque__append,
        self->deque, obj, NULL);
    if(ret) {
        self->size++;
        pthread_cond_signal(&self->cond);
    }
    (void) pthread_mutex_unlock(&self->mutex);

    if(ret && self->notify != Py_None) {
        Py_DECREF(ret);
        ret = PyObject_CallFunctionObjArgs(self->notify, self, NULL);
    }

    return ret;
}

/**
 * @Latch._on_fork()
 */
static PyObject *
latch_on_fork(LatchObject *self, PyObject *args, PyObject *kwds)
{
    Py_RETURN_NONE;
}


/*
 * ansible.playbook.base.FieldAttributeBase.copy()
 */

static int
copy_attr(PyObject *dst, PyObject *src, PyObject *attr, int optional)
{
    PyObject *value = PyObject_GetAttr(src, attr);
    if(! value) {
        if(optional) {
            PyErr_Clear();
            return 0;
        }
        return -1;
    }

    if(PyObject_SetAttr(dst, attr, value)) {
        Py_DECREF(value);
        return -1;
    }

    Py_DECREF(value);
    return 0;
}

static PyObject *
shallow_copy_value(PyObject *v)
{
    PyTypeObject *t = Py_TYPE(v);

    if(v == Py_None ||
       t == &PyBool_Type ||
#if PY_MAJOR_VERSION < 3
       t == &PyInt_Type ||
#endif
       t == &PyLong_Type ||
       t == &PyUnicode_Type ||
       t == &PyBytes_Type ||
       t == (PyTypeObject *) py_ansible__unicode ||
       v == py_ansible__sentinel) {
        Py_INCREF(v);
        return v;
    }

    if(t == &PyList_Type) {
        return PyList_GetSlice(v, 0, PyList_GET_SIZE(v));
    }
    if(t == &PyDict_Type) {
        return PyDict_Copy(v);
    }
    if(t == &PySet_Type) {
        return PyObject_CallMethodObjArgs(v, py_u__copy, NULL);
    }

    return PyObject_CallFunctionObjArgs(py_copy__copy, v, NULL);
}

static int
shallow_copy_item(PyObject *dst, PyObject *src, PyObject *key)
{
    PyObject *v = /* borrow */ PyDict_GetItem(src, key);
    if(! v) {
        PyErr_SetObject(PyExc_KeyError, key);
        return -1;
    }

    PyObject *v2 = shallow_copy_value(v);
    if(! v2) {
        return -1;
    }

    int rc = PyDict_SetItem(dst, key, v2);
    Py_DECREF(v2);
    return rc;
}


static PyObject *
py_FieldAttributeBase__copy(PyObject *self, PyObject *args)
{
    PyObject *class = NULL;
    PyObject *valid_attrs = NULL;
    PyObject *alias_attrs = NULL;
    PyObject *new = NULL;
    PyObject *old_attributes = NULL;
    PyObject *new_attributes = NULL;
    PyObject *old_attr_defaults = NULL;
    PyObject *new_attr_defaults = NULL;

    if(PyTuple_GET_SIZE(args) != 1) {
        PyErr_SetString(PyExc_TypeError,
            "copy() accepts exactly one argument");
        return NULL;
    }

    self = PyTuple_GET_ITEM(args, 0);

    if(! ((class = PyObject_GetAttr(self, py_u__class__)))) {
        goto fail;
    }

    if(! ((valid_attrs = PyObject_GetAttr(self, py_u__valid_attrs)))) {
        goto fail;
    }

    if(! ((alias_attrs = PyObject_GetAttr(self, py_u__alias_attrs)))) {
        goto fail;
    }

    if(! ((new = PyObject_CallFunction(class, NULL)))) {
        goto fail;
    }

    if(! ((old_attributes = PyObject_GetAttr(self, py_u__attributes)))) {
        goto fail;
    }

    if(! ((new_attributes = PyObject_GetAttr(new, py_u__attributes)))) {
        goto fail;
    }

    if(! ((old_attr_defaults = PyObject_GetAttr(self, py_u__attr_defaults)))) {
        goto fail;
    }

    if(! ((new_attr_defaults = PyObject_GetAttr(new, py_u__attr_defaults)))) {
        goto fail;
    }

    if(copy_attr(new, self, py_u__loader, 0)) {
        goto fail;
    }
    if(copy_attr(new, self, py_u__variable_manager, 0)) {
        goto fail;
    }
    if(copy_attr(new, self, py_u__validated, 0)) {
        goto fail;
    }
    if(copy_attr(new, self, py_u__finalized, 0)) {
        goto fail;
    }
    if(copy_attr(new, self, py_u__uuid, 0)) {
        goto fail;
    }
    if(copy_attr(new, self, py_u__ds, 1)) {
        goto fail;
    }

    Py_ssize_t ppos = 0;
    PyObject *pkey;
    PyObject *pvalue;

    while(PyDict_Next(valid_attrs, &ppos, &pkey, &pvalue)) {
        if(! PySequence_Contains(alias_attrs, pkey)) {
            if(shallow_copy_item(new_attributes, old_attributes, pkey)) {
                goto fail;
            }

            if(shallow_copy_item(new_attr_defaults, old_attr_defaults, pkey)) {
                goto fail;
            }
        }
    }

    goto out;

fail:
    Py_CLEAR(new);
out:
    Py_XDECREF(class);
    Py_XDECREF(valid_attrs);
    Py_XDECREF(alias_attrs);
    Py_XDECREF(old_attributes);
    Py_XDECREF(new_attributes);
    Py_XDECREF(old_attr_defaults);
    Py_XDECREF(new_attr_defaults);
    return new;
}


/*
 * module_response_deepcopy()
 */

static PyObject *
module_response_deepcopy(PyObject *v);

static PyObject *
module_response_deepcopy_dict(PyObject *v);

static PyObject *
module_response_deepcopy_list(PyObject *v);


static PyObject *
module_response_deepcopy_dict(PyObject *v)
{
    Py_ssize_t ppos = 0;
    PyObject *pkey;
    PyObject *pvalue;

    PyObject *dct = PyDict_New();
    if(! dct) {
        return NULL;
    }

    while(PyDict_Next(v, &ppos, &pkey, &pvalue)) {
        PyObject *elem = module_response_deepcopy(pvalue);
        if(elem == NULL) {
            Py_DECREF(dct);
            return NULL;
        }

        if(PyDict_SetItem(dct, pkey, elem)) {
            Py_DECREF(dct);
            Py_DECREF(elem);
            return NULL;
        }

        Py_DECREF(elem);
    }

    return dct;
}

static PyObject *
module_response_deepcopy_list(PyObject *v)
{
    PyObject *lst = PyList_New(PyList_GET_SIZE(v));
    if(! lst) {
        return NULL;
    }

    for(int i = 0; i < PyList_GET_SIZE(v); i++) {
        PyObject *elem = module_response_deepcopy(PyList_GET_ITEM(v, i));
        if(! elem) {
            Py_DECREF(lst);
            return NULL;
        }

        PyList_SET_ITEM(lst, i, elem);
    }

    return lst;
}

static PyObject *
module_response_deepcopy(PyObject *v)
{
    if(PyDict_Check(v)) {
        v = module_response_deepcopy_dict(v);
    } else if(PyList_Check(v)) {
        v = module_response_deepcopy_list(v);
    } else {
        Py_INCREF(v);
    }

    return v;
}

static PyObject *
py_module_response_deepcopy(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *obj = NULL;
    static char *keywords[] = {"v", NULL};

    if(! PyArg_ParseTupleAndKeywords(args, kwds, "O", keywords, &obj)) {
        return NULL;
    }

    return module_response_deepcopy(obj);
}


/*
 * strip_internal_keys()
 */

enum strip_internal_keys_status {
    kUnrecognizedType,
    kSuccess,
    kInternalError
};

static enum strip_internal_keys_status
strip_internal_keys(PyObject *obj, PyObject *exceptions);

static enum strip_internal_keys_status
strip_internal_keys_dict(PyObject *obj, PyObject *exceptions);

static enum strip_internal_keys_status
strip_internal_keys_list(PyObject *obj, PyObject *exceptions);


static enum strip_internal_keys_status
strip_internal_keys_list(PyObject *obj, PyObject *exceptions)
{
    Py_ssize_t i;
    enum strip_internal_keys_status status = kSuccess;

    for(i = 0; status == kSuccess && i < PyList_GET_SIZE(obj); i++) {
        switch(strip_internal_keys(PyList_GET_ITEM(obj, i), exceptions)) {
            case kUnrecognizedType:
                /* fallthrough */
            case kSuccess:
                break;
            case kInternalError:
                status = kInternalError;
                break;
        }
    }

    return status;
}


static int
is_internal_key(PyObject *k, PyObject *exceptions)
{
    int is_true = 0;

    if(PyUnicode_Check(k)) {
        PyObject *rc = PyObject_CallFunctionObjArgs(
            py_unicode_startswith,
            k,
            py_u_ansible,
            NULL
        );
        assert(rc != NULL);
        is_true = PyObject_IsTrue(rc);
        Py_DECREF(rc);
    } else if(PyBytes_Check(k)) {
        PyObject *rc = PyObject_CallFunctionObjArgs(
            py_bytes_startswith,
            k,
            py_b_ansible,
            NULL
        );
        assert(rc != NULL);
        is_true = PyObject_IsTrue(rc);
        Py_DECREF(rc);
    }

    if(is_true && exceptions) {
        is_true = !PySequence_Contains(exceptions, k);
    }

    return is_true;
}


static enum strip_internal_keys_status
strip_internal_keys_dict(PyObject *obj, PyObject *exceptions)
{
    Py_ssize_t ppos = 0;
    PyObject *pkey;
    PyObject *pvalue;
    PyObject *tmp;

    if(! ((tmp = PyList_New(0)))) {
        return kInternalError;
    }

    enum strip_internal_keys_status status = kSuccess;
    while(status == kSuccess && PyDict_Next(obj, &ppos, &pkey, &pvalue)) {
        if(is_internal_key(pkey, exceptions)) {
            if(PyList_Append(tmp, pkey)) {
                return kInternalError;
            }
        }

        switch(strip_internal_keys(pvalue, exceptions)) {
            case kUnrecognizedType:
                /* fallthrough */
            case kSuccess:
                break;
            case kInternalError:
                status = kInternalError;
        }
    }

    for(int i = 0; status == kSuccess && i < PyList_GET_SIZE(tmp); i++) {
        if(PyDict_DelItem(obj, PyList_GET_ITEM(tmp, i))) {
            status = kInternalError;
        }
    }

    Py_DECREF(tmp);
    return status;
}


static enum strip_internal_keys_status
strip_internal_keys(PyObject *obj, PyObject *exceptions)
{
    if(PyList_Check(obj)) {
        return strip_internal_keys_list(obj, exceptions);
    } else if (PyDict_Check(obj)) {
        return strip_internal_keys_dict(obj, exceptions);
    }
    return kUnrecognizedType;
}


static PyObject *
py_strip_internal_keys(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *obj = NULL;
    PyObject *exceptions = NULL;
    static char *keywords[] = {"obj", "exceptions", NULL};

    if(! PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords,
                                     &obj, &exceptions)) {
        return NULL;
    }

    switch(strip_internal_keys(obj, exceptions)) {
        case kUnrecognizedType:
            PyErr_SetString(PyExc_TypeError,
                "incorrect input type for strip_internal_keys()");
            /* fallthrough */
        case kInternalError:
            return NULL;
        case kSuccess:
            break;
    }

    Py_INCREF(obj);
    return obj;
}


/*
 * Boilerplate / type defs.
 */

static struct PyMethodDef latch_methods[] = {
    {"close", (PyCFunction)latch_close, METH_NOARGS},
    {"size", (PyCFunction)latch_size, METH_NOARGS},
    {"empty", (PyCFunction)latch_empty, METH_NOARGS},
    {"get", (PyCFunction)latch_get, METH_VARARGS|METH_KEYWORDS},
    {"put", (PyCFunction)latch_put, METH_VARARGS|METH_KEYWORDS},
    {"_on_fork", (PyCFunction)latch_on_fork, METH_CLASS|METH_NOARGS},
    {NULL, NULL}
};

static struct PyMemberDef latch_attrs[] = {
    {"notify", T_OBJECT_EX, offsetof(LatchObject, notify), 0, ""},
    {NULL, 0, 0, 0, NULL}
};


static PyTypeObject PyLatch_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "Latch",                    /*tp_name*/
    sizeof(LatchObject),        /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor) latch_dealloc, /*tp_dealloc*/
    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
    0,                          /*tp_setattr*/
    0,                          /*tp_compare*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    0,                          /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash*/
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    0,                          /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,         /*tp_flags*/
    0,                          /*tp_doc*/
    0,                          /*tp_traverse*/
    (inquiry) latch_clear,      /*tp_clear*/
    0,                          /*tp_richcompare*/
    offsetof(LatchObject, weaklist), /*tp_weaklistoffset*/
    0,                          /*tp_iter*/
    0,                          /*tp_iternext*/
    latch_methods,              /*tp_methods*/
    latch_attrs,                /*tp_members*/
    0,                          /*tp_getset*/
    0,                          /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    0,                          /*tp_init*/
    0,                          /*tp_alloc*/
    latch_new,                  /*tp_new*/
    0,                          /*tp_free*/
};


static struct PyMethodDef module_methods[] = {
    {"FieldAttributeBase__copy", (PyCFunction) py_FieldAttributeBase__copy, METH_VARARGS, ""},
    {"module_response_deepcopy", (PyCFunction) py_module_response_deepcopy, METH_VARARGS|METH_KEYWORDS, ""},
    {"strip_internal_keys", (PyCFunction) py_strip_internal_keys, METH_VARARGS|METH_KEYWORDS, ""},
    {0, 0, 0, 0}
};


#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cpython",
    NULL,
    -1,
    module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif


struct string_const
{
    const char *constant;
    PyObject **obj;
};


static const struct string_const unicode_consts[] = {
    {"__class__", &py_u__class__},
    {"_loader", &py_u__loader},
    {"_variable_manager", &py_u__variable_manager},
    {"_validated", &py_u__validated},
    {"_validated", &py_u__validated},
    {"_finalized", &py_u__finalized},
    {"_uuid", &py_u__uuid},
    {"_ds", &py_u__ds},
    {"_attributes", &py_u__attributes},
    {"_attr_defaults", &py_u__attr_defaults},
    {"_alias_attrs", &py_u__alias_attrs},
    {"_valid_attrs", &py_u__valid_attrs},

    {"copy", &py_u__copy},
    {NULL, NULL}
};


/**
 * Do all required to initialize the lmdb.cpython module.
 */
PyMODINIT_FUNC
MODINIT_NAME(void)
{
    for(int i = 0; unicode_consts[i].constant; i++) {
        const struct string_const *sc = &unicode_consts[i];
        *(sc->obj) = PyUnicode_FromString(sc->constant);
        if(! *(sc->obj)) {
            MOD_RETURN(NULL);
        }
    }

    if(! ((py_unicode_startswith = PyObject_GetAttrString(
            (PyObject *) &PyUnicode_Type,
            "startswith")))) {
        MOD_RETURN(NULL);
    }

    if(! ((py_bytes_startswith = PyObject_GetAttrString(
            (PyObject *) &PyBytes_Type,
            "startswith")))) {
        MOD_RETURN(NULL);
    }

    if(! ((py_u_ansible = PyUnicode_FromString("_ansible_")))) {
        MOD_RETURN(NULL);
    }

    if(! ((py_b_ansible = PyBytes_FromString("_ansible_")))) {
        MOD_RETURN(NULL);
    }

    {
        PyObject *copy = PyImport_ImportModule("copy");
        if(! copy) {
            MOD_RETURN(NULL);
        }

        if(! ((py_copy__copy = PyObject_GetAttrString(copy, "copy")))) {
            Py_DECREF(copy);
            MOD_RETURN(NULL);
        }

        Py_DECREF(copy);
    }

    {
        PyObject *core = PyImport_ImportModule("mitogen.core");
        if(! core) {
            MOD_RETURN(NULL);
        }

        if(! ((py_LatchError = PyObject_GetAttrString(core, "LatchError")))) {
            Py_DECREF(core);
            MOD_RETURN(NULL);
        }

        if(! ((py_TimeoutError = PyObject_GetAttrString(core, "LatchError")))) {
            Py_DECREF(core);
            MOD_RETURN(NULL);
        }

        Py_DECREF(core);
    }


    {
        PyObject *collections = PyImport_ImportModule("collections");
        if(! collections) {
            MOD_RETURN(NULL);
        }

        if(! ((py_deque = PyObject_GetAttrString(collections, "deque")))) {
            Py_DECREF(collections);
            MOD_RETURN(NULL);
        }

        if(! ((py_deque__append = PyObject_GetAttrString(
                py_deque, "append")))) {
            Py_DECREF(collections);
            MOD_RETURN(NULL);
        }

        if(! ((py_deque__popleft = PyObject_GetAttrString(
                py_deque, "popleft")))) {
            Py_DECREF(collections);
            MOD_RETURN(NULL);
        }

        Py_DECREF(collections);
    }

    {
        PyObject *smod = PyImport_ImportModule("ansible.utils.sentinel");
        // dont fail, for tests.
        if(smod) {
            if(! ((py_ansible__sentinel = PyObject_GetAttrString(smod, "Sentinel")))) {
                Py_DECREF(smod);
                MOD_RETURN(NULL);
            }

            Py_DECREF(smod);
        } else {
            PyErr_Clear();
        }
    }

    {
        PyObject *umod = PyImport_ImportModule("ansible.parsing.yaml.objects");
        // dont fail, for tests.
        if(umod) {
            if(! ((py_ansible__unicode = PyObject_GetAttrString(
                    umod,
                    "AnsibleUnicode"
                    )))) {
                Py_DECREF(umod);
                MOD_RETURN(NULL);
            }

            Py_DECREF(umod);
        } else {
            PyErr_Clear();
        }
    }

#if PY_MAJOR_VERSION >= 3
    PyObject *mod = PyModule_Create(&moduledef);
#else
    PyObject *mod = Py_InitModule3("cpython", module_methods, "");
#endif
    if(! mod) {
        MOD_RETURN(NULL);
    }

    if(PyType_Ready(&PyLatch_Type)) {
        MOD_RETURN(NULL);
    }

    if(PyObject_SetAttrString(mod, "Latch", (PyObject *)&PyLatch_Type)) {
        MOD_RETURN(NULL);
    }

    MOD_RETURN(mod);
}
