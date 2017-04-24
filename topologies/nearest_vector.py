"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.NearestVectors import PairProcessBolt, VectorSumBolt, NearestBolt
from spouts.words import IndexSpout


class NearestVectors(Topology):
    vector_spout = IndexSpout.spec()
    index_bolt = PairProcessBolt.spec(inputs={vector_spout: Grouping.SHUFFLE},
                                    par=8)
    sum_bolt = VectorSumBolt.spec(inputs=index_bolt, group_on="vector_id",
                                    par=8)
    final_bolt = NearestBolt.spec(inputs={sum_bolt: Grouping.fields('final')},
                                    par=8)
