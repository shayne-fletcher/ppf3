#include <boost/python/module.hpp>

namespace ppf
{
  namespace math
  {
    void register_multi_array();
    void register_special_functions();
    void register_numpy();
    
  } // namespace math

} // namespace ppf

BOOST_PYTHON_MODULE(ppf_math)
/*
void init_module_ppf_math();
extern "C" __declspec(dllexport) void initppf_math()
{
  boost::python::detail::init_module( "ppf_math", &init_module_ppf_math);
}

void init_ppf_math()
*/
{
  using namespace ppf::math;
  using namespace boost::python;

  register_multi_array();
  register_special_functions();
  register_numpy();
}
