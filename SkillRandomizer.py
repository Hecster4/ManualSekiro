import struct
from SkillCatergories import skills, mushin, prosthetics
from random import choice
from CompressDCX import compress_dcx_content
from os import path, remove

skill_param_offset = 0x54b410

def randomize_skill_param(content):
    skill_ids: list = []
    offsets: dict = {}
    data_modified: dict = {}
    data_original: dict = {}
    rows = struct.unpack_from("H", content, skill_param_offset + 10)[0]
    offset = skill_param_offset + 0x40
    while len(skill_ids) < rows:
        skill_id = struct.unpack_from("Q", content, offset)[0]
        skill_ids.append(skill_id)
        offsets[skill_id] = struct.unpack_from("QQ", content, offset + 8)
        data_original[skill_id] = list(struct.unpack_from("i i 3i i i 3i h h i i b 2B B 8i 8B", content, offsets[skill_id][0] + skill_param_offset))
        data_modified[skill_id] = data_original[skill_id].copy()
        offset += struct.calcsize("QQQ")
    skills_original = skills.copy()
    for skill in skills_original:
        random_skill = choice(skills)
        skills.remove(random_skill)
        data_modified[skill][0:2] = data_original[random_skill][0:2]
        data_modified[skill][5:10] = data_original[random_skill][5:10]
        data_modified[skill][12:14] = data_original[random_skill][12:14]
        data_modified[skill][15:17] = data_original[random_skill][15:17]
    for skill in mushin:
        data_modified[skill][0:2] = data_modified[mushin[skill]][0:2]
        data_modified[skill][5:10] = data_modified[mushin[skill]][5:10]
        data_modified[skill][12:14] = data_modified[mushin[skill]][12:14]
        data_modified[skill][15:17] = data_modified[mushin[skill]][15:17]
    prosthetics_original = prosthetics.copy()
    for prosthetic in prosthetics_original:
        random_prosthetic = choice(prosthetics)
        prosthetics.remove(random_prosthetic)
        data_modified[prosthetic][0:2] = data_original[random_prosthetic][0:2]
        data_modified[prosthetic][5:10] = data_original[random_prosthetic][5:10]
        data_modified[prosthetic][12:14] = data_original[random_prosthetic][12:14]
        data_modified[prosthetic][15:17] = data_original[random_prosthetic][15:17]
    skill_param = content[skill_param_offset: skill_param_offset + 0x40]
    offset = skill_param_offset + 0x40
    for skill_id in skill_ids:
        skill_param += struct.pack("QQQ", skill_id, *offsets[skill_id])
        offset += struct.calcsize("QQQ")
    for skill_id in skill_ids:
        skill_param += struct.pack("i i 3i i i 3i h h i i b 2B B 8i 8B", *data_modified[skill_id])
        offset += struct.calcsize("i i 3i i i 3i h h i i b 2B B 8i 8B")
    return skill_param, offset

def main():
    with open("gameparam.parambnd", "rb") as file:
        content = file.read()
    param = content[0: skill_param_offset]
    skill_param, offset = randomize_skill_param(content)
    param += skill_param
    param += content[offset: len(content)]
    compressed_param = compress_dcx_content(param)
    if path.exists("param/gameparam/gameparam.parambnd.dcx"):
        remove("param/gameparam/gameparam.parambnd.dcx")
    with open("param/gameparam/gameparam.parambnd.dcx", "xb") as file:
        file.write(compressed_param)
    print("gameparam.parambnd.dcx Written")
        
if __name__ == "__main__":
    main()