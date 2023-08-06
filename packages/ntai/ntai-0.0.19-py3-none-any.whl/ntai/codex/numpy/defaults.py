import numpy as np
# from ntai.codex.numpy.utils import make_encodex_matrix, invert_codex

ENCODING_a      = [1,0,0,0,0,0]
ENCODING_c      = [0,1,0,0,0,0]
ENCODING_g      = [0,0,1,0,0,0]
ENCODING_t      = [0,0,0,1,0,0]
ENCODING_u      = [0,0,0,0,1,0]
ENCODING_repeat = [0,0,0,0,0,1]
INCLUDE_URACIL = False
INCLUDE_REPEAT = False

NUMPY_FASTA_ENCODEX = {
    '-': 0, # E is used to represent '-' as a python variable
    'A': 1,
    'C': 2,
    'G': 3,
    'T': 4,
    'U': 5,
    'R': 6,
    'Y': 7,
    'K': 8,
    'M': 9,
    'S': 10,
    'W': 11,
    'B': 12,
    'D': 13,
    'H': 14,
    'V': 15,
    'N': 16,
    '_': 17, # e is used to represent '_' as a python variable
    'a': 18,
    'c': 19,
    'g': 20,
    't': 21,
    'u': 22,
    'r': 23,
    'y': 24,
    'k': 25,
    'm': 26,
    's': 27,
    'w': 28,
    'b': 29,
    'd': 30,
    'h': 31,
    'v': 32,
    'n': 33,
}
