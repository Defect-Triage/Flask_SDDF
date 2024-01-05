import pandas as pd
import numpy as np
import gensim
from gensim.models import FastText
import re
from datetime import datetime
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from ApiManager import *


def getcurrentdefects(sessionid, platform):
    """getcurrentdefects collects all relevant defects from starc depending on the platform
    :param sessionid: str
        contains a key that is used to authenticate an API request
    :param platform: str
        contains the platform for that the defects are collected
    :return: pandas.Dataframe
        gives back a Dataframe with the currentdefects for the according platform
    """
    # create a list of lists to collect all the data from a json file
    defectid_list = []
    defect_list = []
    opendatelist = []
    data_list = [defectid_list, defect_list, opendatelist]
    date_format = "%Y-%m-%d"    # specify the date formate which is read from the json
    datetoday = datetime.today().strftime('%Y-%m-%d')   # get the current date to compare
    # check which platform was entered and use the according platformid to make the request
    if platform == "Gen20x.i2":
        platformid = "140599"
    elif platform == "Gen20x.i3_Star3.0":
        platformid = "3322425"
    elif platform == "Gen20x.i3_Star3.5":
        platformid = "155702"
    elif platform == "NTG7":
        platformid = "124772"
    elif platform == "MMC":
        platformid = "186740"

    # depending on the platform and the device the string has to be edited
    querystring = "project.id IN (16) AND tracker.id IN (14566687) AND '16.14566687.status' IN ('Open','In Progress','In Verification','Fixed') AND '14566687.choiceList[40]' IN (156146) AND PlatformID IN (" + platformid + ")"
    pagesize = '500'
    page = '1'

    # make an initial request to check how many defects you have to get
    response = getdatabyquery(sessionid, pagesize, page, querystring)

    # Iterate through all available defects in the query and store them in the lists
    if int(pagesize) > int(response['total']):
        upperlimit = int(response['total'])
        upperlimitpage = 1
    else:
        upperlimit = int(pagesize)
        upperlimitpage = int(np.ceil(response['total'] / int(pagesize)))

    for currentpage in range(int(page), upperlimitpage+1):
        response = getdatabyquery(sessionid, str(pagesize), str(currentpage), querystring)
        if response['total']-(currentpage-1)*response['pageSize'] < 500:
            upperlimit = int(response['total']) - (currentpage-1) * int(response['pageSize'])
        for x in range(0, upperlimit):
            data_list[0].append(response['items'][x]['id'])     # get the id for this defect
            data_list[1].append(response['items'][x]['name'])   # get the title(name) of this defect
            dateset = 0     # initialise a checkvariable
            for i in range(len(response['items'][x]['customFields'])):  # iterate through custom fields of the response
                if response['items'][x]['customFields'][i]['fieldId'] == 10055:
                    # get the open date of the defect and calculate passed days
                    date_raw = response['items'][x]['customFields'][i]['value']
                    date = re.search(r'\d{4}-\d{2}-\d{2}', date_raw)
                    a = datetime.strptime(date.group(), date_format).date()
                    b = datetime.strptime(datetoday, date_format).date()
                    delta = b - a   # calculate difference in days
                    data_list[2].append(delta)  # enter the days to the list

                    dateset = 1     # set check variable
                    break       # break out of custom field iteration
            if dateset == 0:
                data_list[2].append(0.01)    # if there was no date available enter this
    # create dataframe
    df = pd.DataFrame(columns=['score', 'defectid', 'defecttitle'])
    df['defectid'] = data_list[0]
    df['defecttitle'] = data_list[1]
    df['opendays'] = data_list[2]
    # df.to_excel('current_defects.xlsx')
    return df   # return dataframe


def spatialDistance(vector1, vector2):
    """calculates the eucledian distance between two sentence vectors"""
    return euclidean_distances([vector1], [vector2])


def spatialDistance1(vector1, vector2):
    """calculates the cosine similarity between two sentence vectors"""
    similarity_raw = str(round(float(cosine_similarity([vector1], [vector2])), 2))
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
    currentdefects_df['defecttitle'] = currentdefects_df['defecttitle'].str.replace('_', ' ')
	
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
