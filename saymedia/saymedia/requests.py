from scrapy.http import Request

class PageRequest(Request):
    pass

class AssetRequest(Request):
    def __init__(self, *args, **kwargs):
        kwargs['method'] = 'HEAD'
        super(AssetRequest, self).__init__(*args, **kwargs)