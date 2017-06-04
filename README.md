# Intsights-Project #

This Project is a simple web crawler built in python language.
This crawler will crawl a site that is a part of an"onion network", take information from site and store it on a database.
The Crawler will run automatically every 4 hours and try to update the database with new information.



# Getting Started #
You should follow these instructions for installing the project. Enjoy (:
 
### Prerequisites ###
Before downloading all libraries needed for this project - you should have python3 installed on your computer.
You can download python3 from here: https://www.python.org/

Also, you need to download docker to your computer for using container that will fetch .onion sites:
  - Windows docker - https://docs.docker.com/docker-for-windows/
  - Linux docker  - https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository
  - Docker for mac - https://docs.docker.com/docker-for-mac/

After that, you need to get the following libraries:
  - lxml
  - tinyDB
  - arrow
  - requests
  - PySocks
 
You can install them by going to command line and enter the following command:

  - pip install XXX (XXX represent name of library)




### Installing the project ###
Installing the project is simple and fun!

First of all , you should run your docker (after installing it) by typing in the command line (for Linux\OSX) or Powershell (for windows): 
  - Linux\OSX:   sudo docker run -it -p 8118:8118 -p 9050:9050 -d dperson/torproxy
  - Windows: docker run -it -p 8118:8118 -p 9050:9050 -d dperson/torproxy
 
This command will execute a non-caching web proxy with advanced filtering capabilities.



After that, all you have to do is to clone the project, go to command line , get into the  specific directory of the project  and enter:
  - python main.py
  
    
That's all!


### Built with ###
  - TinyDB - noSQL database  - more information on http://tinydb.readthedocs.io/en/latest/
  - lxml - Processing XML and HTML with Python -  more information on http://lxml.de/
  - arrows - Python library for date and time - more information on http://arrow.readthedocs.io/en/latest/
  - cssselect - cssselect parses CSS3 Selectors and translates them to XPath 1.0 - more information on https://pypi.python.org/pypi/cssselect
  
## Author ##
 Ori Feinshreiber - Python Developer

## Contribution ##

You can contribute my bank account - that's always good (:
