# file for RCA exception class to report errors in the RCA config and other
# errors specific to RCA



class RCAException(Exception):
    def __init__(self, message):
        self.message = message