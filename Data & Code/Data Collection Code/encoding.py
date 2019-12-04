import json, os, glob, csv
# 1. Load the patterns list
# 2. Load the graphed program 
# 3. For each item in the Pattern List, check if it exists in the graphed program
# 4. If it exists, write a 1 to the list
# 5. If it doesn't, write a 0
# 6. Write the class at the end of the list
# 7. Print the list to CSV
loadpath = "E:\MasterDiss\Data\APIPatterns.json"
directory = ".\Graphed"
savepath = os.path.join(".\Encoded","b_Encoded.csv")

with open(loadpath, "r") as json_data:
    dataset = json.load(json_data)  
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            print(filename)
            graphpath = os.path.join(directory, filename)
            with open(graphpath, "r") as graph_data:
                data = json.load(graph_data)
                graphlist = []
                for d in dataset:
                    if dataset[d] in data.values():
                        graphlist.append("1")
                    else:
                        graphlist.append("0")
                if data["Class"] == "Malware":
                    graphlist.append("1")
                else:
                    graphlist.append("0")
                with open(savepath, "a") as encoded:
                    writer = csv.writer(encoded)
                    writer.writerow(graphlist)