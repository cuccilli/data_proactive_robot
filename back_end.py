import json
import pandas as pd
from pathlib import Path
import statistics

# Calculate DGD result
def get_dgd_result(data):
    tmp = {}
    tmp["Conqueror"] = 0
    tmp["Manager"] = 0
    tmp["Wanderer"] = 0
    tmp["Participant"] = 0

    for i in data:
        if(int(i[1:])%4 == 1):
            tmp["Conqueror"] += data[i]
        elif (int(i[1:])%4 == 2):
            tmp["Manager"] += data[i]
        elif (int(i[1:])%4 == 3):
            tmp["Wanderer"] += data[i]
        else:
            tmp["Participant"] += data[i]
    return tmp

# Perceived Social Intelligence
def get_psi_result(data):
    res = {}
    label = ["RB", "HLP", "TRU", "RC", "AC", "PC", "SOC"]
    for i in label:
        res[i] = []
    for i in range(1,28, 7):
        x = i
        for tmp in range(0,7):
            res[label[tmp]].append(data["Q"+str(x)])
            x += 1
    # Reverse Item 
    res["AC"][1] = 6 - res["AC"][1]
    res["SOC"][2] = 6 - res["SOC"][2]

    # Mean Res
    for i in res:
        res[i] = statistics.mean(res[i])
    
    return res

# Service Proactivity
def get_sp_result(data):
    res = []
    for i in range(29, 35):
        res.append(data["Q"+str(i)])

    return statistics.mean(res)

# Actions from Robot
def get_n_action(dict_level):
    frequency = 0
    liked = 0
    unliked = 0
    # For each level 
    for level_loop in range(1, len(dict_level)+1):
        level = str(level_loop)
        if(level in dict_level.keys()): 
            # For each state
            dict_state = dict_level[level]["sequenza"]
            for state_ in range(0, len(dict_state.keys())):
                state = str(state_)
                moves_dict = dict_state[state]["mossa"]
                # For each action
                for move_loop in range(0, len(moves_dict)):
                    move = str(move_loop)
                    # Set Assistance Requested
                    action_type = moves_dict[move]["tipo"]
                    if action_type == "Intervento":
                        # Update Old Action with the new one 
                        frequency += 1
                    elif action_type == "Gradito":
                        liked += 1
                    elif action_type == "Non Gradito":
                        unliked += 1
    return frequency, liked, unliked

##################################################################################################

def get_data():
    files_random = [str(x)[7:] for x in Path("./random/").glob("*.json")]
    write = []
    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

    for txt_path in Path(".").glob("*.json"):
        # Get data from file
        file_json = open(txt_path)
        data = json.load(file_json)

        # Get questionnaires' result
        dgd = get_dgd_result(data["dgd_test"])
        psi = get_psi_result(data["post_interaction"])
        sp = get_sp_result(data["post_interaction"])

        # Get the number of robot actions 
        n_action, liked, unliked = get_n_action(data["partita"]["livello"])

        id = 0 if str(txt_path) in files_random else 1
        # Write the row on array
        write.append([id, int(data["eta"]), data["genere"], data["formazione"], dgd["Conqueror"], dgd["Manager"], dgd["Wanderer"], dgd["Participant"], data["partita"]["livello_raggiunto"], data["partita"]["score_tot"], data["partita"]["errori_tot"], data["partita"]["aiuti_tot"], data["partita"]["aiuti_tot"]-n_action, n_action, liked, unliked, psi['RB'], psi['HLP'], psi['TRU'], psi['RC'], psi['AC'], psi['PC'], psi['SOC'], sp])

    # Convert array to Pandas DataFrame
    df = pd.DataFrame(write,  columns=['ID','Age', 'Gender', 'Education', 'Conqueror', 'Manager', 'Wanderer', 'Participant', 'Level','Score','#Mistakes','#AssistanceTot', '#AssistanceRequested', '#AssistanceFromRobot', 'Liked', 'Unliked', 'RB', 'HLP', 'TRU', 'RC', 'AC', 'PC', 'SOC', 'ServiceProactivity']).sort_values('ID')
    df.to_excel(writer, index=False, sheet_name='Generic')

    # Get Means for each condition
    write = []
    mean_value = ['ID', 'Frequency', '#Male', '#Female', 'Age', 'Level','Score','#Mistakes','#AssistanceTot', '#AssistanceRequested', '#AssistanceFromRobot', 'Liked', 'Unliked', 'RB', 'HLP', 'TRU', 'RC', 'AC', 'PC', 'SOC', 'ServiceProactivity']
    for id in range(0, 2):
        dfID = df[df['ID']==id]
        # Get Means
        dfMean = dfID.drop(columns=['ID']).mean()
        # Set ID, Frequency, Number of Male, Number of Female
        tmp = [id, (dfID['ID']==id).sum(), (dfID['Gender']=='Maschio').sum(), (dfID['Gender']=='Femmina').sum()]
        # Set other columns
        for i in mean_value[4:]:
            tmp.append(dfMean[i])
        write.append(tmp)
    df2 = pd.DataFrame(write,  columns=mean_value)
    df2.to_excel(writer, index=False, sheet_name='Mean')

    # Save Data
    writer.save()

if __name__ == "__main__":
    get_data()