from firebase import Firebase

class FirebaseReport(object):

    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process(self, spider):
        pass


class XmlReport(object):
    pass