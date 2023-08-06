from random import choices, random, randint
from .defaults import FASTA_CHARS
def random_fasta(min_length:int=0, max_length:int=100, repeat_likelihood:float=0.5) -> str:
    '''
    Arguments:
        min_length (int): minimum length the sequence should be.
        max_length (int): maximum length the sequence should be.
        repeat_likelihood (float): likelihood a given character in the sequence
            should be a repeated masked region.
    Returns:
        sequence (str): the fasta sequence.
    '''
    n = randint(min_length, max_length)
    chars = choices(list(FASTA_CHARS), k=n)
    return ''.join([e if random() < repeat_likelihood else e.upper() for e in chars])
