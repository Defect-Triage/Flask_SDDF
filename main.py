"""Main file for SDDF includes GUI and highlevel function execution
Main File for SDDF includes GUI and execution depending on the input of the user
On execution the application authenticates the user in the Starc-API and asks for a Session-ID
To get the current Data the user needs to press update database which requires the session ID to be entered.
As soon as the database is updated, the duplicates can be searched. To do that the title and Platform need to be entered
After pressing the button "Process", The probable duplicates will be displayed.

Author: Lael Klaiber

Created: 20.07.2023
"""
# imports:
from DataManager import *  # handles all functional tasks like data management and similarity calc.
import ttkbootstrap as ttk  # Using Tkinters module ttkbootstrap to create an appealing gui
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import webbrowser
import pandas as pd

# modules
def process_data():
    """process_data calculates a table of possible duplicates based on entry2 and entry3 (title and platform)"""
    #delete everything in treeview that was there before
    for item in tree.get_children():
        tree.delete(item)

    titleinput = entry2.get()  # retrieve the title from entry2
    platform = platform_combo.get()  # retrieve the platform from entry3
    currentdefects_df = pd.DataFrame  # create Dataframe to store all current defects
    if platform == "Gen20x.i2":  # store the applicable current defects depending on the platform
        currentdefects_df = pd.read_excel(r"currentdefects_i2.xlsx")
    elif platform == "Gen20x.i3_Star3.0":
        currentdefects_df = pd.read_excel(r"currentdefects_i30.xlsx")
    elif platform == "Gen20x.i3_Star3.5":
        currentdefects_df = pd.read_excel(r"currentdefects_i35.xlsx")
    elif platform == "NTG7":
        currentdefects_df = pd.read_excel(r"currentdefects_ntg7.xlsx")
    elif platform == "MMC":
        currentdefects_df = pd.read_excel(r"currentdefects_mmc.xlsx")

    if currentdefects_df.empty:  # check if platform was wrong
        pass
    else:
        # calculate the most similar defects depending on the title
        currentdefects_df = calculate_similarity(currentdefects_df, titleinput, model)
        # remove the index
        currentdefects_df.pop(currentdefects_df.columns[0])
        # taking all the columns heading in a variable"df_col".
        df_col = currentdefects_df.columns.values

        # all the column name are generated dynamically.
        tree["columns"] = (df_col)
        counter = len(currentdefects_df)
        rowLabels = currentdefects_df.index.tolist()

        # create variables to display the table in the gui
        l1 = list(currentdefects_df)  # List of column names as headers
        r_set = currentdefects_df.to_numpy().tolist()  # Create list of list using rows
        tree['columns'] = l1
        # Defining headings, other option in tree
        # width of columns and alignment
        tree.column('score', width=60, anchor='w', stretch=False)
        tree.column('defectid', width=70, anchor='w', stretch=False)
        tree.column('defecttitle', width=600, anchor='w', stretch=False)
        tree.column('opendays', width=70, anchor='w', stretch=False)

        tree['show'] = 'headings'
        # for i in l1:
        #     tree.column(i, width=1000, anchor='w')
        # Headings of respective columns
        for i in l1:
            tree.heading(i, text=i, anchor='w')
        for dt in r_set:
            v = [r for r in dt]  # collect the row data as list
            if float(v[0]) >= 0.80:
                tree.insert("", 'end', iid=v[1], values=v, tag='gr')
                tree.tag_configure(tagname='gr', foreground='#000fff000')
            if float(v[0]) >= 0.5 and float(v[0])<0.80:
                tree.insert("", 'end', iid=v[1], values=v, tag='ye')
                tree.tag_configure(tagname='ye', foreground='yellow')
            if float(v[0]) < 0.5:
                tree.insert("", 'end', iid=v[1], values=v, tag='re')
                tree.tag_configure(tagname='re', foreground='red')
        tree.pack(pady=15, padx=10, fill="x")


    return


