import gensim
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import re
from gensim.models import FastText
def spatialDistance(vector1, vector2):
    """calculates the eucledian distance between two sentence vectors"""
    return euclidean_distances([vector1], [vector2])


def spatialDistance1(vector1, vector2):
    """calculates the cosine similarity between two sentence vectors"""
    similarity_raw = str(cosine_similarity([vector1], [vector2]))
    similarity = re.sub(r'\D\D', '', similarity_raw)
    similarity = round(float(similarity), 2)
    return similarity
def calculate_similarity(currentdefects_df, inputtitle, model):
    """ Calculates similarity between the input title and all current defects
    :param currentdefects_df: pandas.Dataframe
        includes all current defects for the previously defined platform
    :param inputtitle: str
        the title that is input by the user
    :param model: Fastext.model
        the model that was previously trained and is used to calculate the word embeddings
    :return: pandas.Dataframe
        the updated dataframe with the similarity score as a new column
    """
    df1 = currentdefects_df.copy()
    # preprocess the title collumn and the input title for creating the word embeddings
    df1.defecttitle = df1.defecttitle.map(gensim.utils.simple_preprocess)
    inputtitle = gensim.utils.simple_preprocess(inputtitle)
    inputvector = model.wv.get_sentence_vector(inputtitle)  # create a word embedding using the given model
    # create sentence vectors (word embeddings)
    df1['vector'] = df1.defecttitle.map(model.wv.get_sentence_vector)
    # calculate similarity to input
    currentdefects_df['score'] = df1.apply(lambda x: spatialDistance1(inputvector, x['vector']), axis=1)
    # sort the list for the highest score
    currentdefects_df = currentdefects_df.sort_values(by=['score'], axis=0, ascending=False, ignore_index=True)

    return currentdefects_df
