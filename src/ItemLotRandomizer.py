import struct
from os import path, remove
from random import choice
from CompressDCX import compress_dcx_content
from Locations_JSON import write_locations_json
from Item_JSON import write_items_json
from ItemCategories import randomized_items, key_items, memories, skills_and_prosthetics, health_and_healing_upgrades, \
     important_items

item_lot_id_param_offset = 0x30a5e0

def randomize_item_lot_param(content):
    offsets: dict = {}
    item_lot_ids: list = []
    data_original: dict = {}
    data_modified: dict = {}
    replacments: dict = {}
    
    rows = struct.unpack_from("H", content, item_lot_id_param_offset + 10)[0]
    offset = item_lot_id_param_offset + 0x40
    while len(item_lot_ids) < rows:
        item_lot_id = struct.unpack_from("Q", content, offset)[0]
        item_lot_ids.append(item_lot_id)
        offsets[item_lot_id] = struct.unpack_from("QQ", content, offset + 8)
        data_original[item_lot_id] = list(struct.unpack_from("8i 8i 8H 8H 8i i i B B B 7B c c b B H 8H", content, offsets[item_lot_id][0] + item_lot_id_param_offset))
        data_modified[item_lot_id] = data_original[item_lot_id].copy()
        offset += struct.calcsize("QQQ")
    locations = randomized_items + memories + skills_and_prosthetics + health_and_healing_upgrades
    for item_lot_id in randomized_items + memories + skills_and_prosthetics + health_and_healing_upgrades:
        random_location = choice(locations)
        locations.remove(random_location)
        data_modified[random_location][0:40] = data_original[item_lot_id][0:40]
        data_modified[random_location][41:65] = data_original[item_lot_id][41:65]
        replacments[random_location] = item_lot_id
    for item_lot_id in important_items + key_items:
        data_modified[item_lot_id][0] = 11500
        for i in range(1,8):
            data_modified[item_lot_id][i] = 0
        data_modified[item_lot_id][8] = 1073741824
        for i in range(9, 16):
            data_modified[item_lot_id][i] = 0
        data_modified[item_lot_id][16] = 1000
        for i in range(17, 24):
            data_modified[item_lot_id][i] = 0
        data_modified[item_lot_id][57] = 1
        for i in range(58, 65):
            data_modified[item_lot_id][i] = 0
    write_items_json(replacments)
    offset = item_lot_id_param_offset + 0x40
    param = content[item_lot_id_param_offset:offset]
    for item_lot_id in item_lot_ids:
        param += struct.pack("QQQ", item_lot_id, *offsets[item_lot_id])
        offset += struct.calcsize("QQQ")
    for item_lot_id in item_lot_ids:
        param += struct.pack("8i 8i 8H 8H 8i i i B B B 7B c c b B H 8H", *data_modified[item_lot_id])
        offset += struct.calcsize("8i 8i 8H 8H 8i i i B B B 7B c c b B H 8H")
    return param, offset
    
if __name__ == "__main__":
    with open("gameparam.parambnd", "rb") as file:
        content = file.read()
    param = content[0:item_lot_id_param_offset]
    item_lot_id_param, offset = randomize_item_lot_param(content)
    param += item_lot_id_param
    param += content[offset:len(content)]
    compressed_param = compress_dcx_content(param)
    if path.exists("param/gameparam/gameparam.parambnd.dcx"):
        remove("param/gameparam/gameparam.parambnd.dcx")
    with open("param/gameparam/gameparam.parambnd.dcx", "xb") as file:
        file.write(compressed_param)
    print("gameparam.parambnd.dcx Written")