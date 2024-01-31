from app.models.other_checklist_models import OtherCheckList


def test_fr_account_list_models():
    otherchecklist = OtherCheckList(
    id = 1,
    employee_id = 1,
    equipment = "teste",
    file_budget = "teste"
    )

    assert otherchecklist.id == 1
    assert otherchecklist.employee_id == 1
    assert otherchecklist.equipment == 'teste'
    assert otherchecklist.file_budget == 'teste'
    