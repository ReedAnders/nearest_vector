import os
from collections import Counter
import requests
import json

import numpy as np

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

class VectorMapBolt(Bolt):
    outputs = ['pair', 'vector_id']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()

    def process(self, tup):
        vector = tup.values[0]
        vector_id = tup.values[1]
        query = tup.values[2]

        # self.logger.info("VECTOR MAP [{}]".format(vector_id))

        for index_id, pair in enumerate(zip(vector, query)):
            self.emit([pair, vector_id])

class PairProcessBolt(Bolt):
    outputs = ['pair', 'vector_id']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()

    def process(self, tup):
        pair = tup.values[0]
        vector_id = tup.values[1]

        pair = (pair[0]-pair[1])**2

        # self.logger.info("PAIRBOLT vector_id [{:,}]".format(vector_id))

        self.emit([pair, str(vector_id)])

class VectorSumBolt(Bolt):
    outputs = ['sum', 'vector_id','final']

    def initialize(self, conf, ctx):
        self.sum = Counter()
        self.total = Counter()
        self.pid = os.getpid()

    def _increment(self, tup, inc_by):
        self.sum[tup[1]] += tup[0]
        self.total[tup[1]] += inc_by

    def process(self, tup):

        self._increment((tup.values[0],tup.values[1]), 1)
        # self.logger.info("SUMBOLT vector_id [{},{}]".format(self.total[tup[1]] == 20,tup.values[1]))

        if self.total[tup.values[1]] == 20:
            self.emit([np.sqrt(self.sum[tup.values[1]]), str(tup.values[1]),'final'])

class NearestBolt(Bolt):
    outputs = ['nearest']

    def initialize(self, conf, ctx):
        self.nearest = []
        self.total = 0
        self.pid = os.getpid()

    def _increment(self, tup, inc_by):
        self.total += inc_by
        self.nearest.append(tup)
        self.nearest.sort(key=lambda x: x[0])

    def _increment_min(self, tup, inc_by):
        self.total += inc_by
        self.nearest[5] = tup
        self.nearest = self.nearest[:5]
        self.nearest.sort(key=lambda x: x[0])

    def _post_nearest(self):
        nearest_index = [x for (x,y) in self.nearest]
        msg_nearest = json.dumps(nearest_index)
        r = requests.post('http://127.0.0.1:5000/update', data = {'user':'A', 'vector':msg_nearest})
        self.logger.info("***************** Request {}".format(response.text))

    def process(self, tup):
        _sum = tup.values[0]
        _id = tup.values[1]

        if len(self.nearest) <= 6:
            self._increment((_sum,_id), 1)
        elif _sum < self.nearest[5]:
            self._increment_min((_sum,_id), 1)

        if self.total == 9:
            self.logger.info("NEAR_BOLT counted [{}] nearest [{}]".format(self.total,
                                                                self.nearest))
            # self._post_nearest()
            self.emit([self.nearest])

