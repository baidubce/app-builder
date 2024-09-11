def pretty_print_dict(kv_dict, header=["新增Components Name", "Error Message"]):
    """
    格式化打印字典，生成一个带边框的表格字符串。
    
    Args:
        kv_dict (dict): 需要打印的字典，格式为{key: value}。
        header (list, optional): 表格头部，格式为["Key", "Value"]。默认为["Key", "Value"]。
    
    Returns:
        str: 格式化后的表格字符串。
    
    """
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
        if k == "Component Name":
            continue
        if k == "None":
            continue
        if isinstance(v, str) and len(v) >= max_v:
            str_v = "... " + v[-46:]
        else:
            str_v = v
        draws += l_format.format(k, " " * spacing, str(str_v))
    
    draws += back_border

    _str = "\n{}\n".format(draws)
    return _str

def read_error_file(filename):
    """
    读取指定格式的错误文件，并返回键值对字典和表头信息
    
    Args:
        filename (str): 错误文件路径
    
    Returns:
        Tuple[Dict[str, str], List[str]]: 返回一个包含键值对字典和表头信息的元组
            - 键值对字典（Dict[str, str]）：以文件中第二列作为键，第一列作为值构建的字典
            - 表头信息（List[str]）：文件中的第一行数据，经过去除首尾空格和按制表符分割后的列表
    
    """
    kv_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().split('\t')
        for line in lines[1:]: 
            components = line.strip().split('\t')
            if len(components) == 2:
                kv_dict[components[0]] = components[1]
    return kv_dict, header

def read_error_file_new(filename):
    """
    读取指定格式的错误文件，并返回键值对字典和表头信息
    
    Args:
        filename (str): 错误文件路径
    
    Returns:
        Tuple[Dict[str, str], List[str]]: 返回一个包含键值对字典和表头信息的元组
            - 键值对字典（Dict[str, str]）：以文件中第二列作为键，第一列作为值构建的字典
            - 表头信息（List[str]）：文件中的第一行数据，经过去除首尾空格和按制表符分割后的列表
    
    """
    kv_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines: 
            components = line.strip().split('\t')
            if len(components) == 2:
                kv_dict[components[0]] = components[1]
    return kv_dict

if __name__ == "__main__":
    filename = 'components_error_info.txt' 
    components_test_txt = 'new_add_components_error_info.txt'
    kv_dict_1, header_1 = read_error_file(filename)
    kv_dict_2 = read_error_file_new(components_test_txt)
    print("存在tool_eval方法与manifest成员变量但是不符合规范的Components组件如下[全量检测，包含白名单]:\n")
    print(pretty_print_dict(kv_dict_1, header=header_1))
    print("新增的Components组件tool_eval方法与manifest成员变量检测[增量检测，排除白名单]\n")
    print(pretty_print_dict(kv_dict_2))
    print("Components组件开发规范详见:\nhttps://github.com/baidubce/app-builder/blob/master/docs/develop_guide/components_guidelines.md")