from urllib2 import urlopen


DEBUG = True


def http_200_response(addr, url, timeout=1):
    try:
        code = urlopen(
            url,
            timeout=timeout).getcode()
        return True if code == 200 else False
    except:
        return False


def http_any_response(addr, url, timeout=1):
    try:
        urlopen(
            url,
            timeout=timeout)
        return True
    except:
        return False
