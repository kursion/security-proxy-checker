# proxy_checker
Small tool that takes a single proxy or a proxy list and check it. This tool is using threads
and queues to work as fast as possible.

**Requirement**: python2

# Usage
You can check the help by using the following command: `$ python2 proxy_checker.py`.
Or the accurate example below.

## ProxyChecker Help

```
$ python2 proxy_checker.py --help
usage: proxy_checker.py [-h] [-f INPUT] [-o OUTPUT] [-t TIMEOUT] [-u URL]
                        [ips [ips ...]]

positional arguments:
  ips                   An single proxy address to test, eg: 127.0.0.1:8080 or
                        multiple proxy address separated by space

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT, --input INPUT
                        Input file with proxies address
  -o OUTPUT, --output OUTPUT
                        Save working proxies to a specific file
  -t TIMEOUT, --timeout TIMEOUT
                        Socket timeout
  -u URL, --url URL     URL to test. Eg: http://www.google.com
```

## Examples
For every commands of `proxy_checker`. It will return `0` if every proxies address worked and `1` if
it didn't (POSIX convention).

### 1. Check if single proxy works:
* Command: `proxy_checker 127.0.0.1:80`.
* Description: This will test a simple proxy address.

### 2. Check if multiple proxy works:
* Command: `proxy_checker 127.0.0.1:81 127.0.0.2:81`.
* Description: This will test if both proxy addresses works.

### 3. Append working proxies to output file:
* Command: `proxy_checker -o working_proxies.txt 127.0.0.1:81 127.0.0.2:81`.
* Description: This will test if both proxy addresses works.
It will also append the proxies address that **works** into the output specified file.

### 4. Use an input file to test:
* Command: `proxy_checker -i proxies_to_test.txt `.
* Description: This will test if all proxy addresses from the input file `proxies_to_test.txt`.
The format of the file should be the following:
```
file: proxies_to_test.txt
##########################
123.0.0.1:80
127.0.0.1:81
8.8.8.8:1234
...
```

### 4. Use a input file to test, append working proxies to output file:
* Command: `proxy_checker -i proxies_to_test.txt -o working_proxies.txt`.
* Description: This will test if all proxy addresses from the input file `proxies_to_test.txt`.
It will also append the proxies address that **works** into the output specified file.

### Use it as a package
```python
import proxy_checker
proxiesToTest = ["213.321.413.1:8080", "413.333.321.12:81", ...]

# 1. with default options, just pass the proxies list
workingProxies = process(proxiesToTest)
print workingProxies                # a list of working proxies

# 2. optional arguments
timeout = 4                         # socket timeout in sec
url     = "http://www.yahoo.com"    # url used to test the proxy
output  = "working_proxies.txt"     # file to append working proxies
workingProxies = process(proxiesToTest, timeout, url, output)
print workingProxies                # a list of working proxies
```

# Author
Yves Lange
