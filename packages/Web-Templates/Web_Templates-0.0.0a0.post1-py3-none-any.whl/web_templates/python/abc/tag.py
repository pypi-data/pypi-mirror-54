class TAG() :
    """

    ::
        >>> tag = TAG()
        >>> f"{tag}"
        <tag>{tag}</tag>
        >>> f"{tag:f}"
        <tag/>
        >>> tag = tag/tag
        >>> f"{tag}"
        <tag><tag>{tag}</tag></tag>
        >>> f"{tag:f}"
        <tag><tag></tag></tag>
        >>> f"{tag:v}"
        <tag>
           <tag>
           </tag>
        </tag>
    """
    __root__ = None
    __fold__   = False # <TAG></TAG> versus <TAG/>
    __data__   = []
    def __opening__(self):
        return f"<{self.__class__.__name__}>"
    def __closing__(self):
        return f"</{self.__class__.__name__}>"
    def _data_(self, spec):
        return str(self.__data__)
    def __format__(self, spec):
        dent = "    " * len(self.parents()) # TODO : This is not working at the moment.
        if spec :
            return { "h" : self.__opening__() + "{" + self.__class__.__name__ + ":" + spec + "}" + self.__closing__(),
                     "v" : dent + self.__opening__() + "\n" + "{" + self.__class__.__name__ + ":" + spec + "}" + "\n" + self.__closing__() }[spec]
        return str(self)
    def __str__(self):
        return f"{self:v}".format(**{self.__class__.__name__ : self})# **{self.__class__.__name__ : "\n".join(f"{item}" if isinstance(item, TAG) else str(item) for item in self.__data__)})
    def __floordiv__(self, item):
        types = {str : lambda item : item,
                 TAG : lambda item : self.__data__ + [item] if isinstance(self.__data__, list) else [item]}
        try :
            # TODO : Test that the item has no parent; should it do so remove itself as a child and re-assign it or error out accordingly.
            self.__data__ = types[type(item)](item)
            item.__root__ = self
            return self
        except KeyError as error :
            raise ValueError("The operator only works with other instances of tag or string ") from error
    def parents(self) :
        items = []
        item = self
        while item.__root__ :
            item += item.__root__
            item = item.__root__
        return items

class HTML_TAG(TAG) :
    """"""

class XML_TAG(TAG) :
    """"""
if __name__ == "__main__" :
    t = TAG()//TAG()
    print(f"{t}")