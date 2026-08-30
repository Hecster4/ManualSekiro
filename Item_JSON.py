from ItemCategories import important_items, key_items, memories, skills_and_prosthetics, health_and_healing_upgrades, headless_items
from ParamNames import ItemLotParam
from os import path, remove

categories = {"Key Items": key_items,
              "Memories": memories,
              "Skills and Prosthetics": skills_and_prosthetics,
              "Health and Healing Upgrades": health_and_healing_upgrades,
              "Headless Items": headless_items}
             
def write_items_json(replacment):
    names: list = []
    count: dict = {}
    item_category: dict = {}
    for item in important_items:
        name = ItemLotParam[replacment[item]][ItemLotParam[replacment[item]].index("]") + 2: len(ItemLotParam[replacment[item]])]
        if name not in names:
            names.append(name)
            count[name] = 0
        count[name] += 1
        for category in categories:
            if replacment[item] in categories[category]:
                item_category[name] = category
                break
            else:
                item_category[name] = "Filler"
    if path.exists("manual_sekiro/data/items.json"):
        remove("manual_sekiro/data/items.json")
    with open("manual_sekiro/data/items.json", "x", encoding = "utf-8") as file:
        file.write('{\n')
        file.write('    "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.items.schema.json",\n')
        file.write('    "data": [\n')
        for item in key_items:
            name = ItemLotParam[item][ItemLotParam[item].index("]") + 2:len(ItemLotParam[item])]
            file.write('        {\n')
            file.write(f'            "name": "{name}",\n')
            file.write('            "category": ["Key Items"],\n')
            file.write('            "count": 1,\n')
            if item == 3060 or item == 61600:
                file.write('            "early": true,\n')
            file.write('            "progression": true\n')
            file.write('        },\n')
        for name in names:
            file.write('        {\n')
            file.write(f'            "name": "{name}",\n')
            file.write(f'            "category": ["{item_category[name]}"],\n')
            if item_category[name] in categories:
                file.write('            "useful": true,\n')
            file.write(f'            "count": {count[name]}\n')
            file.write('        },\n')
        file.write('        {\n')
        file.write('            "name": "Victory",\n')
        file.write('            "category": ["Victory"],\n')
        file.write('            "count": 1,\n')
        file.write('            "progression": true\n')
        file.write('        }\n')
        file.write('    ]\n')
        file.write('}')
        print("items.json Written")