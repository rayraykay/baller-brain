Updates:
- January 20, 2017
I can get the data matrix now for the simple features I have! Time to feed it into the algorithm.


To run this program, you need a conventional installation of Python 2 with tkinter, and the external libraries numpy, scipy, and matplotlib. I would've written this in Python 3, but UofT ECE really hates upgrading :((

Musings:
- January 20, 2017
I need to clean up this code after the hackathon I'm making this for. In particular, I could wrap the data scrapper and machine learning algorithm into separate classes, and I can have instance variables in each that can determine exactly what the capabilities can be (ex. the data scrapper class could have modular capabilities that include being able to add special features) and encapsulate the spaghetti functions I've written into a nicer framework
