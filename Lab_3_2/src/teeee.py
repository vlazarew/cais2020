import argparse
import copy
import json


def get_test_data_record(test_data, step, type_of_test='source'):
    for item in test_data:
        if item['type'] == type_of_test and step == item['step']:
            return item
    return None


def get_name_from_reg(reg):
    if len(reg) == 2:
        return reg[0]
    elif len(reg) == 3:
        return reg[1]


def get_weight_from_reg(reg):
    if 'l' in reg:
        return 1
    elif 'h' in reg:
        return 2
    elif 'e' in reg:
        return 4
    elif 'r' in reg:
        return 8
    else:
        return 3


class Register:
    def __init__(self, reg):
        self.fullname = reg
        self.name = get_name_from_reg(reg)
        self.weight = get_weight_from_reg(reg)
        self.l = self.weight >= 1
        self.h = self.weight >= 2
        self.x = self.weight >= 4
        self.e = self.weight >= 4
        self.r = self.weight >= 8


class Memory:
    def __init__(self, item):
        self.start_address = item[0]
        self.size = item[1]
        self.end_address = self.size + self.start_address


def add_register(item, marked_data):
    count_of_regs = 0
    temp_reg = Register(item)
    if len(marked_data) == 0:
        marked_data.append(temp_reg)
        count_of_regs += 1
    for reg in marked_data:
        if isinstance(reg, Register):
            count_of_regs += 1
            if reg.name == temp_reg.name:
                if reg.weight >= temp_reg.weight:
                    reg = temp_reg
                else:
                    reg.l = reg.l or temp_reg.l
                    reg.h = reg.h or temp_reg.h
                    reg.x = reg.x or temp_reg.x
                    reg.e = reg.e or temp_reg.e
                    reg.r = reg.r or temp_reg.r
            else:
                marked_data.append(temp_reg)

    if count_of_regs == 0:
        marked_data.append(temp_reg)


def add_memory(item, marked_data):
    count_of_mem = 0
    temp_mem = Memory(item)
    if len(marked_data) == 0:
        marked_data.append(temp_mem)
        count_of_mem += 1
    else:
        for taint in marked_data:
            if isinstance(taint, Memory):
                count_of_mem += 1
                if taint.start_address == temp_mem.end_address:
                    taint.start_address = temp_mem.start_address
                    taint.size = taint.size + temp_mem.size
                elif taint.end_address == temp_mem.start_address:
                    taint.end_address = temp_mem.end_address
                    taint.size = taint.size + temp_mem.size
                elif taint.end_address > temp_mem.start_address > taint.start_address:
                    break
                elif temp_mem.start_address < temp_mem.end_address < taint.start_address or \
                        taint.end_address < temp_mem.start_address < temp_mem.end_address:
                    marked_data.append(temp_mem)
            # for index in range(item[0], item[0] + item[1]):
    #     marked_memory.add(index)

    if count_of_mem == 0:
        marked_data.append(temp_mem)


def mark(taint, marked_data):
    for item in taint:
        if isinstance(item, str):
            add_register(item, marked_data)
        elif isinstance(item, list):
            add_memory(item, marked_data)


def add_items(input_record, marked_data, type_of_add):
    for item in input_record[type_of_add]:
        if isinstance(item, str):
            add_register(item, marked_data)
        elif isinstance(item, list):
            add_memory(item, marked_data)


def handle_step(input_record, marked_data, name_of_field):
    result = False
    for item in input_record[name_of_field]:
        for taint in marked_data:
            if isinstance(item, str) and isinstance(taint, Register):
                temp_reg = Register(item)
                if taint.name == temp_reg.name:
                    add_items(input_record, marked_data, 'writtenMem')
                    if taint.weight <= temp_reg.weight:
                        add_items(input_record, marked_data, 'writeRegs')
                    result = True
            if isinstance(item, list) and isinstance(taint, Memory):
                temp_mem = Memory(item)
                if temp_mem.start_address >= taint.start_address and temp_mem.end_address <= taint.end_address:
                    add_items(input_record, marked_data, 'writtenMem')
                    add_items(input_record, marked_data, 'writeRegs')
                    result = True
    return result


def remove_memory(item, marked_data):
    temp_mem = Memory(item)
    for taint in marked_data:
        if isinstance(taint, Memory):
            if temp_mem.start_address == taint.start_address and temp_mem.end_address == taint.end_address:
                marked_data.remove(taint)
            elif temp_mem.start_address == taint.start_address:
                taint.size = taint.size - temp_mem.size
                taint.start_address = taint.start_address + taint.size
            elif temp_mem.end_address == taint.end_address:
                taint.size = taint.size - temp_mem.size
                taint.end_address = taint.start_address + taint.size


def delete_data(input_record, marked_data, type_of_field):
    for item in input_record[type_of_field]:
        if isinstance(item, list):
            remove_memory(item, marked_data)


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

    index_of_instruction = 0
    index_of_test = 0
    result_answer = []
    marked_data = []

    for input_record in input_data:
        if index_of_instruction == 75:
            i = 1
        source_test = get_test_data_record(test_data, index_of_instruction, 'source')
        sink_test = get_test_data_record(test_data, index_of_instruction, 'sink')
        if source_test:
            mark(source_test['taint'], marked_data)
        if sink_test:
            result_answer.append({'step': index_of_instruction, 'answer': copy.deepcopy(marked_data)})

        has_read_mem = handle_step(input_record, marked_data, 'readMem')
        has_read_reg = handle_step(input_record, marked_data, 'readRegs')

        if not (has_read_reg and has_read_mem) and 'mov' in input_record['text']:
            i = 1
            delete_data(input_record, marked_data, 'writeRegs')
            delete_data(input_record, marked_data, 'writtenMem')
        index_of_instruction += 1

    with open(output_JSON, 'w') as f:
        json.dump(result_answer, f)
    print("Success")


main()
