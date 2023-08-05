JUNKYARD

A collection of various helper classes and modules designed by the author for use by the author, using PyCharm and
Anaconda (Python 3.7.#).

to install junkyard with pip:
`"pip install junkyard"`

to import junkyard into your python script:
`"import junkyard.garbagebasket as junkyard"`

--

Current features include:

 FileHandler(WIP)
 An attempt at leveraging standard library modules to accomplish routine filesystem tasks in a safe, reliable, 
 and modular manner. 
 
 example usage:
     
     import junkyard.garbagebasket as junkyard
          
     fh = junkyard.FileHandler()
     filename = 'data/bob.txt
     fh.read(filename)