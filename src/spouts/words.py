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

            if vector[0] == 0:
                self.logger.info("SPOUT vector [{}]".format(vector[0]))

            self.emit([list(vector[1]), vector[0], list(self.query)])
        except:
            pass
