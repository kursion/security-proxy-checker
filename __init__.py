#!/bin/python2
import proxy_checker
__all__ = ["proxy_checker"]


def process(proxiesToTest,
            timeout,
            url,
            output):
    proxy_checker.process(proxiesToTest, timeout, url, output)

if __name__ == "__main__":
    print "Please run proxy_checker.py --help"
