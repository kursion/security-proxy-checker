import py_console.colors as console
import signal
import sys
import time
import urllib2
import socket
import threading
from Queue import *


class ProxyChecker:
    workingProxies = []  # Care shared object need lock
    queueProxies = None
    __lockPrint = threading.RLock()
    __lockWorkingProxies = threading.RLock()
    CONFIG = {}

    def __init__(self,
                 proxies,
                 timeout=10,
                 url_test="http://www.google.com",
                 output=None):
        socket.setdefaulttimeout(timeout)
        self.queueProxies = Queue()
        self.CONFIG["timeout"] = timeout
        self.CONFIG["url_test"] = url_test
        self.CONFIG["output"] = output
        self.initQueue(proxies)
        self.startWorkers()

    def getProxies(self):
        return self.workingProxies

    def safe_print(self, msg):
        self.__lockPrint.acquire()
        print(msg)
        sys.stdout.flush()
        self.__lockPrint.release()

    def initQueue(self, proxies):
        for proxy in proxies:
            self.queueProxies.put(proxy)

    def getNextProxy(self):
        return self.queueProxies.get()

    def startWorkers(self):
        nbr_workers = self.queueProxies.qsize()/3 or 1
        self.safe_print("%i thread will be launched" % nbr_workers)
        for workerID in range(1, nbr_workers+1):
            t = threading.Thread(target=self.proxyWorker, args=[workerID])
            t.daemon = True
            t.start()
        self.queueProxies.join()

    def proxyWorker(self, workerID):
        self.safe_print("Worker %i launched." % workerID)
        while True:
            proxy = self.getNextProxy()
            remaining = self.queueProxies.qsize()
            self.safe_print("Worker %i testing: %s (remaining %i)"
                            % (workerID, proxy, remaining))
            proxyOK = self.checkProxy(proxy)
            if proxyOK:
                self.safe_print("Proxy %s worked !!!!" % proxy)
                self.appendWorkingProxy(proxy)
            self.queueProxies.task_done()

    def appendWorkingProxy(self, proxy):
        self.__lockWorkingProxies.acquire()
        self.workingProxies.append(proxy)
        self.__lockWorkingProxies.release()

    # check if the proxy is working
    # NOTE: HTTPS doesn't seems to work
    def checkProxy(self, proxy):
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req = urllib2.Request(self.CONFIG["url_test"])
            urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            # errorMsg = ('Error code: %i' % e.code)
            proxyOK = False
        except Exception, detail:
            # errorMsg = ('ERROR: %s' % detail)
            return False
        return True

    def saveFile(self):
        file = open(self.CONFIG["output"], "a+")
        for currentProxy in self.workingProxies:
            file.write(currentProxy+"\n")
        file.close()


def process(proxies, timeout, url_test, output):
    proxyChecker = ProxyChecker(proxies, timeout, url_test, output)
    workingProxies = proxyChecker.getProxies()
    print("Done. %i proxies are working out of %i" %
          (len(workingProxies), len(proxies)))
    if len(workingProxies) > 0 and output is not None:
        workingProxies.saveFile()
    return workingProxies


def checkProxyAddressFormat(addr):
    if len(addr.split(":")) != 2:
        return False
    return True

if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("ips",
                        help="An single proxy address to test, eg: 127.0.0.1:8080 \
                        or multiple proxy address separated by space",
                        nargs='*')
    parser.add_argument("-f", "--input",
                        help="Input file with proxies address")
    parser.add_argument("-o", "--output",
                        help="Save working proxies to a specific file")
    parser.add_argument("-t", "--timeout",
                        help="Socket timeout", type=int, default=10)
    parser.add_argument("-u", "--url",
                        help="URL to test. Eg: http://www.google.com",
                        default="http://www.google.com")
    args = parser.parse_args()

    if len(args.ips) == 0 and args.input is None:
        print "invalid arguments. " + \
            "Please specify at least an ip or an input file. Example:\n" + \
            "$ proxy_checker 127.0.0.1:8080\n" + \
            "$ proxy_checker 127.0.0.1:81 127.0.0.2:82\n" + \
            "$ proxy_checker -f proxies_to_test.txt\n" + \
            "$ proxy_checker -f proxies_to_test.txt -o result.txt\n" + \
            "or use proxy_checker --help to see all possible options"
        sys.exit(1)

    proxiesToTest = []

    if len(args.ips) > 0:
        proxiesToTest = args.ips

    if args.input is not None:
        try:
            proxiesFromFile = open(args.input, "r").readlines()
        except:
            print "Input file %s doesn't exists. Ignoring..." % args.input
            sys.exit(2)
        for i, proxy in enumerate(proxiesFromFile):
            proxy = proxy.strip()
            if proxy == "":
                print "Ignored empty line %i (file %s)" % (i+1, args.input)
            elif not checkProxyAddressFormat(proxy):
                print "Bad address line %i of file %s" % (i+1, args.input)
            else:
                proxiesToTest.append(proxy)

    lenProxiesToTest = len(proxiesToTest)
    if lenProxiesToTest == 0:
        print "Nothing to do... :("
        sys.exit(1)
    print "%i proxies to check" % lenProxiesToTest
    proxiesToTest = proxiesToTest[:1]  # TODO: remove me
    workingProxies = process(proxiesToTest,
                             args.timeout,
                             args.url,
                             args.output)

    if len(proxiesToTest) == len(workingProxies):
        sys.exit(0)
    else:
        sys.exit(1)
