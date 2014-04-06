#include <boost/detail/lightweight_test.hpp>
#include <boost/python.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>

int main()
{
  namespace bd = boost::date_time;
  namespace bg = boost::gregorian;
  namespace python = boost::python;
  typedef bd::year_based_generator<bg::date> ybd_t;

  Py_Initialize();

  try
  {
    //extract the ppf.date_time.nth_imm_of_year class
    //object
    python::object main_module = python::import("__main__");
    python::object global(main_module.attr("__dict__"));
    python::object result =
      python::exec("from ppf.date_time import *\n", global, global);
    python::object nth_imm_of_year_class = global["nth_imm_of_year"];

    //use the class object to create instances of
    //nth_imm_of_year
    python::object first_imm_ = nth_imm_of_year_class(bg::Mar);
    python::object second_imm_ = nth_imm_of_year_class(bg::Jun);
    python::object third_imm_ = nth_imm_of_year_class(bg::Sep);
    python::object fourth_imm_ = nth_imm_of_year_class(bg::Dec);

    //get references to boost date_time year_based_generators
    //from the newly created objects
    ybd_t& first_imm =  python::extract<ybd_t&>(first_imm_);
    ybd_t& second_imm = python::extract<ybd_t&>(second_imm_);
    ybd_t& third_imm =  python::extract<ybd_t&>(third_imm_);
    ybd_t& fourth_imm = python::extract<ybd_t&>(fourth_imm_);

    //check imm dates for 2005
    BOOST_TEST(first_imm.get_date  (2005) == bg::date(2005, bg::Mar, 16));
    BOOST_TEST(second_imm.get_date (2005) == bg::date(2005, bg::Jun, 15));
    BOOST_TEST(third_imm.get_date  (2005) == bg::date(2005, bg::Sep, 21));
    BOOST_TEST(fourth_imm.get_date (2005) == bg::date(2005, bg::Dec, 21));
  }
  catch(python::error_already_set const&)
  {
    PyErr_Print();
  }
  catch(std::runtime_error const& e)
  {
    std::cerr << e.what() << std::endl;
  }
  catch(...)
  {
    std::cerr << "unexpected exception" << std::endl;
  }

  return boost::report_errors();
}
