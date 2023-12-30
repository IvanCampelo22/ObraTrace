import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
import warnings

from main import app
from app.schemas.other_checklist_schemas import OtherCheckListBase


client = TestClient(app)


def test_valid_other_checklist_schema():
    data = {
        "employee_id": 1,
        "equipment": "Teste",
        "file_budget": "Arquivo"
    }
    assert OtherCheckListBase(**data)


def test_invalid_other_checklist_schema():
    invalid_data = {
        "equipment": "test",
        "file_budget": "Arquivo"
    }

    with pytest.raises(ValidationError):
        OtherCheckListBase(**invalid_data)