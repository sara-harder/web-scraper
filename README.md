# Web Scraper Microservice
Takes a URL for a Wikipedia page and returns all p children elements of the main body (class mw-parser-output) up until the first h2 element.

To start the service, the python file web_scraper.py must be run locally.

In order to request data from the service, connect to port 2007 using ZeroMQ. The code needed for port connection will vary depending on the language.
For JavaScript(Node.js) connection setup, use the following code, taken from https://zeromq.org/get-started/ :

      const zmq = require('zeromq');
      const socket = new zmq.Request();
      socket.connect('tcp://localhost:2007');
  

To send the request itself, send only a Wikipedia URL to the service. This can be done with the following line of code, where URL is replaced with the desired URL:

      await socket.send(b"URL");


In order to receive and parse the data after sending the request, simply use the following lines of code (for Javascript):

      const [result] = await socket.receive();
      const data = result.toString()
      
To receive the data in other languages, please refer to the ZMQ get started page: https://zeromq.org/get-started/

The following is a UML diagram describing this relationship:

![Screenshot 2023-05-03 at 9 01 37 PM](https://user-images.githubusercontent.com/91351068/236017480-a4847d80-573d-4ee5-af36-82835fd8cf08.png)
