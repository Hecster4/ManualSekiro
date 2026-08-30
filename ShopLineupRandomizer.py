import struct
from ShopLineupCategories import randomized_shops, dragon_tally_board, pot_nobles, infinite_shops, discounted_shop_lineups,\
     coin_purses
from random import choice
from CompressDCX import compress_dcx_content
from os import path, remove

shop_lineup_param_offset = 0x53f9f0

def randomize_shop_lineup_param(content):
    shop_lineup_ids: list = []
    offsets: dict = {}
    data_modified: dict = {}
    data_original: dict = {}
    rows = struct.unpack_from("H", content, shop_lineup_param_offset + 10)[0]
    offset = shop_lineup_param_offset + 0x40
    while len(shop_lineup_ids) < rows:
        shop_lineup_id = struct.unpack_from("Q", content, offset)[0]
        offsets[shop_lineup_id] = struct.unpack_from("QQ", content, offset + 8)
        shop_lineup_ids.append(shop_lineup_id)
        data_original[shop_lineup_id] = list(struct.unpack_from("i i i i i h B B h 2B i f", content, offsets[shop_lineup_id][0] + shop_lineup_param_offset))
        data_modified[shop_lineup_id] = data_original[shop_lineup_id].copy()
        offset += struct.calcsize("QQQ")
    random_shop_lineup_ids = randomized_shops.copy()
    for shop_lineup_id in pot_nobles:
        random_shop_lineup_ids.append(shop_lineup_id)
    for shop_lineup_id in pot_nobles:
        while True:
            random_shop_lineup_id = choice(random_shop_lineup_ids)
            quantity = 1
            if shop_lineup_id == 2500001:
                quantity = 2
            if data_original[random_shop_lineup_id][5] == quantity:
                break
        random_shop_lineup_ids.remove(random_shop_lineup_id)
        data_modified[shop_lineup_id][0] = data_original[random_shop_lineup_id][0]
        data_modified[shop_lineup_id][3] = data_original[random_shop_lineup_id][3]
    for shop_lineup_id in pot_nobles:
        data_modified[pot_nobles[shop_lineup_id]][0] = data_modified[shop_lineup_id][0]
        data_modified[pot_nobles[shop_lineup_id]][3] = data_modified[shop_lineup_id][3]
    for shop_lineup_id in randomized_shops:
        random_shop_lineup_id = choice(random_shop_lineup_ids)
        random_shop_lineup_ids.remove(random_shop_lineup_id)
        data_modified[shop_lineup_id][0] = data_original[random_shop_lineup_id][0]
        data_modified[shop_lineup_id][1] = data_original[random_shop_lineup_id][1]
        data_modified[shop_lineup_id][3] = data_original[random_shop_lineup_id][3]
        data_modified[shop_lineup_id][5] = data_original[random_shop_lineup_id][5]
        if random_shop_lineup_id in pot_nobles:
            data_modified[shop_lineup_id][1] = -1
    data_modified[1100100] = data_modified[1100000]
    for shop_lineup_id in dragon_tally_board:
        for shop_lineup in dragon_tally_board[shop_lineup_id]:
            data_modified[shop_lineup] = data_modified[shop_lineup_id]
    for shop_lineup_id in discounted_shop_lineups:
        data_modified[shop_lineup_id] = data_modified[shop_lineup_id - 50].copy()
        if data_modified[shop_lineup_id][1] != -1:
            data_modified[shop_lineup_id][1] = int(data_modified[shop_lineup_id][1] * .9)
            if data_modified[shop_lineup_id][0] in coin_purses:
                data_modified[shop_lineup_id][1] = coin_purses[data_modified[shop_lineup_id][0]]
    shop_lineup_param = content[shop_lineup_param_offset: shop_lineup_param_offset + 0x40]
    offset = shop_lineup_param_offset + 0x40
    for shop_lineup_id in shop_lineup_ids:
        shop_lineup_param += struct.pack("QQQ", shop_lineup_id, *offsets[shop_lineup_id])
        offset += struct.calcsize("QQQ")
    for shop_lineup_id in shop_lineup_ids:
        shop_lineup_param += struct.pack("i i i i i h B B h 2B i f", *data_modified[shop_lineup_id])
        offset += struct.calcsize("i i i i i h B B h 2B i f")
    return shop_lineup_param, offset
        
def main():
    with open("gameparam.parambnd", "rb") as file:
        content = file.read()
    param = content[0:shop_lineup_param_offset]
    shop_lineup_param, offset = randomize_shop_lineup_param(content)
    param += shop_lineup_param
    param += content[offset:len(content)]
    compressed_param = compress_dcx_content(param)
    if path.exists("param/gameparam/gameparam.parambnd.dcx"):
        remove("param/gameparam/gameparam.parambnd.dcx")
    with open("param/gameparam/gameparam.parambnd.dcx", "xb") as file:
        file.write(compressed_param)
    print("gameparam.parambnd.dcx Written")
    
if __name__ == "__main__":
    main()