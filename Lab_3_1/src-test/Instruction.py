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
