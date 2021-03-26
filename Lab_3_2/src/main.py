import argparse
import json


class Reg:
    ParentName: str
    MASK: int

    def __init__(self, ParentName: str, MASK: int):
        self.ParentName = ParentName
        self.MASK = MASK


MARKED_MEMORY = set()

MASK_64BIT = 0xFFFFFFFFFFFFFFFF
MASK_32BIT = 0x00000000FFFFFFFF
MASK_16BIT = 0x000000000000FFFF
MASK_8BITR = 0x00000000000000FF
MASK_8BITL = 0x000000000000FF00

REGS_DICT = {
    "rax": Reg("rax", MASK_64BIT), "eax": Reg("rax", MASK_32BIT), "ax": Reg("rax", MASK_16BIT),
    "al": Reg("rax", MASK_8BITR), "ah": Reg("rax", MASK_8BITL),
    "rbx": Reg("rbx", MASK_64BIT), "ebx": Reg("rbx", MASK_32BIT), "bx": Reg("rbx", MASK_16BIT),
    "bl": Reg("rbx", MASK_8BITR), "bh": Reg("rbx", MASK_8BITL),
    "rcx": Reg("rcx", MASK_64BIT), "ecx": Reg("rcx", MASK_32BIT), "cx": Reg("rcx", MASK_16BIT),
    "cl": Reg("rcx", MASK_8BITR), "ch": Reg("rcx", MASK_8BITL),
    "rdx": Reg("rdx", MASK_64BIT), "edx": Reg("rdx", MASK_32BIT), "dx": Reg("rdx", MASK_16BIT),
    "dl": Reg("rdx", MASK_8BITR), "dh": Reg("rdx", MASK_8BITL),

    "rsp": Reg("rsp", MASK_64BIT), "esp": Reg("rsp", MASK_32BIT), "sp": Reg("rsp", MASK_16BIT),
    "spl": Reg("rsp", MASK_8BITR),
    "rbp": Reg("rbp", MASK_64BIT), "ebp": Reg("rbp", MASK_32BIT), "bp": Reg("rbp", MASK_16BIT),
    "bpl": Reg("rbp", MASK_8BITR),
    "rsi": Reg("rsi", MASK_64BIT), "esi": Reg("rsi", MASK_32BIT), "si": Reg("rsi", MASK_16BIT),
    "sil": Reg("rsi", MASK_8BITR),
    "rdi": Reg("rdi", MASK_64BIT), "edi": Reg("rdi", MASK_32BIT), "di": Reg("rdi", MASK_16BIT),
    "dil": Reg("rdi", MASK_8BITR),

    "r8": Reg("r8", MASK_64BIT), "r8d": Reg("r8", MASK_32BIT), "r8w": Reg("r8", MASK_16BIT),
    "r8b": Reg("r8", MASK_8BITR),
    "r9": Reg("r9", MASK_64BIT), "r9d": Reg("r9", MASK_32BIT), "r9w": Reg("r9", MASK_16BIT),
    "r9b": Reg("r9", MASK_8BITR),
    "r10": Reg("r10", MASK_64BIT), "r10d": Reg("r10", MASK_32BIT), "r10w": Reg("r10", MASK_16BIT),
    "r10b": Reg("r10", MASK_8BITR),
    "r11": Reg("r11", MASK_64BIT), "r11d": Reg("r11", MASK_32BIT), "r11w": Reg("r11", MASK_16BIT),
    "r11b": Reg("r11", MASK_8BITR),
    "r12": Reg("r12", MASK_64BIT), "r12d": Reg("r12", MASK_32BIT), "r12w": Reg("r12", MASK_16BIT),
    "r12b": Reg("r12", MASK_8BITR),
    "r13": Reg("r13", MASK_64BIT), "r13d": Reg("r13", MASK_32BIT), "r13w": Reg("r13", MASK_16BIT),
    "r13b": Reg("r13", MASK_8BITR),
    "r14": Reg("r14", MASK_64BIT), "r14d": Reg("r14", MASK_32BIT), "r14w": Reg("r14", MASK_16BIT),
    "r14b": Reg("r14", MASK_8BITR),
    "r15": Reg("r15", MASK_64BIT), "r15d": Reg("r15", MASK_32BIT), "r15w": Reg("r15", MASK_16BIT),
    "r15b": Reg("r15", MASK_8BITR),

    "rflags": Reg("rflags", MASK_64BIT), "eflags": Reg("rflags", MASK_32BIT), "flags": Reg("rflags", MASK_16BIT)
}

REGS_PARTS = {
    "rax": ["rax", "eax", "ax", "al", "ah"],
    "rbx": ["rbx", "ebx", "bx", "bl", "bh"],
    "rcx": ["rcx", "ecx", "cx", "cl", "ch"],
    "rdx": ["rdx", "edx", "dx", "dl", "dh"],

    "rsp": ["rsp", "esp", "sp", "spl"],
    "rbp": ["rbp", "ebp", "bp", "bpl"],
    "rsi": ["rsi", "esi", "si", "sil"],
    "rdi": ["rdi", "edi", "di", "dil"],

    "r8": ["r8", "r8d", "r8w", "r8b"],
    "r9": ["r9", "r9d", "r9w", "r9b"],
    "r10": ["r10", "r10d", "r10w", "r10b"],
    "r11": ["r11", "r11d", "r11w", "r11b"],
    "r12": ["r12", "r12d", "r12w", "r12b"],
    "r13": ["r13", "r13d", "r13w", "r13b"],
    "r14": ["r14", "r14d", "r14w", "r14b"],
    "r15": ["r15", "r15d", "r15w", "r15b"],

    "rflags": ["rflags", "eflags", "flags"]
}

