"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.NearestVectors import NearestVectorsBolt
from spouts.words import VectorSpout


class NearestVectors(Topology):
    vector_spout = VectorSpout.spec()
    count_bolt = NearestVectorsBolt.spec(inputs={vector_spout: Grouping.fields('word')},
                                    par=2)
