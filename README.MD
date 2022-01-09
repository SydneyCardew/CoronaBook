# CoronaBook
### Second Edition
*by Sydney Cardew*

CoronaBook is a Python script that automatically 
creates a printable book called 'The Tally' from a set of data, in this case 
the total deaths from COVID-19 reported in the first two years of the ongoing
pandemic in the UK. By converting this raw data into a tangible physical 
object it is hoped that some sense of the enormity of the tragedy will be 
conveyed, that the intangible will be reified.

The fact that a second edition of this work is called for is a catastrophe.

This is a work of art that is intended as an explicit indictment of the UK
government's handling of this disaster. It builds on Keith A. Smith's idea
of the 'conceptual book'; in Smith's case this was a set of written instructions
to create a book that would be difficult or highly impractical to make real,
such as a bound copy of every single frame of *Fantasia*. In this case, the
instructions are written in computer code and result in a PDF which should be
ready to be printed through any variety of on-demand services. If you wish to
print your own copy you should run the program in '-ni' ('no isbn') mode, as
the ISBN is specifically registered to the artist for sale of the book through
lulu.com. You may buy an 'official' copy of the first edition here:

https://www.lulu.com/en/gb/shop/sydney-cardew/the-tally/paperback/product-yrj5gy.html

A Second Edition of *The Tally* will be published to commemorate the second anniversary
of the pandemic on the 2nd of March 2022.

Though the book contains a standard copyright notice, explicit permission is
given here to print copies of the book for personal use or display, providing 
the ISBN number is NOT included.

###

If you would like to support me less extravagantly, buy me a coffee:

https://ko-fi.com/sydneycardew

---

### Instructions for Use

CoronaBook is a Python script and requires a working installation of Python 3.8.2
to run. It is recommended that you run CoronaBook from the command line.

#### Parser Arguments:

**-ct, --covertest** - Runs the program in a test mode that *only* generates a 
cover in the root directory.  
   
**-l, --log** - Causes the program to create a log file, which is stored in the
/Logs/ directory   

**-nc, --nocover** - Causes the program to run without creating a cover pdf   

**-nd, --nodownload** - Causes the program not to download a new dataset from
coronavirus.gov.uk     

**-ni, --noisbn** - Causes the program to generate a version of the book with
no isbn information, essential if you plan on printing your own copy of the book

**-u, --user** - Causes the program to use the user-defined config settings as
opposed to the default

---

#### Config Settings:

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
**0.2.2**: Further tweaks, prototyping PDF maker function.     
**0.5.0**: PDF maker function working, further refinements.    
**1.0.0**: Full generation of internal matter and cover with ISBN number.    
**1.1.0**: Refactored code, re-worked to add a new '2 year' mode in preparation
for the second edition of The Tally.

---

##### Appendix 1: Dependencies

CoronaBook uses the argparse, configparser, csv, errno, os, requests, sys, 
PILlow, fpdf and datetime Python modules. It is written in Python 3.8.2

##### Appendix 2: Assets and Utilities

The font 'Crimson' is Copyright (c) 2010, Sebastian Kosch 
(sebastian@aldusleaf.org), with Reserved Font Name “Crimson Text”.

This Font Software is licensed under the SIL Open Font License, Version 1.1.

A full copy of the license is included as Assets/Fonts/License.txt

This project was written in the PyCharm IDE; iconography and layouts 
were created with the Adobe Creative Suite.