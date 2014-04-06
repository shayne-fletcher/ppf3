#if !defined(LIMITS_5DDE828B_9989_44F5_9728_47AA72323D96_INCLUDED)
#  define LIMITS_5DDE828B_9989_44F5_9728_47AA72323D96_INCLUDED

#  if defined(_MSC_VER) && (_MSC_VER >= 1020)
#    pragma once
#  endif // defined(_MSC_VER) && (_MSC_VER >= 1020)

#  include <boost/config.hpp>

#  include <limits>

namespace ppf { namespace math {

template <class T>
T epsilon()
{
  return std::numeric_limits<T>::epsilon();
}

template <class T>
T min BOOST_PREVENT_MACRO_SUBSTITUTION ()
{
  return (std::numeric_limits<T>::min)();
}

template <class T>
T max BOOST_PREVENT_MACRO_SUBSTITUTION ()
{
  return (std::numeric_limits<T>::max)();
}

}} // namespace ppf::math

#endif // !defined(LIMITS_5DDE828B_9989_44F5_9728_47AA72323D96_INCLUDED)
