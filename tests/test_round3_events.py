import pytest
from src.schemas import CriterionAssessment,EvidenceItem
from src.safety import review_assessments


def event(day="2026-02-09",category="diagnosis"):
    return EvidenceItem(category=category,value="Clinical event",date=day,evidence_text=f"Event on {day}.",source_file="event.txt",source_page=1,quote_verified=True)


def item(e=None,reference=True):
    facts=[e or event()]
    if reference: facts.append(event("2026-06-22","planned_study_event"))
    return CriterionAssessment(criterion_id="EXC-01",criterion_text="Clinical event within 6 months before first study dose",criterion_type="exclusion",status="UNKNOWN",method="llm",patient_evidence=facts,explanation="Needs date calculation.",window_evidence_index=0)


def test_any_model_selected_clinical_event_is_computed():
    reviewed,flags=review_assessments([item()])
    assert reviewed[0].status=="DOES_NOT_MEET" and "interval 133 days" in reviewed[0].explanation
    assert not any("lacks an explicitly documented" in f for f in flags)


@pytest.mark.parametrize("value",[item(event("2025-01-01")),item(event().model_copy(update={"date":None})),item(reference=False),item().model_copy(update={"window_evidence_index":99})])
def test_outside_missing_or_uncited_dates_are_unknown(value):
    reviewed,flags=review_assessments([value]); assert reviewed[0].status=="UNKNOWN" and flags
