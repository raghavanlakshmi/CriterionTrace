import pytest
from src.safety import review_assessments, quote_is_negative
from src.schemas import CriterionAssessment, EvidenceItem


def answer(quote, basis="explicit_negative", kind="exclusion"):
    fact=EvidenceItem(category="comorbidity", value=quote, evidence_text=quote,
        source_file="record.txt", source_page=1, quote_verified=True)
    return CriterionAssessment(criterion_id="EXC-01", criterion_text="Active condition requiring systemic treatment; replacement is allowed.",
        criterion_type=kind,status="MEETS",method="llm",patient_evidence=[fact],explanation="Record reviewed.",clearance_basis=basis)


@pytest.mark.parametrize("basis,quote,reason", [
    ("exception_only","Replacement therapy only.","allowed condition only"),
    ("absence","No other condition documented.","cleared from absence"),
    ("explicit_negative","Replacement therapy only.","no negative evidence cited"),
    (None,"No active condition.","basis declared"),
])
def test_all_exclusion_clearances_require_negative_basis_and_quote(basis,quote,reason):
    result,flags=review_assessments([answer(quote,basis)])
    assert result[0].status=="UNKNOWN" and any(reason in f for f in flags)


@pytest.mark.parametrize("quote",["No active condition.","Test negative for the condition.","Without the condition.",
    "Patient denies the condition.","The condition was ruled out.","Condition absent.","Patient is free of the condition."])
def test_verified_negatives_are_permitted(quote):
    result,flags=review_assessments([answer(quote)])
    assert result[0].status=="MEETS" and not flags


@pytest.mark.parametrize("quote",["Condition not documented.","Condition cannot be ruled out.","Not only the condition was present."])
def test_nonassessment_and_uncertainty_are_not_negatives(quote):
    assert not quote_is_negative(quote)


def test_unverified_negative_and_inclusion_boundary():
    item=answer("No active condition."); item.patient_evidence[0].quote_verified=False
    assert review_assessments([item])[0][0].status=="UNKNOWN"
    assert review_assessments([answer("Replacement therapy only.","exception_only","inclusion")])[0][0].status=="MEETS"
