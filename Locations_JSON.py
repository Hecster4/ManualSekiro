from ItemCategories import important_items, key_items, missable_items
from ParamNames import ItemLotParam
from os import path, remove

regions =  {"Aromatic Branch": [2040, 2041, 2060, 2061, 2070, 2071, 62306, 63600, 63650, 2500000, 2500020, 2500650, 10212100,
                               10701000, 10801000, 13100000, 13401000, 13800000, 13800001, 14001000, 50500000],
            "Father's Bell Charm": [2100, 2101, 10700100, 14703100, 14703101],
            "Gatehouse Key": [1120010],
            "Gun Fort Shrine Key": [2010, 2011, 2015, 2016, 2017, 2200, 1700000, 1700810],
            "Hidden Temple Key": [2030, 2031],
            "Invasion": [2090, 2091, 2120, 2121, 62302, 14700000, 14700001, 14701000, 14701001, 50200000, 50200001],
            "Mibu Breathing Technique": [1500320, 2000040, 13200100, 13400000, 13502000],
            "Puppeteer Ninjutsu": [50100000],
            "Secret Passage Key": [2130, 2131],
            "Shinobi Prosthetic": [2000, 2001, 2020, 2021, 2050, 2051, 2080, 2081,
                                           61000, 61004, 61600, 62200, 62404, 62406,
                                           63200, 1100000, 1100200, 1100310, 1110010, 1110020, 1110170, 1110860,
                                           1500000, 1500010, 1500040, 1500050, 1700010, 1700020, 1700030, 1700040,
                                           1700820, 2000000, 2000030, 2000170, 2000730, 10200000, 10200001,
                                           10200100, 10202000, 10212000, 10400000, 10400001, 10401100, 10401101, 10101400, 10702000, 10702001, 10800000,
                                           11300000, 11300001, 11900000, 11901100, 13500000, 13501000, 13700000,
                                           13700001, 14000000, 14702000, 14702001, 50201000, 50201001, 70000000, 70000001],
            "Slender Finger": [10802000],
            "Start": [3060, 10203000],
            "Young Lord's Bell Charm": [61200, 1000000, 1000010, 1000020, 1000500, 10500000, 10700000, 10700001]}

requires = {"Puppeteer Ninjutsu": [1700810],
            "Mibu Breathing Technique": [2040, 2041, 2070, 2071, 62306, 2500000, 2500020, 2500650, 10212100, 10701000, 13401000, 14001000],
            "Mortal Blade": [2200, 10802000],
            "Shinobi Prosthetic": [1000020, 1000500, 10700000, 10700001]}


def write_locations_json():
    if path.exists("manual_sekiro/data/locations.json"):
        remove("manual_sekiro/data/locations.json")
    with open("manual_sekiro/data/locations.json", "x", encoding = "utf-8") as file:
        file.write('{\n')
        file.write('    "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.items.schema.json",\n')
        file.write('    "data": [\n')
        for item in key_items:
            name = ItemLotParam[item][ItemLotParam[item].index("["):len(ItemLotParam[item])]
            file.write('        {\n')
            file.write(f'            "name": "{name}",\n')
            file.write(f'            "category": ["{ItemLotParam[item][ItemLotParam[item].index(":") + 2:ItemLotParam[item].index("]")]}"],\n')
            if item in missable_items:
                file.write('            "dont_place_item_category": ["Key Items"],\n') 
            for region in regions:
                if item in regions[region]:
                    file.write(f'            "region": "{region}"\n')
            file.write('        },\n')
        for item in important_items:
            file.write('        {\n')
            file.write(f'            "name": "{ItemLotParam[item][ItemLotParam[item].index("["):len(ItemLotParam[item])]}",\n')
            file.write(f'            "category": ["{ItemLotParam[item][ItemLotParam[item].index(":") + 2:ItemLotParam[item].index("]")]}"],\n')
            if item in missable_items:
                file.write('            "dont_place_item_category": ["Key Items"],\n')
            for requirment in requires:
                if item in requires[requirment]:
                    file.write(f'            "requires": "|{requirment}|",\n')
            if item == 50500000:
                file.write('            "requires": "(|Truly Precious Bait (Harunga)| or |Truly Precious Bait (Koremori)|) and |Gun Fort Shrine Key| and |Mibu Breathing Technique|",\n')
            for region in regions:
                if item in regions[region]:
                    file.write(f'            "region": "{region}"\n')
            file.write('        },\n')
        region = "Divine Dragon's Tears"
        file.write('        {\n')
        file.write('            "name": "Victory",\n')
        file.write('            "category": ["Victory"],\n')
        file.write(f'            "region": "{region}",\n')
        file.write('            "victory": true\n')
        file.write('        }\n')
        file.write('    ]\n')
        file.write('}')
        print("locations.json Written")
        
if __name__ == "__main__":
    write_locations_json()