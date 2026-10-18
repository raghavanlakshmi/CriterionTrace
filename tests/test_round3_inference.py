import pytest
from src.schemas import CriterionAssessment,EvidenceItem
from src.safety import review_assessments


def answer(explanation,quote="Condition documented.",criterion="Immune-mediated disease"):
    fact=EvidenceItem(category="comorbidity",value=quote,evidence_text=quote,source_file="r.txt",source_page=1,quote_verified=True)
    return CriterionAssessment(criterion_id="EXC-01",criterion_type="exclusion",criterion_text=criterion,status="DOES_NOT_MEET",method="llm",patient_evidence=[fact],explanation=explanation)


@pytest.mark.parametrize("hedge",["likely","probably","suggests","consistent with","may represent"])
def test_unsupported_category_link_cannot_support_decision(hedge):
    item=answer(f"The condition is {hedge} immune-mediated.")
    result,flags=review_assessments([item])
    assert result[0].status=="UNKNOWN" and any("category-inference" in f for f in flags)


def test_no_hedge_or_source_supported_category_is_unchanged():
    assert review_assessments([answer("The exclusion applies.")])[0][0].status=="DOES_NOT_MEET"
    assert review_assessments([answer("Likely immune-mediated.","Immune-mediated disease documented.")])[0][0].status=="DOES_NOT_MEET"


def test_incidental_unsupported_inference_is_review_flag_only():
    result,flags=review_assessments([answer("Probably unrelated finding.",criterion="Documented condition")])
    assert result[0].status=="DOES_NOT_MEET" and any("Review reasoning" in f for f in flags)
