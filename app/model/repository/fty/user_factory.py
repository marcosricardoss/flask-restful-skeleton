"""This module contains a concrete class of the RepositoryFactory abstract class."""

from app.model.repository.factory import RepositoryFactory
from app.model.repository.repo.user_repo_imp import UserRepositoryImp

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
