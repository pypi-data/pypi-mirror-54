Installation
============

**text2array** requires at least Python 3.6 and can be installed via pip::

    $ pip install text2array

Overview
========

.. doctest::

    >>> samples = [
    ...   {'ws': ['john', 'talks']},
    ...   {'ws': ['john', 'loves', 'mary']},
    ...   {'ws': ['mary']}
    ... ]
    >>>
    >>> # Create a Vocab
    >>> from text2array import Vocab
    >>> vocab = Vocab.from_samples(samples, options={'ws': dict(min_count=2)})
    >>> vocab['ws']
    StringStore(['<pad>', '<unk>', 'john', 'mary'], default='<unk>')
    >>> # 'talks' and 'loves' are out-of-vocabulary because they occur only once
    >>> 'john' in vocab['ws']
    True
    >>> vocab['ws'].index('john')
    2
    >>> 'talks' in vocab['ws']
    False
    >>> vocab['ws'].index('talks')  # unknown word is mapped to '<unk>'
    1
    >>>
    >>> # Applying vocab to samples
    >>> samples
    [{'ws': ['john', 'talks']}, {'ws': ['john', 'loves', 'mary']}, {'ws': ['mary']}]
    >>> samples = list(vocab.stoi(samples))
    >>> list(samples)
    [{'ws': [2, 1]}, {'ws': [2, 1, 3]}, {'ws': [3]}]
    >>>
    >>> # Shuffle, create batches of size 2, convert to array
    >>> from random import Random
    >>> from text2array import BatchIterator, ShuffleIterator
    >>> iterator = BatchIterator(ShuffleIterator(samples, rng=Random(123)), batch_size=2)
    >>> len(iterator)
    2
    >>> it = iter(iterator)
    >>> batch = next(it)
    >>> arr = batch.to_array()
    >>> arr['ws']
    array([[3, 0, 0],
           [2, 1, 3]])
    >>> batch = next(it)
    >>> arr = batch.to_array()
    >>> arr['ws']
    array([[2, 1]])
