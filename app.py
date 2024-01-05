# '''App file for SDDF includes function execution depending on input of the user.
# On execution the application authenticates the user in the Starc-API and asks for a Session-ID.
# To get the current data the user needs to sync-tickets which requires the session ID to be entered.
# As soon as the database is updated, the duplicates can be searched.To do that the title and Platforn need to be entered.
# After which by process_data function executes, the probable duplicates will be displayed.'''
# import pandas as pd
# from gensim.models import FastText
# from DataManager import calculate_similarity, authenticate, getcurrentdefects # handles all functional tasks like data management and similarity calc.

# model = FastText.load('fasttext.model') #load the fast text model
# sessionid = authenticate()  #authenticate the application to access the starc-API

# def process_data(title, platform, threshold):
#     currentdefects_df = pd.DataFrame() #create a empty dataframe to store defects

#     if platform == "Gen20x.i2": #store the current defects depending on the platform
#         currentdefects_df = pd.read_excel("currentdefects_i2.xlsx")
#     elif platform == "Gen20x.i3_Star3.0":
#         currentdefects_df = pd.read_excel("currentdefects_i30.xlsx")
#     elif platform == "Gen20x.i3_Star3.5":
#         currentdefects_df = pd.read_excel("currentdefects_i35.xlsx")
#     elif platform == "NTG7":
#         currentdefects_df = pd.read_excel("currentdefects_ntg7.xlsx")

#     similardefects = calculate_similarity(currentdefects_df, title, model)  #Calculate similarity between the title and all the existing defect titles
#     duplicates = list()
#     for _, row in similardefects.iterrows():
#         similardefects_score = row['score']
#         if similardefects_score >= float(threshold):
#             #Create a list for each duplicate defect and append to the list.
#             ticket = {                          
#                 "Defect ID": row['defectid'],
#                 "Title": row['defecttitle'],
#                 "Score": similardefects_score,
#                 "OpenDays": row['opendays'],
#             }
#             duplicates.append(ticket)
#     return duplicates 

# def sync_tickets():
#     try:
#         # Update the database and get all current defects for different platforms
#         currentdefects_i2 = getcurrentdefects(sessionid, 'Gen20x.i2')
#         currentdefects_i2.to_excel('currentdefects_i2.xlsx', engine='xlsxwriter')
#         print('Updated Gen20x.i2')

#         currentdefects_i30 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.0')
#         currentdefects_i30.to_excel('currentdefects_i30.xlsx', engine='xlsxwriter')
#         print('Updated Gen20x.i3_Star3.0')

#         currentdefects_i35 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.5')
#         currentdefects_i35.to_excel('currentdefects_i35.xlsx', engine='xlsxwriter')
#         print('Updated Gen20x.i3_Star3.5')
        
#         currentdefects_ntg7 = getcurrentdefects(sessionid, 'NTG7')
#         currentdefects_ntg7.to_excel('currentdefects_ntg7.xlsx', engine='xlsxwriter')
#         print('Updated NTG7')

#         currentdefects_mmc = getcurrentdefects(sessionid, 'MMC')
#         currentdefects_mmc.to_excel('currentdefects_mmc.xlsx', engine='xlsxwriter')
#         print('Updated MMC')

#         return "Database updated successfully"
#     except Exception as e:
#         return {"error": str(e)}


'''App file for SDDF includes function execution depending on input of the user.
On execution the application authenticates the user in the Starc-API and asks for a Session-ID.
To get the current data the user needs to sync-tickets which requires the session ID to be entered.
As soon as the database is updated, the duplicates can be searched.To do that the title and Platforn need to be entered.
After which by process_data function executes, the probable duplicates will be displayed.'''
import pandas as pd
from gensim.models import FastText
from DataManager import calculate_similarity, authenticate, getcurrentdefects # handles all functional tasks like data management and similarity calc.

model = FastText.load('fasttext.model') #load the fast text model
sessionid = authenticate()  #authenticate the application to access the starc-API

import os

def process_data(title, platform, threshold):
    try:
        platforms = ["Gen20x.i2", "Gen20x.i3_Star3.0", "Gen20x.i3_Star3.5", "NTG7", "MMC"]

        if platform not in platforms:
            return [{"error": f"Invalid platform: {platform}"}]

        filename = f"currentdefects_{platform.lower()}.xlsx"

        if not os.path.exists(filename):
            return [{"error": f"File not found: {filename}"}]

        currentdefects_df = pd.read_excel(filename)

        # Rest of the code for processing data

        similardefects = calculate_similarity(currentdefects_df, title, model)

        duplicates = [
            {
                "Defect ID": row['defectid'],
                "Title": row['defecttitle'],
                "Score": row['score'],
                "OpenDays": row['opendays'],
            }
            for _, row in similardefects.iterrows() if row['score'] >= float(threshold)
        ]

        return duplicates

    except Exception as e:
        return [{"error": f"An error occurred during data processing: {str(e)}"}]

def sync_tickets():
    try:
        # Update the database and get all current defects for different platforms
        currentdefects_i2 = getcurrentdefects(sessionid, 'Gen20x.i2')
        currentdefects_i2.to_excel('currentdefects_i2.xlsx', engine='xlsxwriter')
        print('Updated Gen20x.i2')

        currentdefects_i30 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.0')
        currentdefects_i30.to_excel('currentdefects_i30.xlsx', engine='xlsxwriter')
        print('Updated Gen20x.i3_Star3.0')

        currentdefects_i35 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.5')
        currentdefects_i35.to_excel('currentdefects_i35.xlsx', engine='xlsxwriter')
        print('Updated Gen20x.i3_Star3.5')
        
        currentdefects_ntg7 = getcurrentdefects(sessionid, 'NTG7')
        currentdefects_ntg7.to_excel('currentdefects_ntg7.xlsx', engine='xlsxwriter')
        print('Updated NTG7')

        currentdefects_mmc = getcurrentdefects(sessionid, 'MMC')
        currentdefects_mmc.to_excel('currentdefects_mmc.xlsx', engine='xlsxwriter')
        print('Updated MMC')

        return "Database updated successfully"
    except Exception as e:
        return {"error": str(e)}


