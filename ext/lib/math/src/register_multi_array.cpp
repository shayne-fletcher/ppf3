// Copyright Daniel Wallin 2006. Use, modification and distribution is
// subject to the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/module.hpp>
#include <boost/multi_array/python.hpp>

namespace ppf { namespace math {

void register_multi_array()
{
  using namespace boost::multi_array_python;

  wrap_multi_array<double, 1>("double");
  wrap_multi_array<double, 2>("double");
  wrap_multi_array<double, 3>("double");
}

}} // namespace ppf::math

