"""It contains the repository factory classes"""

from abc import ABC, abstractmethod

from app.model.repository.repository import Repository
from app.model.repository.user.user_repo_imp import UserRepositoryImp


class RepositoryFactory(ABC):
    """The RepositoryFactory abstract class declares the factory method that is
    supposed to return an object of a Repository class. The RepositoryFactory's
    subclasses usually provide the implementation of this class.
    """

    @abstractmethod
    def create(self) -> Repository:
        """Factory method.

        The subclasses of RepositoryFactory class can provide a
        implementation of this method.

        Returns:
            Repository: a repository object
        """

        pass


class UserRepositoryFactory(RepositoryFactory):
    """This class extends the abstract class RepositoryFactory and
    is responsable to create a instance of the UserRepositoryImp.
    """

    def create(self) -> UserRepositoryImp:
        """Creates instance of the UserRepositoryImp class.

        Returns:
            UserRepositoryImp: A UserRepositoryImp object
        """

        return UserRepositoryImp()
