import pytest
from pipert2.utils.shared_memory_manager import SharedMemoryManager


MAX_SEGMENT_COUNT = 50


@pytest.fixture
def dummy_shared_memory_manager():
    dummy_shared_memory_manager = SharedMemoryManager()
    return dummy_shared_memory_manager


def test_write_and_read_from_memory(dummy_shared_memory_manager):
    test_data = b"AAA"
    memory_name = dummy_shared_memory_manager.write_to_mem(test_data)
    assert dummy_shared_memory_manager.read_from_mem(memory_name, len(test_data)) == test_data


def test_max_count(dummy_shared_memory_manager):
    test_data = b"BBB"
    test_data_2 = b"aaa"
    memories = []
    first_memory = dummy_shared_memory_manager.write_to_mem(test_data)

    for _ in range(MAX_SEGMENT_COUNT - 1):
        memories.append(dummy_shared_memory_manager.write_to_mem(test_data_2))

    for memory in memories:
        assert test_data_2 == dummy_shared_memory_manager.read_from_mem(memory, len(test_data))

    assert test_data == dummy_shared_memory_manager.read_from_mem(first_memory, len(test_data))
    second_cycle = dummy_shared_memory_manager.write_to_mem(test_data_2)
    assert second_cycle == first_memory
    assert test_data != dummy_shared_memory_manager.read_from_mem(first_memory, len(test_data))


def test_cleanup(dummy_shared_memory_manager):
    dummy_shared_memory_manager.cleanup_memory()
    assert dummy_shared_memory_manager.shared_memory_generator.shared_memories == {}
