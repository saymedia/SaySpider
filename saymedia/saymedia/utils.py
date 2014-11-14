import hashlib
import time

def Throttle(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait <= 0:
	            ret = func(*args,**kargs)
	            lastTimeCalled[0] = time.clock()
	            return ret
        return rateLimitedFunction
    return decorate

def url_hash(url):
    return hashlib.sha256(url).hexdigest()