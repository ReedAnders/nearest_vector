import os
from collections import Counter

from streamparse import Bolt


# class NearestVectorsBolt(Bolt):
#     outputs = ['word', 'count']

#     def initialize(self, conf, ctx):
#         self.counter = Counter()
#         self.pid = os.getpid()
#         self.total = 0

#     def _increment(self, word, inc_by):
#         self.counter[word] += inc_by
#         self.total += inc_by

#     def process(self, tup):
#         word = tup.values[0]
#         self._increment(word, 10 if word == "dog" else 1)
#         if self.total % 1000 == 0:
#             self.logger.info("counted [{:,}] words [pid={}]".format(self.total,
#                                                                     self.pid))
#         self.emit([word, self.counter[word]])

class PairProcessBolt(Bolt):
    outputs = ['pair', 'vector_id']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()

    def process(self, tup):
        pair = tup.values[0]
        vector_id = tup.values[1]

        pair = (pair[0]-pair[1])**2

        self.logger.info("PAIRBOLT vector_id [{:,}]".format(vector_id))

        self.emit([pair, str(vector_id)])

class VectorSumBolt(Bolt):
    outputs = ['sum', 'vector_id','final']

    def initialize(self, conf, ctx):
        self.sum = 0
        self.total = 0
        self.pid = os.getpid()

    def process(self, tup):
        self.sum =+ tup.values[0]
        self.total =+ 1

        self.logger.info("SUMBOLT vector_id [{}]".format(self.total))

        if self.total == 20:
            self.sum = np.sqrt(self.sum)
            self.emit([self.sum, str(tup.values[1]),'final'])

class NearestBolt(Bolt):
    outputs = ['nearest']

    def initialize(self, conf, ctx):
        self.nearest = []
        self.total = 0
        self.pid = os.getpid()

    def process(self, tup):
        _sum = tup.values[0]
        _id = tup.values[1]
        self.total =+ 1

        if len(self.nearest) <= 6:
            self.nearest.append((_sum,_id))
            self.nearest.sort(key=lambda x: x[0])
        elif _sum < self.nearest[5]:
            self.nearest[5] = (_sum, _id)
            self.nearest.sort(key=lambda x: x[0])

        if self.total % 1000 == 0:
            self.logger.info("counted [{:,}] nearest [{}]".format(self.total,
                                                                self.nearest))

        if self.total == 10000:
            self.emit([self.nearest])

