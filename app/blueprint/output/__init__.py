"""That module the contains the classes used to format the response output of API."""


from abc import ABC, abstractmethod
from flask import jsonify, Response


class Output(ABC):
    """Abstract class that is responsible to create output for the requests. It
    contains the abstract method 'create' which the subclasses must to implement.

    Attributes:
        status_code (int): The HTTP code request.        
        message (str): A response text message.
        data (dict): The data related with the request.
        headers (list): Header to be added the response headers.

    """

    def __init__(self, status_code: int, message: str = None, data: dict = None, headers: list = []) -> None:
        """ The constructor for Output class.

        Parameters:
            status_code (int): The HTTP code request.        
            message: A response text message.
            data: The data related with the request.
            headers: Header to be added the response headers.
        """

        self._status_code = status_code
        self._message = message
        self._data = data
        self._headers = headers

    def _create_response(self, output=dict()):
        """Creates the Reponse object

        Parameters:
            output (dict): the data to be used on the response construction.
        
        Returns:
            response: A flask response object.
        """

        response = jsonify(output)
        response.status_code = self._status_code
        for header in self._headers:
            response.headers.add(*header)

        return response

    @abstractmethod
    def create(self):
        """A abstract method that is responsible to create an output.
        The subclasses of that class, must to implement it
        """

        pass


class SuccessOutput(Output):
    """This class creates output to requests that were processed successfully.
    
    Attributes:
        status_code (int): The HTTP code request.                
        data (dict): The data related with the request.
        headers (list): Header to be added the response headers."""

    def __init__(self, status_code: int, data: dict, headers: list = list()) -> None:
        """ The constructor for SuccessOutput class.

        Parameters:
            status_code (int): The HTTP code request.                    
            data: The data related with the request.
            headers: Header to be added the response headers.
        """

        Output.__init__(self, status_code=status_code, data=data, headers=headers)
        self.__status = 'success'

    def create(self) -> Response:
        """This method is responsible to create an output for the API Request.
        
        Returns:
            A flask response object.
        """

        output = dict()
        output["status"] = self.__status
        output["data"] = self._data

        return self._create_response(output)


class SuccessEmptyOutput(Output):
    """This class creates output to requests that were processed successfully 
    without data in the response body.

    Attributes:
        status_code (int): The HTTP code request.        
        headers (list): Header to be added the response headers.
    """

    def __init__(self, status_code: int, headers: list = list()) -> None:
        """ The constructor for SuccessEmptyOutput class.

        Parameters:
            status_code (int): The HTTP code request.                
            headers: Header to be added the response headers.
        """

        Output.__init__(self, status_code=status_code, headers=headers)

    def create(self) -> Response:
        """This method is responsible to create an output for the API Request.
        
        Returns:
            A flask response object.
        """

        return self._create_response()


class FailOutput(Output):
    """This class creates output to requests that were processed unsuccessfully.
    
    Attributes:
        status_code (int): The HTTP code request.            
        data (dict): The data related with the request.
        headers (list): Header to be added the response headers.
    """

    def __init__(self, status_code: int, data: dict, headers: list = list()) -> None:
        """ The constructor for FailOutput class.

        Parameters:
            status_code (int): The HTTP code request.                
            data: The data related with the request.
            headers: Header to be added the response headers.
        """

        Output.__init__(self, status_code=status_code, data=data, headers=headers)
        self.__status = 'fail'

    def create(self) -> Response:
        """This method is responsible to create an output for the API Request.
        
        Returns:
            A flask response object.
        """

        output = dict()
        output["status"] = self.__status
        output["data"] = self._data

        return self._create_response(output)


class ErrorOutput(Output):
    """This class creates output to requests that were processed with errors.
    
    Attributes:
        status_code (int): The HTTP code request.        
        message (str): A response text message.        
        headers (list): Header to be added the response headers.
    """


    def __init__(self, status_code: int, message: str, headers: list = list()) -> None:
        """ The constructor for ErrorOutput class.

        Parameters:
            status_code (int): The HTTP code request.        
            message: A response text message.            
            headers: Header to be added the response headers.
        """

        Output.__init__(self, status_code=status_code,message=message, headers=headers)
        self.__status = 'error'

    def create(self) -> Response:
        """This method is responsible to create an output for the API Request.
        
        Returns:
            A flask response object.
        """

        output = dict()
        output["status"] = self.__status
        output["message"] = self._message

        return self._create_response(output)
