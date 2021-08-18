class SharedMemory: # Should be singleton
    
    @classmethod
    def does_data_saved_in_shared_memory(cls, data_value):
        pass

    @classmethod
    def get_data_metadata(cls, data_value):
        pass

    @classmethod
    def get_data(cls, data_address, metadata):
        pass

    @classmethod
    def save_data(cls, data):
        pass