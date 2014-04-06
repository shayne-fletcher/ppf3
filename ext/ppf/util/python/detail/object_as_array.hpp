#if !defined(OBJECT_AS_ARRAY_0067910E_F5F1_4BD6_9565_3BF98B4A12C1_INCLUDED)
#  define OBJECT_AS_ARRAY_0067910E_F5F1_4BD6_9565_3BF98B4A12C1_INCLUDED

#  if defined(_MSC_VER) && (_MSC_VER >= 1020)
#    pragma once
#  endif // defined(_MSC_VER) && (_MSC_VER >= 1020)

#include <ppf/util/python/detail/decref.hpp>

#include <boost/python/errors.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/bind.hpp>

namespace ppf { namespace util { namespace python {

namespace detail
{

template <int = 0>
struct object_as_array_impl_
{
  static boost::shared_ptr<PyArrayObject> get(
    PyObject* input, int type, int min_dim, int max_dim)
  {
    if(PyArray_Check(input))
    {
      if(!PyArray_ISCARRAY(reinterpret_cast<PyArrayObject*>(input)))
      {
        PyErr_SetString(PyExc_TypeError, "not a C array");
  
        boost::python::throw_error_already_set();
      }
  
      return boost::shared_ptr<PyArrayObject>(
            reinterpret_cast<PyArrayObject*>(
                boost::python::expect_non_null(
                   PyArray_ContiguousFromObject(
                      input, type, min_dim, max_dim))
              )
            , boost::bind(decref<PyArrayObject>, _1)
        );
    }
    else
    {
      PyErr_SetString(PyExc_TypeError, "not an array");
  
      boost::python::throw_error_already_set();
    }
  
    return boost::shared_ptr<PyArrayObject>();
  }
};

typedef object_as_array_impl_<> object_as_array_impl;

inline boost::shared_ptr<PyArrayObject>
object_as_array(
  PyObject* input, int type, int min_dim, int max_dim)
{
  return object_as_array_impl::get(input, type, min_dim, max_dim);
}

}}}} // namespace ppf::util::python::detail

#endif // !defined(OBJECT_AS_ARRAY_0067910E_F5F1_4BD6_9565_3BF98B4A12C1_INCLUDED)
