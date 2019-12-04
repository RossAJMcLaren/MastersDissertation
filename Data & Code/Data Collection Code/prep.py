import json, os, glob

directory = 'E:\MasterDiss\Data\BenignAPI\PostScalp'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        print(filename)
        loadpath = os.path.join(directory, filename)
        with open(loadpath, 'r') as json_data:
            data = json.load(json_data)
            graph = {}
            graph['Calls'] = []
            pastcall = {}
            pastcall['API'] = []
            pastcall['Arguments'] = []
            for call in data['process']:
                currentcall = call
                if currentcall['API'] == pastcall['API']:
                    if currentcall['Arguments'] == pastcall['Arguments']:
                        continue
                    else:
                        continue
                if len(graph["Calls"]) == 0:
                    graph["Calls"].append({
                        "API" : currentcall["API"],
                        "Arguments" : currentcall["Arguments"]
                })
                else:
                    if currentcall not in graph["Calls"]:
                        graph["Calls"].append({
                            "API" : currentcall["API"],
                            "Arguments" : currentcall["Arguments"]
                    })
                pastcall = currentcall
            savepath = os.path.join('E:\MasterDiss\Data\BenignAPI\PostProcess', filename)
            with open(savepath, 'w') as outfile:
                json.dump(graph, outfile)
              