"""Handling of Sleeper Avatar data."""


class Avatar:
    """Users and leagues have avatar images.
    There are thumbnail and full-size images for each avatar.
    """

    def __init__(self, avatar_id: str) -> None:
        self._avatar_id = avatar_id
        self._avatar_url = f"https://sleepercdn.com/avatars/{avatar_id}"
        self._avatar_thumb_url = f"https://sleepercdn.com/avatars/thumbs/{avatar_id}"

    @property
    def avatar_id(self) -> str:
        """Avatar ID."""
        return self._avatar_id

    @property
    def avatar_url(self) -> str:
        """Avatar URL."""
        return self._avatar_url

    @property
    def avatar_thumb_url(self) -> str:
        """Avatar thumbnail URL."""
        return self._avatar_thumb_url
