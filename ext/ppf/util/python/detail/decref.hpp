#if !defined(DECREF_4A1F1D9D_CE18_4CA1_AF52_DA1C51847FB4_INCLUDED)
#  define DECREF_4A1F1D9D_CE18_4CA1_AF52_DA1C51847FB4_INCLUDED

#  if defined(_MSC_VER) && (_MSC_VER >= 1020)
#    pragma once
#  endif // defined(_MSC_VER) && (_MSC_VER >= 1020)

#  include <boost/python/detail/wrap_python.hpp>

namespace ppf { namespace util { namespace python {

namespace detail
{
  //Py_DECREF() is a macro which makes it unsuitable
  //for use with bind constructs in scope guards.
  template <class T>
  inline void decref(T* obj)
  {
    Py_DECREF(obj);
  }
}

}}} // namespace ppf::util::python

#endif // !defined(DECREF_4A1F1D9D_CE18_4CA1_AF52_DA1C51847FB4_INCLUDED)
