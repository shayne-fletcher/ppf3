#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/noncopyable.hpp>
#include <boost/implicit_cast.hpp>
#include <boost/python/class.hpp>
#include <boost/python/def.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/implicit.hpp>
#include <boost/python/operators.hpp>
#include <boost/python/pure_virtual.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

namespace ppf { namespace date_time {

struct year_based_generator_wrap
  : boost::date_time::year_based_generator<boost::gregorian::date>
  , boost::python::wrapper<boost::date_time::year_based_generator<boost::gregorian::date> >
{
  boost::gregorian::date
    get_date(boost::gregorian::date::year_type y) const
  {
    return this->get_override("get_date")(y);
  }

  std::string to_string() const
  {
    //return this->get_override("to_string")();
    return "not implemented - fix me";
  }
};

void register_date_more()
{
  using boost::implicit_cast;
  using namespace boost::python;
  namespace bg = boost::gregorian;
  namespace bd = boost::date_time;

  class_<bg::date_period>("date_period"
    , "A period can be specified by providing either the beginning point "
      "and a duration or the beginning point and the end point (end is not "
      "part of the period but 1 unit past it. A period will be 'invalid' "
      "if either end_point <= begin_point or the given duration <= 0. Any "
      "valid period will return false for is_null(). Zero length periods "
      "are also considered invalid."
    , init<bg::date, bg::date>("Create a period from begin to last eg:[begin,end) If end <= begin then the period will be invalid"))
    .def(init<bg::date, bg::date_duration>("Create a period as [begin,begin +len) If len <= 0 then the period will be invalid"))
    .def(init<bg::date_period const&>())
    .def("begin", &bg::date_period::begin, "Return the first element in the period")
    .def("end", &bg::date_period::end, "Return one past the last element")
    .def("last", &bg::date_period::last, "Return the last item in the period")
    .def("length", &bg::date_period::length, "Return the length of the period")
    .def("is_null", &bg::date_period::is_null, "True if period is ill formed (length is zero or less)")
    .def(self == self)
    .def(self != self)
    .def(self < self)
    .def(self > self)
    .def(self <= self)
    .def(self >= self)
    .def("shift", &bg::date_period::shift, "Shift the start and end by the specified amount")
    .def("contains", implicit_cast<bool(bg::date_period::*)(bg::date const&) const>(&bd::period<bg::date, bg::date_duration>::contains)
         , "True if the point is inside the period, zero length periods contain no points")
    .def("contains", implicit_cast<bool(bg::date_period::*)(bg::date_period const&) const>(&bd::period<bg::date, bg::date_duration>::contains)
         , "True if this period fully contains (or equals) the other period")
    .def("intersects", &bg::date_period::intersects, "True if the periods overlap in any way")
    .def("is_adjacent", &bg::date_period::is_adjacent, "True if periods are next to each other without a gap")
    .def("is_before", &bg::date_period::is_before, "True if all of the period is prior to the passed point or end <= t")
    .def("is_after", &bg::date_period::is_after, "True if all of the period is prior or t < start")
    .def("intersection", &bg::date_period::intersection, "Returns the period of intersection or invalid range no intersection")
    .def("merge", &bg::date_period::merge, "Returns the union of intersecting periods -- or null period")
    .def("span", &bg::date_period::span, "Combines two periods with earliest start and latest end")
    ;

  class_<std::vector<bg::date_period> >("date_period_vec", "vector (C++ std::vector<date_period> ) of date")
    .def(vector_indexing_suite<std::vector<bg::date_period> >())
    ;

  class_<year_based_generator_wrap, boost::noncopyable>("year_based_generator")
    .def("get_date", pure_virtual(&bd::year_based_generator<bg::date>::get_date))
    .def("to_string", pure_virtual(&bd::year_based_generator<bg::date>::to_string))
    ;

  class_<bg::partial_date, bases<bd::year_based_generator<bg::date> > >(
    "partial_date"
    , "Generates a date by applying the year to the given month and day.", init<bg::greg_day, bg::greg_month>())
    .def(init<long>("Partial date created from number of days into year."))
    .def(init<bg::partial_date const&>())
    .def("get_date", &bg::partial_date::get_date, "Return a concrete date when provided with a specific year")
    .def("__call__", &bg::partial_date::operator())
    .def(self < self)
    .def(self == self)
    .def("month", &bg::partial_date::month)
    .def("day", &bg::partial_date::day)
    .def("__str__", &bg::partial_date::to_string, "Returns a string suitable for use in POSIX time zone string")
    ;

  {
    scope nth_kday_of_month_scope =
      class_<bg::nth_kday_of_month>("nth_kday_of_month", "Useful generator for finding holidays", init<bg::nth_kday_of_month::week_num, bg::greg_weekday, bg::greg_month>())
      .def("get_date", &bg::nth_kday_of_month::get_date)
      .def("month", &bg::nth_kday_of_month::month)
      .def("nth_week", &bg::nth_kday_of_month::nth_week)      
      .def("day_of_week", &bg::nth_kday_of_month::day_of_week)
      .def("__str__", &bg::nth_kday_of_month::to_string)
      ;

    enum_<bg::nth_kday_of_month::week_num>("week_num")
      .value("first", bg::nth_kday_of_month::first)
      .value("second", bg::nth_kday_of_month::second)
      .value("third", bg::nth_kday_of_month::third)
      .value("fourth", bg::nth_kday_of_month::fourth)
      .export_values()
      ;
  }

  class_<bg::first_kday_of_month, bases<bd::year_based_generator<bg::date> > >(
    "first_kday_of_month"
    , "Useful generator functor for findning holidays and daylight savings", init<bg::greg_weekday, bg::greg_month>())
    .def("get_date", &bg::first_kday_of_month::get_date)
    .def("month", &bg::first_kday_of_month::month)
    .def("day_of_week", &bg::first_kday_of_month::day_of_week)
    ;

  class_<bg::last_kday_of_month, bases<bd::year_based_generator<bg::date> > >(
    "last_kday_of_month"
    , "Calculate something like last Sunday of January", init<bg::greg_weekday, bg::greg_month>())
    .def("get_date", &bg::last_kday_of_month::get_date)
    .def("month", &bg::last_kday_of_month::month)
    .def("day_of_week", &bg::last_kday_of_month::day_of_week)
    ;

  enum_<bd::date_resolutions>("date_resolutions")
    .value("day", bd::day)
    .value("week", bd::week)
    .value("months", bd::months)
    .value("year", bd::year)
    .value("decade", bd::decade)
    .value("century", bd::century)
    .value("NumDateResolutions", bd::NumDateResolutions)
    ;

  typedef bd::gregorian_calendar_base<
       bd::year_month_day_base<bg::greg_year, bg::greg_month, bg::greg_day>, unsigned long
         > gregorian_calendar_base;

  class_< gregorian_calendar_base > ("gregorian_calendar_base")
    .def("day_of_week", &gregorian_calendar_base::day_of_week)
    .def("week_number", &gregorian_calendar_base::week_number)
    .def("day_number", &gregorian_calendar_base::day_number)
    .def("julian_day_number", &gregorian_calendar_base::julian_day_number)
    .def("modjulian_day_number", &gregorian_calendar_base::modjulian_day_number)
    .def("from_day_number", &gregorian_calendar_base::from_day_number)
    .def("from_julian_day_number", &gregorian_calendar_base::from_julian_day_number)
    .def("from_modjulian_day_number", &gregorian_calendar_base::from_modjulian_day_number)
    .def("is_leap_year", &gregorian_calendar_base::is_leap_year)
    .def("end_of_month_day", &gregorian_calendar_base::end_of_month_day)
    .def("epoch", &gregorian_calendar_base::epoch)
    .def("days_in_week", &gregorian_calendar_base::days_in_week)
    .staticmethod("day_of_week")
    .staticmethod("week_number")
    .staticmethod("day_number")
    .staticmethod("julian_day_number")
    .staticmethod("modjulian_day_number")
    .staticmethod("from_day_number")
    .staticmethod("from_julian_day_number")
    .staticmethod("from_modjulian_day_number")
    .staticmethod("is_leap_year")
    .staticmethod("end_of_month_day")
    .staticmethod("epoch")
    .staticmethod("days_in_week")
    ;
}

}} // namespace ppf::date_time
