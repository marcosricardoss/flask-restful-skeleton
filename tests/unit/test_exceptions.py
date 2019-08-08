"""It contains tests for the custom exceptions"""

import pytest

def test_token_not_found_exception():
  """
  GIVEN the TokenNotFound class exception
  WHEN raise a TokenNotFound
  THEN check the exception trigger
  """

  from app.exceptions import TokenNotFound

  with pytest.raises(TokenNotFound):
    raise TokenNotFound