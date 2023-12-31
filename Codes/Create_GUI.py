import pandas as pd
import os
import PySimpleGUI as sg
import sys

def str_to_bool(value):
    dict1 = {'True':True, 'False':False}
    return(dict1[value])

def create_loading_bar(max_value):
    # Define the layout of the window
    layout = [[sg.Text("Please wait while each folder within the master folder is analysed.")],
              [sg.ProgressBar(max_value, orientation='h', size=(30, 20), key='progressbar')]]

    # Create the window
    window = sg.Window('Loading Bar Example', layout)

    return window

def update_loading_bar(window, value):
    # Update the progress bar
    window['progressbar'].update_bar(value)
    
def close_loading_bar(window):
    # Update the progress bar
    window.close()

def default_values():
    
    default = {}

    # Choose the path of a folder, so the code can import every CSV file in the folder.
    default['Import location'] = r'C:\Users\hazza\Documents\Sipping data'
    default['Export location'] = r'C:\Users\hazza\Documents\Sipping data'
    
    # Choose the start and end times.
    default['Type start time']  = 'Use custom time'
    default['Start time']       = '2/07/2022 19:31:12'
    default['Type end time']    = 'Use custom time'
    default['End time']         = '2/07/2022 21:48:57'
    
    # Choose the interval for the time bins.
    default['Time bin (mins)'] = 1
    
    # Choose whether to analyse individual columns and select genotypes/treatments.
    # Choose whether to import an existing settings file.
    default['Find individual columns']    = False
    default['Use settings file']          = False
    
    return(default)

def basic_options(default):
    
    # Create a dictionary with the inputs from the GUI.
    inputs = {}
    
    # Create a GUI with the options for analysis.
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text("Choose a folder for the import location"), 
                     sg.Input(default_text=default['Import location'],key="Import",
                              enable_events=True),sg.FolderBrowse(key="Import2")],
        [sg.T("")], [sg.Text("Choose a folder for the export location"),
                     sg.Input(default_text=default['Export location'],key="Export",
                              enable_events=True),sg.FolderBrowse(key="Export2")],
        [sg.T("")], [sg.Text("Start time",size=(8,1)), 
                     sg.Combo(["Use custom time","Use first timestamp"],
                              default_value=default['Type start time'], size=(17,1),
                              key="Type_Start_Time",enable_events=True),
                     sg.Input(default_text=default['Start time'],key="Start_Time",
                              enable_events=True, size=(25,1))],
        [sg.T("")], [sg.Text("End time",size=(8,1)), 
                     sg.Combo(["Use custom time","Use last timestamp"],
                              default_value=default['Type end time'], size=(17,1),
                              key="Type_End_Time",enable_events=True),
                     sg.Input(default_text=default['End time'],key="End_Time",
                              enable_events=True, size=(25,1))],
        [sg.T("")], [sg.Text("Time bin interval (in mins)",size=(20,1)), 
                     sg.Input(default_text=default['Time bin (mins)'],key="Time_Bin",
                              enable_events=True,size=(10,1))],
        [sg.T("")], [sg.Text("Get individual column summaries and label " +
                             "genotypes/treatments",size=(48,1)), 
                     sg.Combo(["True", "False"],
                              default_value=str(default['Find individual columns']),
                              key="Find_Ind_Cols",enable_events=True)],
        [sg.T("")], [sg.Button("Submit")]
             ]
    window = sg.Window('Options for analysis', layout)
        
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        # Make the time entries invisible if needed.
        if values["Type_Start_Time"] in ["Use first timestamp","Use initiation poke"]:
            window.Element("Start_Time").Update(visible=False)
        if values["Type_Start_Time"] == 'Use custom time':
            window.Element("Start_Time").Update(visible=True)
        if values["Type_End_Time"] == "Use last timestamp":
            window.Element("End_Time").Update(visible=False)
        if values["Type_End_Time"] == 'Use custom time':
            window.Element("End_Time").Update(visible=True)
        # If submit is pressed, record the entries in the GUI.
        if event == "Submit":
            inputs['Import location']         = values["Import"]
            inputs['Export location']         = values["Export"]
            inputs['Start time type']         = values["Type_Start_Time"]
            inputs['Start time']              = values["Start_Time"]
            inputs['End time type']           = values["Type_End_Time"]
            inputs['End time']                = values["End_Time"]
            inputs['Time bin (mins)']         = float(values["Time_Bin"])
            inputs['Find individual columns'] = str_to_bool(values["Find_Ind_Cols"])
            window.close()
            break
        
    return(inputs)

