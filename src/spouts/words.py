import numpy as np
from streamparse import Spout


class IndexSpout(Spout):
    outputs = ['pair', 'vector_id']

    def initialize(self, stormconf, context):
        self.query = np.random.rand(20,)
        self.matrix = ((x,y) for (x,y) in enumerate(np.random.rand(10,20)))

    def next_tuple(self):
        try:
            vector = next(self.matrix)

            for index_id, pair in enumerate(zip(vector[1], self.query)):
                self.emit([pair, vector[0]])

            self.logger.info("vector id [{:,}]".format(vector[0]))
        except:
            pass
