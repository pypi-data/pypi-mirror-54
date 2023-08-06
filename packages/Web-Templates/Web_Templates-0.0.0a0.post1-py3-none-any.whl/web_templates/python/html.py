"""

.. note :: 

   Everything should really inherit a class called :class:`Element` a sort of analogue to `None`.
   The root element should be "hidden" and forms the document.
   The reason for this is that the DTD and HTML tags are siblings and need to have a parent that returns no content.

.. note ::

   Consider creating a :class:`Content` class for handling the text within an element.
   Naturally this should be an extention of :class:`str`.
"""
from .abc import TAG

class DTD(TAG) :
    """"""

class HTML(TAG) :
    """"""

class Head(TAG) :
    """"""

class Body(TAG) :
    """"""
    
class Nav(TAG) :
    """"""

class Main(TAG) :
    """"""

class Article(TAG) :
    """"""

class Div(TAG) :
    """"""

class Span(TAG) :
    """"""

class I(TAG) :
    """"""


