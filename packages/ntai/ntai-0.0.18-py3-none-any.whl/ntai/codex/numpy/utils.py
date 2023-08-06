import numpy as np
from ntai.codex.numpy.defaults import (
    INCLUDE_URACIL,
    INCLUDE_REPEAT,
    ENCODING_a,
    ENCODING_c,
    ENCODING_g,
    ENCODING_t,
    ENCODING_u,
    ENCODING_repeat
)

def validate_base_encoding(name, encoding):
    if np.cumsum(encoding)[-1] != 1:
        msg = 'base encoding for {} should be one hot!'.format(name)
        raise ValueError(msg)
    if encoding.size != 6:
        msg = 'base encoding for {} should be of shape (6, )!'.format(name)
        raise ValueError(msg)

def make_encodex_matrix(
    encodex:dict,
    a:list       = ENCODING_a,
    c:list       = ENCODING_c,
    g:list       = ENCODING_g,
    t:list       = ENCODING_t,
    u:list       = ENCODING_u,
    repeat:list  = ENCODING_repeat
) -> list:

    E = np.zeros((6, ), dtype=np.int64) # '-'
    A = np.array(a)
    C = np.array(c)
    G = np.array(g)
    T = np.array(t)
    U = np.array(u)
    _R = np.array(repeat)





    encodings = [('a', A),('c', C),('g', G,),('t', T,),('u', U,),('r', _R)]
    for c, encoding in encodings:
        validate_base_encoding(c, encoding)


    R = A + G
    Y = C + T + U
    K = G + T + U
    M = A + C
    S = C + G
    W = A + T + U
    B = C + G + T + U
    D = A + G + T + U
    H = A + C + T + U
    V = A + C + G
    N = A + C + G + T + U

    _e = E + _R
    _a = A + _R
    _c = C + _R
    _g = G + _R
    _t = T + _R
    _u = U + _R
    _r = _R

    r =  R + _R
    y =  Y + _R
    k =  K + _R
    m =  M + _R
    s =  S + _R
    w =  W + _R
    b =  B + _R
    d =  D + _R
    h =  H + _R
    v =  V + _R
    n =  N + _R


    encodex_matrix = np.array([
        E,  A, C, G, T, U, R, Y, K, M, S, W, B, D, H, V, N,
       # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,
        _e,_a,_c,_g,_t,_u, r, y, k, m, s, w, b, d, h, v, n,
       #17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33
        # E,  A, C, G, T, U, R, Y, K, M, S, W, B, D, H, V, N,
    ])
    return encodex_matrix[list(encodex.values())]


def invert_encodex(encodex:dict) -> dict:
    k, v = zip(*encodex.items())
    return dict(zip(v, k))

def find_row(matrix:list, row:list) -> int:
    return np.where(np.all(matrix == row, axis=1))[0][0]

def _char_to_int(char:str, encodex:dict)->int:
    return encodex[char]

def _sequence_to_indices(sequence:str, encodex:dict)->list:
    fn = lambda c: _char_to_int(c, encodex)
    return list(map(fn, sequence))


def lookup_channel_index(
    channel:int,
    encodex:dict,
    encodex_matrix:list
) -> int:
    return np.argmax(encodex_matrix[_char_to_int(channel, encodex)])


def get_channel_indices(
    encodex: dict,
    encodex_matrix: list,
    include_uracil: bool = INCLUDE_URACIL,
    include_repeat: bool = INCLUDE_REPEAT
) -> list:
    # drop uracil or repeat channel as needed
    channels = 'acgt'
    if include_uracil: channels += 'u'
    if include_repeat: channels += '_'
    fn = lambda c: lookup_channel_index(c, encodex, encodex_matrix)
    return list(map(fn, channels))


def encode(
    sequence:str,
    encodex: dict,
    encodex_matrix: list = None,
    include_uracil: bool = INCLUDE_URACIL,
    include_repeat: bool = INCLUDE_REPEAT
):
    # convert from string to integers
    indices = np.array(_sequence_to_indices(sequence, encodex))
    if encodex_matrix is None:
        encodex_matrix = make_encodex_matrix(encodex=encodex)
    # extract the rows from the encoding matrix in order as they appear in seq
    results = encodex_matrix[indices]
    channel_indices = get_channel_indices(encodex, encodex_matrix, include_uracil, include_repeat)
    # filter results
    return results[:, channel_indices].tolist()

def decode(
    encoded:list,
    encodex: dict,
    encodex_matrix: list = None,
    include_uracil: bool = INCLUDE_URACIL,
    include_repeat: bool = INCLUDE_REPEAT,
    decodex: dict = None
):

    if encodex_matrix is None:
        encodex_matrix = make_encodex_matrix(encodex=encodex)
    if decodex is None:
        decodex = invert_encodex(encodex)

    channel_indices = get_channel_indices(encodex, encodex_matrix, include_uracil, include_repeat)
    filtered_matrix = encodex_matrix[:, channel_indices]
    keys = list(map(lambda r: find_row(filtered_matrix, r), encoded))
    return ''.join(list(map(lambda k: decodex[k], keys)))
