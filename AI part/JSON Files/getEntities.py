import json

data_file1 = open('Artive-SCB\AI part\JSON Files\main_data.json').read()

main_data = json.loads(data_file1)
print(type(main_data))


data_file2 = open(
    'Artive-SCB\Customer-Care-Sample-Skill-dialog (4).json', encoding="utf8").read()

data = json.loads(data_file2)
print(type(data))


data_file3 = open(
    'Artive-SCB\Customer-Care-Sample-Skill-dialog.json', encoding="utf8").read()

data1 = json.loads(data_file3)
print(type(data1))

# t is a dictionary where the keys are intents and the values are responses as lists {"key": [...], ...} from Customer-Care-Sample-Skill-dialog (4).json file
t = {}
for dic in data["entities"]:
    lst = []
    for each in dic["values"]:
        if "synonyms" in each:
            lst = lst + each["synonyms"]
    t[dic["entity"]] = lst

# t1 is a dictionary where the keys are intents and the values are responses as lists {"key": [...], ...} from Customer-Care-Sample-Skill-dialog.json file
t1 = {}
for dic in data1["entities"]:
    lst = []
    for each in dic["values"]:
        if "synonyms" in each:
            lst = lst + each["synonyms"]
    t1[dic["entity"]] = lst


for each in main_data["intents"]:
    if each["intent"] in t.keys():
        each["responses"] = t[each["intent"]]
        t.pop(each["intent"])
    else:
        each["responses"] = []


for each in main_data["intents"]:
    if each["intent"] in t1.keys():
        each["responses"] = each["responses"] + t1[each["intent"]]
        t1.pop(each["intent"])

for entity, synonyms in t.items():
    lst = []
    if entity in t1.keys():
        lst = t1[entity]
        t1.pop(entity)
    new_dic = {"intent": entity, "examples": [], "responses": synonyms+lst}
    main_data["intents"].append(new_dic)

for entity, synonyms in t1.items():
    new_dic = {"intent": entity, "examples": [], "responses": synonyms}
    main_data["intents"].append(new_dic)

json_object = json.dumps(main_data, indent=2)
with open("Artive-SCB\AI part\JSON Files\main_data_new.json", "w") as outfile:
    outfile.write(json_object)
