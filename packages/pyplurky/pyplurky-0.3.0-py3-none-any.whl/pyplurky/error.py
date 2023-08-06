# coding=utf-8


class PlurkyError(Exception):
    def __init__(self, message):
        super(PlurkyError, self).__init__()
        self.message = message

    def __str__(self):
        return '%s' % (self.message)
