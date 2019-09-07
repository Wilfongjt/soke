class CloudBase():
    def __init__(self, settings=None):
        self.settings=settings

    def getClassName(self):
        return self.__class__.__name__

    def get_settings(self):
        return self.settings

    def connect(self):
        raise Exception('Initialize connect in {}'.format(self.getClassName()))
        return self