def import_settings_file(inputs, default):
    
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text(("Import an existing settings excel file with filenames, "+
                              "genotypes and treatments.")), 
                     sg.Combo(["True", "False"],default_value=str(default['Use settings file']),
                              key="Settings",enable_events=True)],
        [sg.T("")], [sg.Button("Submit")]
             ]
    window = sg.Window('Choose whether to import an excel file', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            inputs['Use settings file'] = str_to_bool(values["Settings"])
            window.close()
            break
    
    return(inputs)    
    
def choose_settings_file_location(inputs):
    
    sg.theme("DarkTeal2")
    layout = [
        [sg.T("")], [sg.Text("Choose the location of the settings excel file."), 
                     sg.Input(default_text=inputs['Import location'],key="Import",
                              enable_events=True),sg.FileBrowse(key="Import2")],
        [sg.T("")], [sg.Button("Submit")]
             ]
    window = sg.Window('Choose the location of the excel file.', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            file_path = values["Import"]
            window.close()
            break
    gt_table = pd.read_excel(file_path, index_col=0)
    gt_table = gt_table.fillna('')
    inputs['Genotypes/treatments table'] = gt_table
    
    return(inputs)
    
def create_settings_file(inputs):
    
    # Based on the import location, list all the CSV files to import.
    import_files = [file for file in os.listdir(inputs['Import location']) if 
                    (file.lower().endswith(".csv") and file.startswith("~$")==False)]
    sg.theme("DarkTeal2")
    size1 = (30,1)
    size2 = (34,1)
    layout = [[sg.T("")], [sg.Text('Filename',size=size1), 
                           sg.Text('Genotype',size=size1),
                           sg.Text('Treatment',size=size1)]]
    for filename in import_files:
        layout += [[sg.Text(filename,size=size1), 
                    sg.Input(size=size2,key=filename+'_Genotype'),
                    sg.Input(size=size2,key=filename+'_Treatment')]]
    layout += [[sg.T("")], [sg.Button("Submit")]]
    window = sg.Window('Fill in the genotypes/treatments', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            gt_table = pd.DataFrame(columns=['Genotype','Treatment'],
                                    index=import_files)
            gt_table.index.name = 'Filename'
            for filename in import_files:
                gt_table.at[filename,'Genotype']  = values[filename+'_Genotype']
                gt_table.at[filename,'Treatment'] = values[filename+'_Treatment']
            window.close()
            break    
    inputs['Genotypes/treatments table'] = gt_table
    
    return(inputs)

def export_settings_file(inputs):
    
    # Export the settings as an excel file.
    export_name = 'Settings_excel_file0.xlsx'
    i = 1
    while export_name in os.listdir(inputs['Export location']):
        export_name = export_name[:-6] + str(i) + '.xlsx'
        i += 1
    export_destination = os.path.join(inputs['Export location'], export_name)
    inputs['Genotypes/treatments table'].to_excel(export_destination)
    print('Saved ' + export_name + ' at ' + inputs['Export location'] + '\n')
    
def GUI():
    
    default = default_values()
    inputs = basic_options(default)
    
    # If find individual columns is true, ask whether to import an existing excle file.
    if inputs['Find individual columns'] == True:
        inputs = import_settings_file(inputs, default)
            
        # If the previous option is true, ask for the import location.
        if inputs['Use settings file'] == True:
            inputs = choose_settings_file_location(inputs)
        
        # If the previous option is false, type in the genotypes/treatments.
        if inputs['Use settings file'] == False:
            inputs = create_settings_file(inputs)
            export_settings_file(inputs)
            
    return(inputs)
