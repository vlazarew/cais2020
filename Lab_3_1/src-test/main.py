import argparse
import json

from src.Instruction import Instruction
from src.baseBlock import BaseBlock


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
            # curr_instruction = Instruction(fix_address(record), index_of_instruction)
            # curr_base_block = BaseBlock(start_instruction, curr_instruction, start_instruction.address,
            #                             int(curr_instruction.address, 16) - int(start_instruction.address, 16))

            # if not prev_base_block is None:
            #     edges.append({'from': prev_base_block,
            #                   'to': curr_base_block})
            # all_base_blocks.add(curr_base_block)
            all_base_blocks_addresses.add(start_instruction.address)
            # prev_base_block = BaseBlock(start_instruction, curr_instruction, start_instruction.address,
            #                             int(curr_instruction.address, 16) - int(start_instruction.address, 16))

            if 'isForeignBranch' in record:
                # curr_base_block = BaseBlock(curr_instruction, curr_instruction, record['foreignTargetName'],
                #                             int(curr_instruction.address, 16) - record['foreignTargetAddress'])

                # if not prev_base_block is None:
                #     edges.append({'from': prev_base_block,
                #                   'to': curr_base_block})
                # all_base_blocks.add(curr_base_block)
                all_base_blocks_addresses.add(record['foreignTargetName'])
                # prev_base_block = BaseBlock(curr_instruction, curr_instruction, record['foreignTargetName'],
                #                             int(curr_instruction.address, 16) - record['foreignTargetAddress'])

            is_new_block = True

        index_of_instruction += 1

    prev_base_block = None
    curr_base_block = None
    edges = []
    for record in data:
        is_foreign = 'isForeignBranch' in record
        if is_foreign:
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
