import numpy as np
from streamparse import Spout


class IndexSpout(Spout):
    outputs = ['vector', 'vector_id', 'query']

    def initialize(self, stormconf, context):
        self.query = np.random.rand(20,)
        self.matrix = ((x,y) for (x,y) in enumerate(np.random.rand(10,20)))

    def next_tuple(self):
        try:
            vector = next(self.matrix)

            self.logger.info("vector id [{:,}]".format(vector[0]))
            self.emit([vector[1], vector[0], self.query])
        except:
            pass
