class BaseBlock:

    # def __init__(self, base_block=None):
    #     if base_block is None:
    #         self.start_address = ""
    #         self.text_commands = [][:]
    #         self.neighbours_address = [][:]
    #     else:
    #         self.start_address = base_block.start_address
    #         self.text_commands = base_block.text_commands[:]
    #         self.neighbours_address = base_block.neighbours_address[:]

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
