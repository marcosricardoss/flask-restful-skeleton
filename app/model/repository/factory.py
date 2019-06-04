"""This module contains abstract class used to implements repository factories."""

from __future__ import annotations
from abc import ABC, abstractmethod

from app.model.repository.repository import Repository


class RepositoryFactory(ABC):
    """The RepositoryFactory class declares the factory method that is supposed to return an
    object of a Repository class. The RepositoryFactory's subclasses usually provide the
    implementation of this method."""

    @abstractmethod
    def create(self) -> Repository:
        """Factory method.

        The subclasses of RepositoryFactory class can provide a
        implementation of this method.

        Returns:
            Repository: a repository object
        """

        pass