MARKED_REGS = {
    "rax": 0,
    "rbx": 0,
    "rcx": 0,
    "rdx": 0,

    "rsp": 0,
    "rbp": 0,
    "rsi": 0,
    "rdi": 0,

    "r8": 0,
    "r9": 0,
    "r10": 0,
    "r11": 0,
    "r12": 0,
    "r13": 0,
    "r14": 0,
    "r15": 0,

    "rflags": 0
}


def mark_address(address, shift):
    for i in range(address, address + shift):
        MARKED_MEMORY.add(i)


def mark_addresses(mems):
    for item in mems:
        mark_address(item[0], item[1])


def unmark_address(address, shift):
    for i in range(address, address + shift):
        MARKED_MEMORY.discard(i)


def unmark_addresses(mems):
    for item in mems:
        unmark_address(item[0], item[1])


def mark_reg(reg_name: str):
    reg = REGS_DICT.get(reg_name, None)
    if reg:
        MARKED_REGS[reg.ParentName] |= reg.MASK


def mark_regs(reg_names):
    for reg_name in reg_names:
        mark_reg(reg_name)


def unmark_reg(reg_name: str):
    reg = REGS_DICT.get(reg_name, None)
    if reg:
        MARKED_REGS[reg.ParentName] &= ~reg.MASK


def unmark_regs(reg_names):
    for reg_name in reg_names:
        unmark_reg(reg_name)


def mark(for_mark):
    for item in for_mark:
        if isinstance(item, str):
            mark_reg(item)
        else:
            mark_address(item[0], item[1])


def merge(marked_memory):
    if len(marked_memory) == 0:
        return list()
    marked_memory_list = list(marked_memory)
    marked_memory_list.sort()
    base_address = marked_memory_list[0]
    curr_shift = 1
    merged_marked_memory = list()
    for address in marked_memory_list[1:]:
        if address - (base_address + curr_shift) == 0:
            curr_shift += 1
        else:
            merged_marked_memory.append([base_address, curr_shift])
            base_address = address
            curr_shift = 1
    merged_marked_memory.append([base_address, curr_shift])
    return merged_marked_memory


ANSWERS = list()


def print_res(step):
    result = list()
    for parent_reg_name, value in MARKED_REGS.items():
        value_copy = value
        for reg_name in REGS_PARTS[parent_reg_name]:
            if value_copy & REGS_DICT[reg_name].MASK == REGS_DICT[reg_name].MASK:
                result.append(reg_name)
                value_copy &= ~REGS_DICT[reg_name].MASK
        if value_copy != 0:
            marked_bytes = list()
            for i in range(0, 8):
                MASK = MASK_8BITR << (i * 8)
                if value_copy & MASK == MASK:
                    marked_bytes.append(i)
            merged_marked_bytes = merge(marked_bytes)
            for base, value in merged_marked_bytes:
                result.append([parent_reg_name, base, value])

    for address, value in merge(MARKED_MEMORY):
        result.append([address, value])

    ANSWERS.append({"step": step, "answer": result})


def isMov(inst):
    com = inst["text"].split()[0]
    return com in {"mov", "cmov", "movz", "movs"}


def propagate(inst):
    marked = False
    for reg_name in inst["readRegs"]:
        reg = REGS_DICT.get(reg_name, None)
        if (reg == None):
            continue
        marked = marked or (MARKED_REGS[reg.ParentName] & reg.MASK != 0)
    for mem in inst["readMem"]:
        for address in range(mem[0], mem[0] + mem[1]):
            marked = marked or (address in MARKED_MEMORY)

    if marked:
        mark_regs(inst["writeRegs"])
        mark_addresses(inst["writtenMem"])
    elif isMov(inst):
        unmark_regs(inst["writeRegs"])
        unmark_addresses(inst["writtenMem"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--test")

    args = parser.parse_args()
    input_JSON = args.input
    output_JSON = args.output
    test_JSON = args.test

    with open(input_JSON, "r") as read_file:
        input_data = json.load(read_file)

    with open(test_JSON, "r") as read_file:
        test_data = json.load(read_file)

    curr_test = 0
    for i, inst in enumerate(input_data):
        # if i == 109:
        #     ww = 1
        while curr_test < len(test_data) and i == test_data[curr_test]["step"]:
            if test_data[curr_test]["type"] == "source":
                mark(test_data[curr_test]["taint"])
            else:
                print_res(i)
            curr_test += 1
        propagate(inst)

    with open(output_JSON, 'w') as f:
        json.dump(ANSWERS, f)
    print("Success")


main()
