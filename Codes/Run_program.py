import os
from Create_GUI         import (GUI, update_loading_bar, create_loading_bar, 
                                close_loading_bar)
from Create_time_bins   import analyse_FED_file
from Create_master_file import (create_blank_master, add_columns_to_master, 
                                create_master_file)

while True:

    # Run the GUI.
    inputs = GUI()
        
    # Create a master file template.
    master = create_blank_master()
    
    # Analyse the data in each CSV file.
    import_files = [file for file in os.listdir(inputs['Import location']) if 
                    (file.lower().endswith(".csv") and file.startswith("~$")==False
                     and file.startswith('Time bins for')==False)]
    window = create_loading_bar(len(import_files))
    event, values = window.read(timeout=100)
    
    # for inputs['Filename'] in tqdm(import_files, ncols=70):
    for i in range(len(import_files)):
        
        inputs['Filename'] = import_files[i]
        
        # Analyse the individual FED file.
        df_bins = analyse_FED_file(inputs)
            
        # Add the columns to the master file.
        if inputs['Find individual columns'] == True:
            master = add_columns_to_master(master, df_bins, inputs)
            
        update_loading_bar(window, i+1)
    
    # Create the master master file.
    if inputs['Find individual columns'] == True:
        create_master_file(master, inputs)
        
    close_loading_bar(window)
