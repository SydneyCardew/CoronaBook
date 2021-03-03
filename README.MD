# CoronaBook
*by Sydney Cardew*

CoronaBook is a Python script that automatically 
creates a printable book from a set of data, in this case the total deaths 
from COVID-19 reported in the first year of the pandemic in the UK. By converting
this raw data into a tangible physical object it is hoped that some sense
of the enormity of the tragedy will be conveyed, that the intangible will be 
reified.

This is a work of art that is intended as an explicit indictment of the UK
government's handling of this disaster. It builds on Keith A. Smith's idea
of the 'conceptual book'; in Smith's case this was a set of written instructions
to create a book that would be difficult or highly impractical to make real,
such as a bound copy of every single frame of *Fantasia*. In this case, the
instructions are written in computer code and result in a PDF which should be
ready to be printed through any variety of on-demand services.

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

**0.1.0**: Creation of PNG files for the body of the book 
working correctly. Logging and terminal under way.   
**0.1.1**: Minor bug fixes, added font licensing info.    
**0.2.0**: Front and back matter generation.
**0.2.1**: Expanded README, some small tweaks.

---

##### Appendix 1: Dependencies

CoronaBook uses the argparse, configparser, csv, errno, os, requests, sys, 
PILlow and datetime Python modules. Written in Python 3.8.2

##### Appendix 2: Assets and Utilities

The font 'Crimson' is Copyright (c) 2010, Sebastian Kosch (sebastian@aldusleaf.org), 
with Reserved Font Name “Crimson Text”.

This Font Software is licensed under the SIL Open Font License, Version 1.1.

This project was written in the PyCharm IDE; iconography and layouts were created
with the Adobe Creative Suite.