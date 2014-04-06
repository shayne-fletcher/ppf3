#include <boost/python/module.hpp>

namespace ppf
{
  namespace date_time
  {
    void register_date();
    void register_date_more();
    
  } // namespace date_time

} // namespace ppf

BOOST_PYTHON_MODULE(ppf_date_time)
/*
void init_module_ppf_date_time();
extern "C" __declspec(dllexport) void initppf_date_time()
{
  boost::python::detail::init_module( "ppf_date_time", &init_module_ppf_date_time);
}

void init_ppf_date_time()
*/
{
  using namespace ppf::date_time;

  register_date();
  register_date_more();
}
