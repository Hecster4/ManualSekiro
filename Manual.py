from CompressDCX import compress_dcx_content
from os import path, remove
from ItemLotRandomizer import randomize_item_lot_param, item_lot_id_param_offset
from ShopLineupRandomizer import randomize_shop_lineup_param, shop_lineup_param_offset
from SkillRandomizer import randomize_skill_param, skill_param_offset
from Zipfile import zipfile_dir

def manual_randomizer():
    with open('gameparam.parambnd', 'rb') as file:
        content = file.read()
    gameparam = content[0:item_lot_id_param_offset]
    param, offset = randomize_item_lot_param(content)
    gameparam += param
    gameparam += content[offset:shop_lineup_param_offset]
    param, offset = randomize_shop_lineup_param(content)
    gameparam += param
    gameparam += content[offset:skill_param_offset]
    param, offset = randomize_skill_param(content)
    gameparam += param
    gameparam += content[offset:len(content)]
    compressed_gameparam = compress_dcx_content(gameparam)
    if path.exists('param/gameparam/gameparam.parambnd.dcx'):
        remove('param/gameparam/gameparam.parambnd.dcx')
    with open('param/gameparam/gameparam.parambnd.dcx', "xb") as file:
        file.write(compressed_gameparam)
    print("gameparam.parambnd.dcx Written")
    zipfile_dir('manual_sekiro')
    
if __name__ == "__main__":
    manual_randomizer()