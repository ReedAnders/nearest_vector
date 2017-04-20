"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.NearestVectors import NearestVectorsBolt
from spouts.words import WordSpout


class NearestVectors(Topology):
    word_spout = WordSpout.spec()
    count_bolt = NearestVectorsBolt.spec(inputs={word_spout: Grouping.fields('word')},
                                    par=2)
