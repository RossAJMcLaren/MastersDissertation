import json, os, glob

report_dir = 'E:\MasterDiss\Data\BenignAPI\CuckooReports\*'
dirs = glob.glob(report_dir)
i = 0
for d in dirs:
    loadpath = os.path.join(d, 'reports', 'report.json')
    if os.path.exists(loadpath):
        with open(loadpath, 'r') as json_data:
            data = json.load(json_data)
            graph = {}
            processlist = []
            if 'behavior' in data:
                behaviors = data['behavior']
                if 'processes' in behaviors:
                    processes = behaviors['processes']
                    if len(processes) == 0:
                        break
                    else:
                        for process in processes:
                            graph['process'] = []
                            if process["process_name"] not in processlist:
                                if 'calls' in process:
                                    if len(process["calls"]) == 0:
                                        continue
                                    else:
                                        savepath = os.path.join("E:\MasterDiss\Data\BenignAPI\PostScalp", process["process_name"][:-3] + str(data["info"]["id"])+".json")
                                        calls = process['calls']
                                        for call in calls:
                                            cname = call['api']
                                            if call['api'][-3:] == "ExW" or call['api'][-3:] == "ExA":                  
                                                cname = call["api"][:-3]
                                            else:
                                                if call['api'][-2:] == "Ex" or call['api'][-2:] == "Ea":
                                                    cname = call['api'][:-2]
                                                else:
                                                    if call['api'][-1:] == "W" or call['api'][-1:] == "A" or call['api'][-1:] == "X":
                                                        cname = call['api'][:-1]
                                            graph["process"].append({
                                            "API" : cname,
                                            "Arguments" : call["arguments"]
                                            })
                                processlist.append(process["process_name"])
                                with open(savepath, 'w') as outfile:
                                    json.dump(graph, outfile)