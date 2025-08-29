"""Handling of Sleeper user data."""

from typing import Dict, Any, Self
from qsleeperfantasybot.sleeper.model.avatar import Avatar


class User:
    """Via the user resource, you can GET the user object
    by either providing the username or user_id of the user.
    """

    def __init__(self, name: str, user_id: str, display_name: str, avatar: str) -> None:
        self._name = name
        self._id = user_id
        self._display_name = display_name
        self._avatar = Avatar(avatar)

    @classmethod
    def from_dict(cls, user_data: Dict[str, Any]) -> Self:
        """Creates User object from dictionary data.

        Args:
            user_data (Dict[str, Any]): _description_

        Returns:
            Self: User model
        """
        return cls(
            name=user_data["username"],
            user_id=user_data["user_id"],
            display_name=user_data["display_name"],
            avatar=user_data["avatar"],
        )

    @property
    def name(self) -> str:
        """Sleeper user name."""
        return self._name

    @property
    def id(self) -> str:
        """Sleeper user ID."""
        return self._id

    @property
    def display_name(self) -> str:
        """Sleeper display name."""
        return self._display_name

    @property
    def avatar(self) -> Avatar:
        """Sleeper avatar."""
        return self._avatar
