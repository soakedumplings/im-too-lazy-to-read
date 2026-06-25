from collections import defaultdict


class MessageStore:
    """In-memory per-chat message buffer. Nothing is persisted to disk."""

    def __init__(self) -> None:
        self._buffers: dict[int, list[tuple[str, str]]] = defaultdict(list)

    def add(self, chat_id: int, sender: str, text: str) -> None:
        self._buffers[chat_id].append((sender, text))

    def pop_all(self, chat_id: int) -> list[tuple[str, str]]:
        return self._buffers.pop(chat_id, [])

    def count(self, chat_id: int) -> int:
        return len(self._buffers.get(chat_id, []))
