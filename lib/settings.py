import json
import random
import methods
import threading
from datetime import datetime
from time import sleep
DEBUG = False


class Settings:
    stats = {}
    statistics = {}
    LASTCHECK = datetime.now()

    def __init__(self, confpath="pool.json", workers=5):
        self.WORKERS = workers
        with open(confpath, "rb+") as fp:
            self.conf = json.loads(fp.read())

            for key in self.conf.keys():
                self.stats[key] = [x["addr"] for x in self.conf[key]["NODES"]]

    def poolUpdateNodes(self, poolname):
        isup = []
        if poolname not in self.conf.keys():
            return 0

        pool = self.conf[poolname]
        method = getattr(methods, pool["method"])

        for node in pool["NODES"]:
            if method(**node):
                if DEBUG:
                    print node["addr"]+" is up."
                isup.append(node["addr"])
            else:
                if DEBUG:
                    print node["addr"]+" is up."

        self.stats[poolname] = isup

        print isup
        return len(isup)

    def updateAllPools(self):
        for key in self.conf.keys():
            self.poolUpdateNodes(key)

    def updatePollsForever(self):
        while True:
            self.updateAllPools()
            sleep(1)
            self.LASTCHECK = datetime.now()
            if DEBUG:
                print "Check at "+str(self.LASTCHECK)

    def resolve(self, name):
        try:
            addr = random.choice(self.stats[name])
            if name not in self.statistics.keys():
                self.statistics[name] = {}
            if addr not in self.statistics[name]:
                self.statistics[name][addr] = 0
            self.statistics[name][addr] += 1
            return addr
        except KeyError:
            return None

    def run_async_checks(self):
        worker = threading.Thread(target=self.updatePollsForever)
        worker.daemon = True
        worker.start()
