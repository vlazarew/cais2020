import argparse
import json
import sys


class Register:
    base = ""
    mask = 0

    def __init__(self, base, mask):
        self.base = base
        self.mask = mask


MASK_64BITR = 0xFFFFFFFFFFFFFFFF
MASK_32BITE = 0x00000000FFFFFFFF
MASK_16BITX = 0x000000000000FFFF
MASK_8BITL = 0x00000000000000FF
MASK_8BITH = 0x000000000000FF00

REGISTERS_DICTIONARY = {
    "rax": Register("rax", MASK_64BITR), "eax": Register("rax", MASK_32BITE), "ax": Register("rax", MASK_16BITX),
    "al": Register("rax", MASK_8BITL), "ah": Register("rax", MASK_8BITH),
    "rbx": Register("rbx", MASK_64BITR), "ebx": Register("rbx", MASK_32BITE), "bx": Register("rbx", MASK_16BITX),
    "bl": Register("rbx", MASK_8BITL), "bh": Register("rbx", MASK_8BITH),
    "rcx": Register("rcx", MASK_64BITR), "ecx": Register("rcx", MASK_32BITE), "cx": Register("rcx", MASK_16BITX),
    "cl": Register("rcx", MASK_8BITL), "ch": Register("rcx", MASK_8BITH),
    "rdx": Register("rdx", MASK_64BITR), "edx": Register("rdx", MASK_32BITE), "dx": Register("rdx", MASK_16BITX),
    "dl": Register("rdx", MASK_8BITL), "dh": Register("rdx", MASK_8BITH),

    "rsp": Register("rsp", MASK_64BITR), "esp": Register("rsp", MASK_32BITE), "sp": Register("rsp", MASK_16BITX),
    "spl": Register("rsp", MASK_8BITL),
    "rbp": Register("rbp", MASK_64BITR), "ebp": Register("rbp", MASK_32BITE), "bp": Register("rbp", MASK_16BITX),
    "bpl": Register("rbp", MASK_8BITL),
    "rsi": Register("rsi", MASK_64BITR), "esi": Register("rsi", MASK_32BITE), "si": Register("rsi", MASK_16BITX),
    "sil": Register("rsi", MASK_8BITL),
    "rdi": Register("rdi", MASK_64BITR), "edi": Register("rdi", MASK_32BITE), "di": Register("rdi", MASK_16BITX),
    "dil": Register("rdi", MASK_8BITL),

    "r8": Register("r8", MASK_64BITR), "r8d": Register("r8", MASK_32BITE), "r8w": Register("r8", MASK_16BITX),
    "r8b": Register("r8", MASK_8BITL),
    "r9": Register("r9", MASK_64BITR), "r9d": Register("r9", MASK_32BITE), "r9w": Register("r9", MASK_16BITX),
    "r9b": Register("r9", MASK_8BITL),
    "r10": Register("r10", MASK_64BITR), "r10d": Register("r10", MASK_32BITE), "r10w": Register("r10", MASK_16BITX),
    "r10b": Register("r10", MASK_8BITL),
    "r11": Register("r11", MASK_64BITR), "r11d": Register("r11", MASK_32BITE), "r11w": Register("r11", MASK_16BITX),
    "r11b": Register("r11", MASK_8BITL),
    "r12": Register("r12", MASK_64BITR), "r12d": Register("r12", MASK_32BITE), "r12w": Register("r12", MASK_16BITX),
    "r12b": Register("r12", MASK_8BITL),
    "r13": Register("r13", MASK_64BITR), "r13d": Register("r13", MASK_32BITE), "r13w": Register("r13", MASK_16BITX),
    "r13b": Register("r13", MASK_8BITL),
    "r14": Register("r14", MASK_64BITR), "r14d": Register("r14", MASK_32BITE), "r14w": Register("r14", MASK_16BITX),
    "r14b": Register("r14", MASK_8BITL),
    "r15": Register("r15", MASK_64BITR), "r15d": Register("r15", MASK_32BITE), "r15w": Register("r15", MASK_16BITX),
    "r15b": Register("r15", MASK_8BITL),

    "rflags": Register("rflags", MASK_64BITR), "eflags": Register("rflags", MASK_32BITE),
    "flags": Register("rflags", MASK_16BITX)
}

REGISTERS_PARTS = {
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

MARKED_REGISTERS = {
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


def is_mov(instruction):
    command = instruction["text"][:4]
    return (command == "cmov" or command[:3] == "mov")


def taint_register(register):
    r = REGISTERS_DICTIONARY.get(register)
    if r != None:
        REGISTERS_DICTIONARY[r.base] |= r.mask


def untaint_register(register):
    r = REGISTERS_DICTIONARY.get(register)
    if r != None:
        REGISTERS_DICTIONARY[r.base] &= ~(r.mask)


tainted_memory = set()


def taint_slice(start, length):
    for i in range(start, start + length):
        tainted_memory.add(i)


def untaint_slice(start, length):
    for i in range(start, start + length):
        tainted_memory.discard(i)


def unite(fragments_set):
    if len(fragments_set) == 0:
        return []
    fragments_list = list(fragments_set)
    fragments_list.sort()
    start = fragments_list[0]
    length = 1
    united = []
    for fragment in fragments_list[1:]:
        if fragment == start + length:
            length += 1
        else:
            united.append([start, length])
            start = fragment
            length = 1
    united.append([start, length])
    return united


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

    index = 0
    result = []
    for i, instruction in enumerate(input_data):
        while index < len(test_data) and i == test_data[index]["step"]:
            if test_data[index]["type"] == "source":
                for item in test_data[index]["taint"]:
                    if type(item) is str:
                        taint_register(item)
                    else:
                        taint_slice(item[0], item[1])
            else:
                answer = []
                for base_register, value in MARKED_REGISTERS.items():
                    saved_value = value
                    for register in REGISTERS_PARTS[base_register]:
                        if saved_value & MARKED_REGISTERS[register].mask == MARKED_REGISTERS[register].mask:
                            answer.append(register)
                            saved_value &= ~(MARKED_REGISTERS[register].mask)
                    if (saved_value != 0):
                        tainted_bytes = []
                        for j in range(0, 8):
                            mask = MASK_8BITL << (j * 8)
                            if saved_value & mask == mask:
                                tainted_bytes.append(j)
                        for base, value in unite(tainted_bytes):
                            answer.append([base_register, base, value])
                for address, value in unite(tainted_memory):
                    answer.append([address, value])
                result.append({"step": i, "answer": answer})
            index += 1
        tainted = False
        for register in instruction["readRegs"]:
            r = REGISTERS_DICTIONARY.get(register)
            if r != None:
                tainted = tainted or (REGISTERS_DICTIONARY[r.base] & r.mask != 0)
        for memory_slice in instruction["readMem"]:
            for byte in range(memory_slice[0], memory_slice[0] + memory_slice[1]):
                tainted = tainted or (byte in tainted_memory)
        if tainted:
            for item in instruction["writeRegs"]:
                taint_register(item)
            for item in instruction["writtenMem"]:
                taint_slice(item[0], item[1])
        elif is_mov(instruction):
            for item in instruction["writeRegs"]:
                untaint_register(item)
            for item in instruction["writtenMem"]:
                untaint_slice(item[0], item[1])

    with open(output_JSON, 'w') as f:
        json.dump(result, f)
    print("Success")

main()