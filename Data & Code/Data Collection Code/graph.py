import json, os, glob, csv

directory = 'E:\MasterDiss\Data\BenignAPI\PostProcess'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        print(filename)
        loadpath = os.path.join(directory, filename)
        savepath = os.path.join('E:\MasterDiss\Data\BenignAPI\Graphed', filename)
        with open(loadpath, 'r') as json_data:
            data = json.load(json_data)
            graphlist = {}
            outputlist = {}
            j = 0
            outputlist["Class"] = "Benign"
            while len(data["Calls"]) != 0:
                name = "Pattern " + str(j)
                graphlist[name] = {}
                graphlist[name]["API's"] = []
                graphlist[name]["API's"].append(data["Calls"][0])
                graphlist[name]["Args"] = []
                for arg in data["Calls"][0]["Arguments"]:
                    graphlist[name]["Args"].append(arg)
                data["Calls"].remove(data["Calls"][0])
                for call in data['Calls']:  
                    if call["API"] not in graphlist[name]["API's"]:
                        for arg in call["Arguments"]:
                            if arg in graphlist[name]["Args"]:
                                graphlist[name]["API's"].append(call)
                                for arg in call["Arguments"]:
                                    if arg not in graphlist[name]["Args"]:
                                        graphlist[name]["Args"].append(arg)
                                        continue
                j+=1
                for call in graphlist[name]["API's"]:
                    if call in data["Calls"]:
                        data["Calls"].remove(data["Calls"][data["Calls"].index(call)])
            j = 0
            for g in graphlist:
                if len(graphlist[g]) != 0:
                    if len(graphlist[g]["API's"]) > 1:
                        outputlist["Pattern " + str(j)] = []
                        for call in graphlist[g]["API's"]:
                            if call["API"] not in outputlist["Pattern " + str(j)]:
                                outputlist["Pattern " + str(j)].append(call["API"])
                        j+=1
        with open(savepath, 'w') as outfile:
            json.dump(outputlist, outfile)
            