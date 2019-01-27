from datamuse import datamuse
import nltk
from nltk.corpus import wordnet


# Download wordnet data if we don't have it already
try:
    nltk.data.find("wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)


def is_word_adjective(word):
    """Determine if a word is an adjective.

    Args:
        word (string): A single word.

    Returns (bool):
        True if the word is an adjective, false otherwise.
    """
    return any(ss.pos() == "a" for ss in wordnet.synsets(word))


def get_associated_adjectives(word, n):
    """Get the n adjectives most relating to a word.

    If the work is already an adjective, then just return the adjective
    wrapped in a list. Same story for if the word is actually not a
    single word.

    Args:
        word (string): A word.
        n (int): The number of associated adjectives to attempt getting.

    Returns (list):
        The word *and* (if all goes well) its requested associated adjectives.
    """
    # Get out if this isn't a single word or if this is already an
    # adjective
    if " " in word or is_word_adjective(word):
        return [word]

    # Instantiate Datamuse API client
    datamuse_client = datamuse.Datamuse()

    results = [hit["word"] for hit in datamuse_client.words(rel_jjb=word, max=n)]

    return [word] + results
