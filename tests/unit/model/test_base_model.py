"""It contains tests for the Model class from the models.py module"""

import pytest
from sqlalchemy.exc import NoInspectionAvailable

def test_base_model(session):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the serialize() and remove_session() methods
    """

    from app.model.models import Model
    model = Model()
    assert model.serialize() == {}   
    with pytest.raises(NoInspectionAvailable):
        model.remove_session()
