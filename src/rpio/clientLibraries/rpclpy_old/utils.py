class LogMessage(object):
    def __init__(self,name='tbd',message="tbd"):

        self._name = name
        self._message= message

    @property
    def name(self):
        """The name (read-only)."""
        return self._name

    @name.setter
    def name(self, cmp):
        """The ID (write)."""
        self._name = cmp

    @property
    def message(self):
        """The message (read-only)."""
        return self._message

    @message.setter
    def message(self, cmp):
        """The message (write)."""
        self._message = cmp

    def instantiate(self,decodedJSON):                  #TODO: this initialize function needs to be generalized to use custom classes
        self._name = decodedJSON._name
        self._message = decodedJSON._message