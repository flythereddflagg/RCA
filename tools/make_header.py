import re
import pathlib

def make_header(cfile_name:str):
    with open(cfile_name) as f:
        src_file = f.read()
    prog = re.compile(r"\n[A-Za-z0-9\_]*\s[A-Za-z0-9\_\*]*\(.*\)\s\{")
    type_prog = re.compile(r"(typedef\s.*\;)|(typedef[^}]*.*\;)")
    result = prog.findall(src_file)
    types = []
    funcs = []
    lines = type_prog.findall(src_file)
    for line in lines:
        l1, l2 = line
        if l1:
            types.append(l1.strip())
        if l2:
            types.append(l2.strip())
    for res in result:
        fw_dec = res.strip()
        fw_dec = fw_dec.replace(" {", ";")
        if fw_dec == "int main();":
            continue
        funcs.append(fw_dec)
    
    all_types = "\n".join(types)
    all_funcs = "\n".join(funcs)
    hfile = cfile_name.replace(".c", ".h")
    hguard = hfile.upper().replace(".", "_").split("/")[-1]
    file_text = f"""#ifndef __{hguard}__
#define __{hguard}__

{all_types}

{all_funcs}

#endif
    """
    return file_text
    
print(make_header("./csrc/node.c"))

for filename in pathlib.Path('./csrc/').glob("*.c"):
    print(filename)
    file_txt = make_header(str(filename))
    with open(str(filename).replace(".c", ".h"), 'w') as f:
        f.write(file_txt)
