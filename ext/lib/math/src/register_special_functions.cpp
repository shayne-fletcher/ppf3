#include <boost/python/def.hpp>

#include <ppf/math/limits.hpp>

namespace ppf { namespace math {

void register_special_functions()
{
  using namespace boost::python;

  def("epsilon", epsilon<double>);
  def("min_flt", min BOOST_PREVENT_MACRO_SUBSTITUTION <double>);
  def("max_flt", max BOOST_PREVENT_MACRO_SUBSTITUTION <double>);
}

}} // namespace ppf::math
