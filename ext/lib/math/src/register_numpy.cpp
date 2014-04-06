#include <ppf/math/detail/wrap_array_object.hpp>
#include <ppf/util/python/detail/object_as_array.hpp>
#include <ppf/util/python/detail/decref.hpp>

#include <boost/python/def.hpp>

#include <blitz/array.h>

#include <numeric>

namespace ppf { namespace math { namespace numpy {

namespace examples
{

double sum_array(PyObject* input)
{
  boost::shared_ptr<PyArrayObject> obj =
    ::ppf::util::python::detail::object_as_array(input, PyArray_DOUBLE, 0, 0);

  // compute size of array 
  int n = 1;
  if(obj->nd > 0)
    for(int i = 0; i < obj->nd; ++i) 
      n *= obj->dimensions[i];

  double* array = reinterpret_cast<double*>(obj->data);

  return std::accumulate(array, array + n, 0.);
}

double trace(PyObject* input)
{
  boost::shared_ptr<PyArrayObject> obj =
    ::ppf::util::python::detail::object_as_array(input, PyArray_DOUBLE, 2, 2);

  int n = obj->dimensions[0];
  if(n > obj->dimensions[1]) n = obj->dimensions[1];

  double sum = 0.;
  for(int i = 0; i < n; ++i)
    sum += *reinterpret_cast<double*>(
      obj->data + i*obj->strides[0] + i*obj->strides[1]);

  return sum;
}

void assign_zero(PyObject* input)
{
  boost::shared_ptr<PyArrayObject> obj =
    ::ppf::util::python::detail::object_as_array(input, PyArray_DOUBLE, 2, 2);

  blitz::Array<double, 2> array(
      reinterpret_cast<double*>(obj->data)
    , blitz::shape(obj->dimensions[0], obj->dimensions[1])
    , blitz::neverDeleteData);
    array = 0;
}

PyObject* make_array(int n)
{
  int dimensions[1]; dimensions[0] = n;
  PyArrayObject* result =
    reinterpret_cast<PyArrayObject*>(
        boost::python::expect_non_null(
          PyArray_FromDims(1, dimensions, PyArray_DOUBLE)));
  double* buffer = reinterpret_cast<double*>(result->data);
  for(int i = 1; i < n; ++i) buffer[i] = i;

  return PyArray_Return(result);
}

}}//namespace numpy::examples

void register_numpy()
{
  using namespace boost::python;

  def("numpy_sum_array", numpy::examples::sum_array);
  def("numpy_trace", numpy::examples::trace);
  def("numpy_assign_zero", numpy::examples::assign_zero);
  def("numpy_make_array", numpy::examples::make_array);

  if (_import_array() < 0) 
  {
    PyErr_Print(); 
    PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); 
  } 

  return;
}

}} // namespace ppf::math

