# CoronaBook

CoronaBook is a Python script that automatically 
creates a book from a set of data, in this case the total deaths 
from COVID-19 reported in the first year of the pandemic. By converting
this raw data into a tangible physical object, it is hoped that some sense
of the enormity of the tragedy will be conveyed.

This is a work of art that is intended as an explicit indictment of the UK
government's handling of this disaster.

---

### Instructions

##### Parser Arguments:

**-l, --log** - Causes the program to create a log file   
**-nd, --nodownload** - Causes the program not to download a new dataset from
coronavirus.gov.uk     
**-u, --user** - Causes the program to use the user-defined config settings as
opposed to the default

##### Config Settings:

*data_source* : Controls where in the coronavirus.gov.uk API the data 
is downloaded from    
*log_length* : The length to which the log filenames are padded    
*mode* : Controls the program mode. '1year' creates a book for the first year
of the pandemic, whilst 'total' creates a book up to the latest available date.

---

### Version history

**0.1**: Creation of PNG files for the body of the book 
working correctly. Logging and terminal under way.   
**0.1.1**: Minor bug fixes, added font licensing info.

---

##### Appendix 1: Dependencies

CoronaBook uses the argparse, configparser, csv, errno, os, requests, sys, 
PILlow and datetime Python modules. Written in Python 3.8.2

##### Appendix 2: Assets

The font 'Crimson' is Copyright (c) 2010, Sebastian Kosch (sebastian@aldusleaf.org), 
with Reserved Font Name “Crimson Text”.

This Font Software is licensed under the SIL Open Font License, Version 1.1.
