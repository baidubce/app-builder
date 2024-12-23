import os

def pretty_print_dict(kv_dict, header=["Key", "Value"]):
    spacing = 2
    max_k = 25
    max_v = 80

    for k, v in kv_dict.items():
        max_k = max(max_k, len(k))

    h_format = "    " + "{{:^{}s}}{}{{:^{}s}}\n".format(max_k, " " * spacing,
                                                          max_v)
    l_format = "    " + "{{:^{}s}}{{}}{{:<{}s}}\n".format(max_k, max_v)
    length = max_k + max_v + spacing

    front_border = "    ╔" + "".join(["═"] * length) + "╗"
    line = "    ╠" + "".join(["═"] * length) + "╣"
    back_border = "    ╚" + "".join(["═"] * length) + "╝"

    draws = ""
    draws += front_border + "\n"

    draws += h_format.format(header[0], header[1])

    draws += line + "\n"

    for k, v in kv_dict.items():
        if isinstance(v, str) and len(v) >= max_v:
            str_v = "... " + v[-46:]
        else:
            str_v = v
        draws += l_format.format(k, " " * spacing, str(str_v))
    
    draws += back_border

    _str = "\n{}\n".format(draws)
    return _str


def read_error_file(filename):
    kv_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().split('\t')
        for line in lines[1:-3]: 
            components = line.strip().split('\t')
            if len(components) == 2:
                kv_dict[components[0]] = components[1]
    return kv_dict, header


if __name__ == "__main__":
    if os.path.exists('components_error_info.txt'):
        print("旧组件:")
        filename = 'components_error_info.txt' 
        kv_dict, header = read_error_file(filename)
        print(pretty_print_dict(kv_dict, header=header))
    if os.path.exists('v2_components_error_info.txt'):
        print("v2组件:")
        filename = 'v2_components_error_info.txt' 
        kv_dict, header = read_error_file(filename)
        print(pretty_print_dict(kv_dict, header=header))