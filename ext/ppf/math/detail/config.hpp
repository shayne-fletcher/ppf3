#if !defined(CONFIG_596ABE7F_F7AD_4F6B_A6E3_63EEB03232FC_INCLUDED)
#  define CONFIG_596ABE7F_F7AD_4F6B_A6E3_63EEB03232FC_INCLUDED

#  if defined(_MSC_VER) && (_MSC_VER >= 1020)
#    pragma once
#  endif // defined(_MSC_VER) && (_MSC_VER >= 1020)

#  if defined(PPF_MATH_DYNAMIC_LIB)
#    if defined(_WIN32) || defined(__CYGWIN__)
#      if defined(PPF_MATH_SOURCE)
#        define PPF_MATH_DECL __declspec(dllexport)
#      else
#        define PPF_MATH_DECL __declspec(dllimport)
#      endif // defined(PPF_MATH_SOURCE)
#    endif // defined(_WIN32)
#  endif // defined(PPF_MATH_DYNAMIC_LIB)

#  if !defined(PPF_MATH_DECL)
#    define PPF_MATH_DECL
#  endif // !defined(PPF_MATH_DECL)

#endif // !defined(CONFIG_596ABE7F_F7AD_4F6B_A6E3_63EEB03232FC_INCLUDED)
