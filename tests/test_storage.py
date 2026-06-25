from storage import MessageStore


def test_add_and_pop_all_returns_in_order():
    store = MessageStore()
    store.add(1, "Alice", "hi")
    store.add(1, "Bob", "hey there")
    assert store.pop_all(1) == [("Alice", "hi"), ("Bob", "hey there")]


def test_pop_all_clears_buffer():
    store = MessageStore()
    store.add(1, "Alice", "hi")
    store.pop_all(1)
    assert store.pop_all(1) == []
    assert store.count(1) == 0


def test_chats_are_isolated():
    store = MessageStore()
    store.add(1, "Alice", "in chat 1")
    store.add(2, "Bob", "in chat 2")
    assert store.pop_all(1) == [("Alice", "in chat 1")]
    assert store.pop_all(2) == [("Bob", "in chat 2")]


def test_count_tracks_buffer_size():
    store = MessageStore()
    assert store.count(1) == 0
    store.add(1, "Alice", "a")
    store.add(1, "Alice", "b")
    assert store.count(1) == 2
