To run this program, you need a conventional installation of Python 2 with tkinter, and the external libraries numpy, scipy, and matplotlib. I would've written this in Python 3, but UofT ECE really hates upgrading :((

Much special thanks to Erick Zhang, Alex Lee, and Jenna Ren from the University of Toronto for their love and support, and maybe for helping me use the MySportsFeeds API. That was definitely the most tedious part. Keep on shining.

Updates:
- January 20, 2017
It functions!! Now we have to add some more features and work on cleaning up the code, specifically:
-Adding more error checking
-Wrapping everything in nice classes so that getting data and feeding into the algorithm and getting results is easier
-Adding compatibility for Python 3

Musings:
- January 20, 2017
I need to clean up this code after the hackathon I'm making this for. In particular, I could wrap the data scrapper and machine learning algorithm into separate classes, and I can have instance variables in each that can determine exactly what the capabilities can be (ex. the data scrapper class could have modular capabilities that include being able to add special features) and encapsulate the spaghetti functions I've written into a nicer framework

Installation Notes:
- June 13, 2018
Requires numpy, scipy, matplotlib, and requests packages
