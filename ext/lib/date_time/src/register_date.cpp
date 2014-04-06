#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/date_generators.hpp>
#include <boost/implicit_cast.hpp>
#include <boost/python/module.hpp>
#include <boost/python/class.hpp>
#include <boost/python/def.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/implicit.hpp>
#include <boost/python/operators.hpp>
#include <boost/python/pure_virtual.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

namespace ppf { namespace date_time {

void register_date()
{
  using boost::implicit_cast;
  using namespace boost::python;
  namespace bg = boost::gregorian;
  namespace bd = boost::date_time;

  class_<bd::int_adapter<int> >("int_adapter_int", init<int>())
     .def("has_infinity", &bd::int_adapter<int>::has_infinity)
     .def("pos_infinity", &bd::int_adapter<int>::pos_infinity)
     .def("neg_infinity", &bd::int_adapter<int>::neg_infinity)
     .def("not_a_number", &bd::int_adapter<int>::not_a_number)
     .def("max", &bd::int_adapter<int>::max)
     .def("min", &bd::int_adapter<int>::min)
     .def("from_special", &bd::int_adapter<int>::from_special)
     .def("is_inf", &bd::int_adapter<int>::is_inf)
     .def("is_neg_inf", &bd::int_adapter<int>::is_neg_inf)
     .def("is_pos_inf", &bd::int_adapter<int>::is_pos_inf)
     .def("is_not_a_number", &bd::int_adapter<int>::is_not_a_number)
     .def("to_special", &bd::int_adapter<int>::to_special)
     .def("maxcount", &bd::int_adapter<int>::maxcount)
     .def("is_infinity", &bd::int_adapter<int>::is_infinity)
     .def("is_pos_infinity", &bd::int_adapter<int>::is_pos_infinity)
     .def("is_neg_infinity", &bd::int_adapter<int>::is_neg_infinity)
     .def("is_nan", &bd::int_adapter<int>::is_nan)
     .def("is_special", &bd::int_adapter<int>::is_special)
     .def(self == self)
     .def(self == other<int >())
     .def(self != self)
     .def(self != other<int >())
     .def(self <self)
     .def(self <other<int >())
     .def(self > self)
     .def("as_number", &bd::int_adapter<int>::as_number)
     .def("as_special", &bd::int_adapter<int>::as_special)
     .def(self + other<int >())
     .def(self - other<int >())
     .def(self * self)
     .def(self * other<int >())
     .def(self / self)
     .def(self / other<int >())
     .def(self % self)
     .def(self % other<int >())
     .staticmethod("has_infinity")
     .staticmethod("pos_infinity")
     .staticmethod("neg_infinity")
     .staticmethod("not_a_number")
     .staticmethod("max")
     .staticmethod("min")
     .staticmethod("from_special")
     .staticmethod("is_inf")
     .staticmethod("is_neg_inf")
     .staticmethod("is_pos_inf")
     .staticmethod("is_not_a_number")
     .staticmethod("to_special")
     .staticmethod("maxcount")
    ;

  enum_<bd::special_values>("special_values")
    .value("not_a_date_time", bd::not_a_date_time)
    .value("neg_infin", bd::neg_infin)
    .value("pos_infin", bd::pos_infin)
    .value("min_date_time", bd::min_date_time)
    .value("max_date_time", bd::max_date_time)
    .value("not_special", bd::not_special)
    .value("NumSpecialValues", bd::NumSpecialValues)
    ;

  enum_<bg::months_of_year>("months_of_year")
    .value("Jan", bg::Jan)
    .value("Feb", bg::Feb)
    .value("Mar", bg::Mar)
    .value("Apr", bg::Apr)
    .value("May", bg::May)
    .value("Jun", bg::Jun)
    .value("Jul", bg::Jul)
    .value("Aug", bg::Aug)
    .value("Sep", bg::Sep)
    .value("Oct", bg::Oct)
    .value("Nov", bg::Nov)
    .value("Dec", bg::Dec)
    .value("NotAMonth", bg::NotAMonth)
    .value("NumMonths", bg::NumMonths)
    ;

  enum_<bd::weekdays>("weekdays")
    .value("Sunday", bd::Sunday)
    .value("Monday", bd::Monday)
    .value("Tuesday", bd::Tuesday)
    .value("Wednesday", bd::Wednesday)
    .value("Thursday", bd::Thursday)
    .value("Friday", bd::Friday)
    .value("Saturday", bd::Saturday)
    ;

  class_<bg::greg_year>("year_type"
                        , "Allows for simple conversion of an integer"
                          " value into a year for the gregorian calendar"
                        , init<unsigned short int>())
    .def("__int__", &bg::greg_year::operator unsigned short int)
    ;

  implicitly_convertible<short unsigned int, bg::greg_year>();
  implicitly_convertible<bg::greg_year, short unsigned int >();

  class_<bg::greg_month>("month_type"
                       , "A class to represent months in gregorian "
                         "based calendar"
                       , init<bg::months_of_year>())
    .def(init<unsigned short int>())
    .def("__int__", &bg::greg_month::operator unsigned short int)
    .def("as_number", &bg::greg_month::as_number)
    .def("as_enum", &bg::greg_month::as_enum)
    ;
  
  implicitly_convertible<bg::months_of_year, bg::greg_month>();
  implicitly_convertible<unsigned short int, bg::greg_month>();
  implicitly_convertible<bg::greg_month, short unsigned int>();

  class_<bg::greg_day>("day_type"
                     , "Represent a day of the month (range 1 - 31)"
                     , init<unsigned short int>())
    .def("__int__", &bg::greg_day::operator unsigned short int)
    .def("as_number", &bg::greg_day::as_number)
    ;

  implicitly_convertible<unsigned short int, bg::greg_day>();
  implicitly_convertible<bg::greg_day, unsigned short int>();

  class_<bg::greg_year_month_day>("year_month_day_type"
    , "Allow rapid creation of ymd triples"
    , init<bg::greg_year, bg::greg_month, bg::greg_day>())
    .def_readonly("year", &bg::greg_year_month_day::year)
    .def_readonly("month", &bg::greg_year_month_day::month)
    .def_readonly("day", &bg::greg_year_month_day::day)
    ;

  class_<bg::greg_weekday>("weekday_type",
                           "Represent a day within a week "
                           "(range 0==Sun to 6==Sat)"
                           , init<short unsigned int>())
    .def("as_number", &bg::greg_weekday::as_number)
    .def("as_enum", &bg::greg_weekday::as_enum)
    ;

  implicitly_convertible<unsigned short int, bg::greg_weekday>();
  implicitly_convertible<bg::greg_weekday, unsigned short int>();

  class_<bg::greg_day_of_year_rep>("day_of_year_type"
    , "A day of the year range  (1..366)", init<unsigned short int>())
    .def( "__int__", &bg::greg_day_of_year_rep::operator short unsigned int)
    .def( "as_number",
          &bg::greg_day_of_year_rep::operator
            bg::greg_day_of_year_rep::value_type)
    .def("max", &bg::greg_day_of_year_rep::max)
    .def("min", &bg::greg_day_of_year_rep::min)
    .staticmethod("max")
    .staticmethod("min")
    ;

  implicitly_convertible<unsigned short int, bg::greg_day_of_year_rep>();
  implicitly_convertible<bg::greg_day_of_year_rep, unsigned short int>();

  class_<bg::date_duration>("days"
    , "Duration type", init<long>("Construct from a day count"))
    .def(init<bg::date_duration const&>())
    .def("__int__", &bg::date_duration::days)
    .def("days", &bg::date_duration::days, "Returns days as value, not object")
    .def("unit", &bg::date_duration::unit
         , "Returns the smallest duration -- used to calculate 'end'")
    .staticmethod("unit")
    .def(self == self)
    .def(self != self)
    .def(self <self)
    .def(self <= self)
    .def(self > self)
    .def(self >= self)
    ;

  class_<bg::weeks, bases<bg::days> >("weeks"
    , "Additional duration type that "
      "represents a number of n*7 days", init<int>())
    .def(init<bg::weeks const&>())
    ;

  class_<bg::months>("months"
    , "Additional duration type that represents a logical month", init<int>())
    .def(init<bg::months const&>())
    .def("number_of_months", &bg::months::number_of_months)
    .def("get_offset", &bg::months::get_offset)
    .def(self == self)
    .def(self != self)
    .def(self + self)
    .def(self += self)
    .def(self - self)
    .def(self -= self)
    .def(self * other<int>())
    .def(self *= other<int>())
    .def(self / other<int>())
    .def(self /= other<int>())
    .def(self - other<bd::years_duration<bg::greg_durations_config> >())
    .def(self -= other<bd::years_duration<bg::greg_durations_config> >())
    ;

  class_<bg::years>("years"
    , "Addtional duration type that represents a logical year", init<int>())
    .def(init<bg::years const&>())
    .def("number_of_years", &bg::years::number_of_years)
    .def("get_neg_offset"
         , &bg::years::get_neg_offset, "Returns a negative duration")
    .def("get_offset", &bg::years::get_offset)
    .def(self == self)
    .def(self != self)
    .def(self + self)
    .def(self += self)
    .def(self - self)
    .def(self -= self)
    .def(self * other<int>())
    .def(self *= other<int>())
    .def(self / other<int>())
    .def(self /= other<int>())
    .def(self + other<bg::months>())
    .def(self - other<bg::months>())
    ;

  class_<bd::day_functor<bg::date> >("day_functor"
    , "Functor to iterate a fixed number of days", init<int>())
    .def("get_offset", &bd::day_functor<bg::date>::get_offset)
    .def("get_neg_offset", &bd::day_functor<bg::date>::get_neg_offset)
    ;

  class_<bd::month_functor<bg::date> >("month_functor"
    , "Provides calculation to next nth month given a date", init<int>())
    .def("get_offset", &bd::month_functor<bg::date>::get_offset)
    .def("get_neg_offset", &bd::month_functor<bg::date>::get_neg_offset)    
    ;

  class_<bd::week_functor<bg::date> >("week_functor"
    , "Functor to iterate over weeks", init<int>())
    .def("get_offset", &bd::week_functor<bg::date>::get_offset)
    .def("get_neg_offset", &bd::week_functor<bg::date>::get_neg_offset)    
    ;

  class_<bd::year_functor<bg::date> >("year_functor", "Functor to iterate by a year adjusting for leap years", init<int>())
    .def("get_offset", &bd::year_functor<bg::date>::get_offset)
    .def("get_neg_offset", &bd::year_functor<bg::date>::get_neg_offset)    
    ;
  
  class_<bg::date>("date","A date type based on the gregorian calendar", init<>("Default construct constructs with not_a_date_time"))
    .def(init<bg::date const&>())
    .def(init<bg::greg_year, bg::greg_month, bg::greg_day>((arg("y"), arg("m"), arg("d")), "Main constructor with year, month, day "))
    .def(init<bg::greg_year_month_day const&>("Construct from a year_month_day_type structure"))
    .def("year", &bg::date::year)
    .def("month", &bg::date::month)
    .def("day", &bg::date::day)
    .def("day_of_week", &bg::date::day_of_week)
    .def("year_month_day", &bg::date::year_month_day)
    .def("day_of_year", &bg::date::day_of_year)
    .def("end_of_month", &bg::date::end_of_month)
    .def("is_special", &bg::date::is_special, "Check to see if date is a special value")
    .def("is_not_a_date", &bg::date::is_not_a_date, "Check to see if date is not a value")
    .def("is_infinity", &bg::date::is_infinity, "Check to see if date is greater than all possible dates")
    .def("is_pos_infinity", &bg::date::is_pos_infinity, "Check to see if date is greater than all possible dates")
    .def("is_neg_infinity", &bg::date::is_neg_infinity, "Check to see if date is less than all possible dates")
    .def("as_special", &bg::date::is_special, "Return as a special value or a not_special if a normal date")
    .def("julian_day", &bg::date::julian_day, "Return the Julian day number for the date")
    .def("day_of_year", &bg::date::day_of_year, "Return the day of year 1..365 or 1..366 (for leap year)")
    .def("modjulian_day", &bg::date::modjulian_day, "return the modified Julian day number for the date")
    .def("week_number", &bg::date::week_number, "Return the iso 8601 week number 1..53")
    .def("day_number", &bg::date::day_number, "return the day number from the calendar")
    .def("end_of_month", &bg::date::end_of_month, "Return the last day of the current month")
    .def(self == self)
    .def(self != self)
    .def(self < self)
    .def(self <= self)
    .def(self >  self)
    .def(self >= self)
    .def(self - self)
    .def(self - other<bg::date_duration>())
    .def(self -= other<bg::date_duration>())
    .def(self + other<bg::date_duration>())
    .def(self += other<bg::date_duration>())
    .def(self - other<bg::months>())
    .def(self -= other<bg::months>())
    .def(self + other<bg::months>())
    .def(self += other<bg::months>())
    .def(self - other<bg::years>())
    .def(self -= other<bg::years>())
    .def(self + other<bg::years>())
    .def(self += other<bg::years>())
    .def(str(self)) 
    ;

  implicitly_convertible<bg::greg_year_month_day const&, bg::date>();

  class_<std::vector<bg::date> >("date_vec"
    , "vector (C++ std::vector<date> ) of date")
    .def(vector_indexing_suite<std::vector<bg::date> >())
    ;
}

}} // namespace date_time
