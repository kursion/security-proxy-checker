#!/bin/python2
import proxy_checker
__all__ = ["proxy_checker"]


def process(proxiesToTest,
            timeout=10,
            url="http://www.google.com",
            output=None):
    proxyChecker = proxy_checker.process(proxiesToTest, timeout, url, output)
    return proxyChecker

if __name__ == "__main__":
    print "Please run proxy_checker.py --help"
