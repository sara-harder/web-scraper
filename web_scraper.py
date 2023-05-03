# web-scraper source: https://realpython.com/beautiful-soup-web-scraper-python/
# This web-scraper receives a ZMQ request for a URL, and searches for specific
# child elements up to a certain element

import zmq
import requests
from bs4 import BeautifulSoup

# socket connection for ZMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2007")

while True:
    # awaits request on socket with a URL
    URL = socket.recv()
    URL = URL.decode("utf-8")
    print(f"Received request: {URL}")

    # establishes properties for the parent tag, end tag, and target tag
    p_tag = {"elem": "div",
             "id": None,
             "class": "mw-parser-output"}
    e_tag = {"elem": "h2",
             "id": None,
             "class": None}
    t_tag = {"elem": "p",
             "class": None}

    # retrieves the data from the URL and parses it
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # if no attributes are specified for parent, sends an error
    if p_tag["elem"] is None and p_tag["id"] is None and p_tag["class"] is None:
        socket.send(bytes("Please specify a type, an id, or a class to locate the element to search in", "utf-8"))
        continue

    # finds the parent element using soup.find and an attribute of the parent
    parents = soup.find_all(p_tag["elem"], id=p_tag["id"], class_=p_tag["class"])

    # if no attributes are specified for end, end = None
    end = None

    if e_tag["elem"] is not None or e_tag["id"] is not None or e_tag["class"] is not None:
        # finds the end element using soup.find and an attribute of the end
        for parent in parents:
            e = parent.find(e_tag["elem"], id=e_tag["id"], class_=e_tag["class"])

            # in the case of multiple parents, only one should have the desired child
            if e is not None and end is None:
                end = e
            elif e is not None:
                socket.send(bytes("Multiple parents have this type of end child. Please specify further info", "utf-8"))
                continue

    # if no end elem was found or specified, uses all children with target attributes
    if end is None:
        target = []
        for parent in parents:
            # if no attributes are specified, children = all of parent's children
            children = parent.find_all(t_tag["elem"], class_=t_tag["class"])

            for child in children:
                target.append(child)

    # if an end elem was found and specified, locates all of its previous siblings with target attributes
    else:
        # if no attributes are specified, siblings = all of end's previous siblings
        siblings = end.find_previous_siblings(t_tag["elem"], class_=t_tag["class"])
        target = reversed(siblings)

    # creates a string to return with all the located info, excluding citations and extras
    string = ""
    for elem in target:
        citations = elem.find_all("sup")
        for cit in citations:
            cit.extract()
        extras = elem.find_all(class_="haudio")
        for xtr in extras:
            p = xtr.find_parent()
            p.extract()
        string += elem.text

    # removes any leading or ending newline / space chars, for consistency
    string = string.strip()

    socket.send(bytes(string, "utf-8"))
