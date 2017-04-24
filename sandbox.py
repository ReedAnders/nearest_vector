import numpy as np

matrix = np.random.rand(10000,20)
i = -1

def _vec_gen():
    i =+ 1
    while i < matrix.shape[0]:
        yield matrix[i]


vector_generator = _vec_gen()

import pdb; pdb.set_trace()
