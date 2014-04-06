"""PPF package setup script

   To create a source distribution of the PPF
   package run

   python setup.py sdist

   which will create an archive file in the 'dist' subdirectory.
   The archive file will be  called 'ppf-1.0.zip' and will
   unpack into a directory 'ppf-1.0'.
   
   An end-user wishing to install the PPF package can simply
   unpack 'ppf-1.0.zip' and from the 'ppf-1.0' directory and
   run

   python setup.py install

   which will ultimately copy the PPF package to the approriate
   directory for 3rd party modules in their Python installation
   (somewhere like 'c:\python25\libs\site-packages').

   To create an executable installer use the bdist_wininst command

   python setup.py bdist_wininst

   which will create an exectuable installer, 'ppf-1.0.win32.exe',
   in the current directory.
   
"""

from distutils.core import setup

setup(
      name="ppf"
    , version="1.0"
    , description="'ppf' package"
    , author="S. Fletcher & C. Gardner"
    , author_email=""
    , maintainer="S. Fletcher"
    , maintainer_email=""
    , long_description="'ppf' package and extensions\n"
    , packages=['ppf'
               ,'ppf.model'
               ,'ppf.model.hull_white'
               ,'ppf.model.hull_white.lattice'
               ,'ppf.model.hull_white.monte_carlo'
               ,'ppf.pricer'
               ,'ppf.pricer.payoffs'
               ,'ppf.core'
               ,'ppf.market'
               ,'ppf.date_time'
               ,'ppf.math'
               ,'ppf.utility'
               ,'ppf.test'
               ,'ppf.com']
    , package_dir={'ppf.math':'ppf/math', 'ppf.date_time':'ppf/date_time'}
    , package_data={'ppf.math':['ppf_math.pyd', 'ppf_math.so']
                  , 'ppf.date_time':['ppf_date_time.pyd', 'ppf_date_time.so']}
    )

