import pytest
from src.schemas import CriterionAssessment,EvidenceItem,DateComparison
from src.safety import review_assessments


def answer(explanation,comparisons=None):
    fact=EvidenceItem(category="diagnosis",value="Condition present",evidence_text="Condition present",source_file="r.txt",source_page=1,quote_verified=True)
    return CriterionAssessment(criterion_id="EXC-01",criterion_type="exclusion",criterion_text="Condition",status="DOES_NOT_MEET",method="llm",patient_evidence=[fact],explanation=explanation,date_comparisons=comparisons or [])


def test_bad_month_precision_claim_is_rejected_without_structured_output():
    original="April 2025 is more than 2 years before 2026-06-22."
    result,flags=review_assessments([answer(original)])
    assert result[0].status=="UNKNOWN" and original in result[0].explanation
    assert any("explanation contains an incorrect date comparison" in f for f in flags)


@pytest.mark.parametrize("claim,expected",[("more_than","UNKNOWN"),("less_than","DOES_NOT_MEET"),("within","DOES_NOT_MEET")])
def test_structured_comparisons_are_recomputed(claim,expected):
    comparison=DateComparison(from_date="2025-04",to_date="2026-06-22",claimed=claim,amount=2,unit="years")
    result,flags=review_assessments([answer("Dates compared.",[comparison])])
    assert result[0].status==expected


def test_correct_prose_comparison_is_unchanged():
    result,flags=review_assessments([answer("April 2025 is less than 2 years before 2026-06-22.")])
    assert result[0].status=="DOES_NOT_MEET" and not flags


def test_date_comparison_schema_rejects_ages_as_calendar_dates():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        DateComparison(from_date="58",to_date="18",claimed="more_than",amount=1,unit="years")
