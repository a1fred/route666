from lib.settings import Settings
from os import getcwd
from lib.dnslib import BindServer

VERSION = "0.1a"


def main():
    conf = Settings(getcwd()+"/pool.json")
    conf.run_async_checks()
    BindServer(ip='10.20.30.53', resolver=conf.resolve)


if __name__ == '__main__':
    main()
