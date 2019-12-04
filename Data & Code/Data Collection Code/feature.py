import json, os, glob, csv

b_directory = '.\BenignAPI\Graphed'
m_directory = '.\MaliciousAPI\Graphed'
apipatterns = {}
j = 1
savepath = os.path.join('E:\MasterDiss\Data', "APIPatterns.json")
for filename in os.listdir(b_directory):
    if filename.endswith(".json"):
        loadpath = os.path.join(b_directory, filename)
        with open(loadpath, 'r') as json_data:
            data = json.load(json_data)
            data.pop('Class', None)
            for d in data:
                if data[d] not in apipatterns.values():
                    apipatterns["Pattern " + str(j)] = data[d]
                    j+=1
for filename in os.listdir(m_directory):
    if filename.endswith(".json"):
        loadpath = os.path.join(m_directory, filename)
        with open(loadpath, 'r') as json_data:
            data = json.load(json_data)
            data.pop('Class', None)
            for d in data:
                if data[d] not in apipatterns.values():
                    apipatterns["Pattern " + str(j)] = data[d]
                    j+=1
print(apipatterns)
with open(savepath, 'w') as data:
    json.dump(apipatterns, data)
                    
                