import argparse
import json


class BaseBlock:

    def __init__(self, start_instruction=None, end_instruction=None, address=None, size=None, shape=None):
        if not address is None:
            self.address = address

        if not size is None:
            self.size = size

        if not start_instruction is None:
            self.start_instruction = start_instruction

        if not end_instruction is None:
            self.end_instruction = end_instruction

        if not shape is None:
            self.shape = shape


class Instruction:

    def __init__(self, address=None, index=None, size=None, next_instruction_address=None, next_instruction_trace=None,
                 target=None):
        if not address is None:
            self.address = address

        if not size is None:
            self.size = size

        if not next_instruction_address is None:
            self.next_instruction_address = next_instruction_address

        if not next_instruction_trace is None:
            self.next_instruction_trace = next_instruction_trace

        if not target is None:
            self.target = target

        if not index is None:
            self.index = index


def fix_address(record):
    return ['{:016x}'.format(i) for i in [record['address']]][0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")

    args = parser.parse_args()
    input_JSON = args.input
    output_File = args.output

    all_base_blocks_addresses = set()
    start_instruction = Instruction(None, 0)

    with open(input_JSON, "r") as read_file:
        data = json.load(read_file)

    index_of_instruction = 0
    is_new_block = True
    for record in data:
        if is_new_block:
            start_instruction = Instruction(fix_address(record), index_of_instruction)
            is_new_block = False

        if 'isBranch' in record:
            all_base_blocks_addresses.add(start_instruction.address)

            if 'isForeignBranch' in record:
                all_base_blocks_addresses.add(record['foreignTargetName'])

            is_new_block = True

        index_of_instruction += 1
"ax
            fixed_address = record['foreignTargetName']
        else:
            fixed_address = fix_address(record)
        if fixed_address in all_base_blocks_addresses:
            if not curr_base_block is None:
                prev_base_block = BaseBlock(None, None, curr_base_block.address)
            prev_is_none = prev_base_block is None
            curr_base_block = BaseBlock(None, None, fixed_address)
            if not prev_is_none:
                edges.append({'from': prev_base_block,
                              'to': curr_base_block})

    printed_strings = []
    result_string = "strict digraph {\n"
    for edge in edges:
        temp_string = "\"" + edge['from'].address + "\" -> \"" + edge['to'].address + "\";\n"
        if not temp_string in printed_strings:
            printed_strings.append(temp_string)
            result_string += temp_string

    result_string += "}"
    f = open(output_File, 'w')
    f.write(result_string)
    print("Success")


main()
