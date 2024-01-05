import pandas as pd
def process_data(data):
    type_title = data.get()
    type_platform =data.get()
    currentdefects_df = pd.DataFrame  # create Dataframe to store all current defects
    if type_platform == "Gen20x.i2":  # store the applicable current defects depending on the platform
        currentdefects_df = pd.read_excel(r"currentdefects_i2.xlsx")
    elif type_platform== "Gen20x.i3_Star3.0":
        currentdefects_df = pd.read_excel(r"currentdefects_i30.xlsx")
    elif  type_platform== "Gen20x.i3_Star3.5":
        currentdefects_df = pd.read_excel(r"currentdefects_i35.xlsx")
    elif  type_platform== "NTG7":
        currentdefects_df = pd.read_excel(r"currentdefects_ntg7.xlsx")
    elif  type_platform== "MMC":
        currentdefects_df = pd.read_excel(r"currentdefects_mmc.xlsx")
    if currentdefects_df.empty:  
        result = "No data found for the given platform."
    else:
        for row in currentdefects_df.iterrows():
             result += "Defect ID: {row['defectid']}, Title: {row['defecttitle']} (Score: {row['score']}) - High Similarity\n"
    return result
