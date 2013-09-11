import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import re

from tornado.options import define, options
from tornado import gen

#use BEncode Editor change torrent tracker you server
#ex. http://111.195.165.131:18888/announce

#your server tracker
tracker = "http://hdcmct.org/announce.php"
#your account passkey
passkey = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#change 20 length id for yourself ex.'-UT3200-fktihngkqfsk'
peer_id = "-UT3200-abcdefghijkl"
#change 8 length Hex key for youself ex.'E2B654A1'
key = "AAAAAAAA"
listen_port = 18888

@gen.coroutine
def handle_request(request):
    uri = request.uri
    if(uri.find('/announce?') == -1):
        ret = 'It\'s work!'
        request.write('HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (
            len(ret), ret)
        )
        
    uri = '?passkey=' + passkey + '&' + uri.replace('/announce?','').replace('/?','')

    result = re.findall('peer_id=.*?&', uri)
    if result :
        uri = uri.replace(result[0], 'peer_id=' + peer_id + '&')

    result = re.findall('&key=.*?&', uri)
    if result :
        uri = uri.replace(result[0], '&key=' + key + '&')

    http_client = tornado.httpclient.AsyncHTTPClient()
    req = tornado.httpclient.HTTPRequest(tracker + uri, user_agent = "uTorrent/3200")

    try:
        res = yield http_client.fetch(req)
        request.write('HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (
            len(res.body), res.body)
        )
    except tornado.httpclient.HTTPError, code:
        print 'HTTPError except Code' + str(code)
        msg = 'NexusPHP Return a Error Code :' + str(code)
        ret = 'd14:failure reason' + str(len(msg)) + ':' + msg + 'e'
        request.write('HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (
            len(ret), ret)
        )
    finally:
        #http_client.close()
        request.finish()
        
    print "Request:" + "\r\n" + request.uri + "\r\n"
    print "Request Re:" + "\r\n" + uri + "\r\n" + "========================"

def main():

    http_server = tornado.httpserver.HTTPServer(handle_request)
    http_server.listen(listen_port)
    
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
