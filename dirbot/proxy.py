import random
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        fd = open('ip.txt','r')
        data = fd.readlines()
        fd.close()
        length = len(data)
        index  = random.randint(0, length -1)
        item = data[index].strip('\n').strip(' ')
        arr = item.split(':')
        request.meta['proxy'] = 'http://%s:%s' % (arr[0],arr[1])