def open_link(event):
    tree = event.widget
    region = tree.identify_region(event.x, event.y)
    col = tree.identify_column(event.x)
    iid = tree.identify('item', event.x, event.y)
    if region == 'cell':
        defectid = tree.item(iid)['values'][1]  # get the link from the selected row
        webbrowser.open('https://starc.i.mercedes-benz.com/issue/'+str(defectid))  # open the link in a browser tab
    return
def update_database():
    """Updates the Database and gets all current defects for all platforms"""

    # get all defects for the available platform and store them #
    currentdefects_i2 = getcurrentdefects(sessionid, 'Gen20x.i2')
    currentdefects_i2.to_excel('currentdefects_i2.xlsx')
    print('updated Gen20x.i2')
    currentdefects_i30 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.0')
    currentdefects_i30.to_excel('currentdefects_i30.xlsx')
    print('updated Gen20x.i3_Star3.0')
    currentdefects_i35 = getcurrentdefects(sessionid, 'Gen20x.i3_Star3.5')
    currentdefects_i35.to_excel('currentdefects_i35.xlsx')
    print('updated Gen20x.i3_Star3.5')
    currentdefects_ntg7 = getcurrentdefects(sessionid, 'NTG7')
    currentdefects_ntg7.to_excel('currentdefects_ntg7.xlsx')
    print('updated NTG7')
    currentdefects_mmc = getcurrentdefects(sessionid, 'MMC')
    currentdefects_mmc.to_excel('currentdefects_mmc.xlsx')
    print('updated MMC')
    return

if __name__ == '__main__':
    # Create the main window
    root = ttk.Window()
    style = ttk.Style()
    style.theme_use('darkly')
    style.configure('Treeview', rowheight=30)
    root.title("SmarDuplicateDefectFinder © Lael Klaiber")  # name the window
    root.geometry("1000x600")  # Set the window size
    sessionid = authenticate()  # authenticate the application to access the starc-API
    model = FastText.load('fasttext.model')  # load in language model

    # Create the input fields and pack them into the gui
    # frame_sessionid = ttk.Frame(root)  # get the sessionid
    # frame_sessionid.pack(pady=15, padx=10, fill="x")
    # ttk.Label(frame_sessionid, text="Sessionid:  ").pack(side="left", padx=5)
    # entry1 = ttk.Entry(frame_sessionid)
    # entry1.pack(side="left", fill="x", expand=True, padx=5)

    frame_title = ttk.Frame(root)  # get the title
    frame_title.pack(pady=15, padx=10, fill="x")
    ttk.Label(frame_title, text="Defecttitle:").pack(side="left", padx=5)
    entry2 = ttk.Entry(frame_title)
    entry2.pack(side="left", fill="x", expand=True, padx=5)

    frame_platform = ttk.Frame(root)  # get the platform
    frame_platform.pack(pady=15, padx=10, fill="x")
    ttk.Label(frame_platform, text="Platform:   ").pack(side="left", padx=5)
    platform_combo = ttk.Combobox(
        frame_platform,
        state='readonly',
        values=['Gen20x.i2', 'Gen20x.i3_Star3.0', 'NTG7', 'MMC'] #Removed ', 'Gen20x.i3_Star3.5'' As it doesn't work currently
    )
    platform_combo.pack(side="left", padx=5)

    # entry3 = ttk.Entry(frame_platform)
    # entry3.pack(side="left", fill="x", expand=True, padx=5)

    # Create the buttons and assign the according function to it
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=50, padx=10, fill="x")
    ttk.Button(button_frame, text="Process", command=process_data).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Update Database", command=update_database).pack(side="left", padx=10)

    colors = root.style.colors  # for using alternate colours
    # create Treeview
    tree = ttk.Treeview(root, selectmode='browse')

    tree.bind('<Button-3>', open_link)
    # Start the GUI event loop
    root.mainloop()
