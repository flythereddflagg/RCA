class DictObj(dict):
    """
    Lets an object be treated like a dictionary.
    ******NOTICE***************
    optimize.py module by Travis E. Oliphant
    
    You may copy and use this module as you see fit with no
    guarantee implied provided you keep this notice in all copies.
    *****END NOTICE************
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '{\n' + '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])+"\n}"
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())
