class MemoryIdIterator:
    """
    Iterates over a set amount of id's. The id's are in the following format:
    "{component_name}_{serial_memory_number}".
    """
    def __init__(self, process_id, max_count):
        self.process_id = process_id
        self.name_count = 0
        self.max_count = max_count

    def get_next(self):
        """
        Get the next shared memory name.
        Returns: Next available shared memory name.
        """
        current_memory_id = (self.name_count % self.max_count)
        next_name = f"{self.process_id}_{current_memory_id}"
        self.name_count += 1

        return next_name
