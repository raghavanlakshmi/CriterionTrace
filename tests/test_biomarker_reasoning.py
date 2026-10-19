import pytest

from src.safety import review_assessments
from src.schemas import CriterionAssessment, EvidenceItem


def record(category, quote):
    return EvidenceItem(category=category, value=quote, evidence_text=quote,
                        source_file='note.txt', source_page=1, quote_verified=True)


def assess(explanation, extra=()):
    item = CriterionAssessment(criterion_id='EXC-01', criterion_type='exclusion',
        criterion_text='Prior targeted inhibitor therapy', status='DOES_NOT_MEET', method='llm',
        patient_evidence=[record('biomarker', 'ABC V123D mutation detected'), *extra], explanation=explanation)
    return review_assessments([item])


@pytest.mark.parametrize('link', ['indicating', 'suggests', 'implies', 'consistent with'])
def test_mutation_alone_cannot_establish_treatment(link):
    result, flags = assess(f'The ABC V123D mutation is {link} inhibitor therapy.')
    assert result[0].status == 'UNKNOWN'
    assert any('biomarker-to-treatment' in f for f in flags)


def test_cited_medication_keeps_status_but_requires_review():
    result, flags = assess('ABC V123D suggests inhibitor therapy.', [record('current_medication', 'Targeted inhibitor drug listed')])
    assert result[0].status == 'DOES_NOT_MEET'
    assert any('review the explanation' in f for f in flags)


@pytest.mark.parametrize('explanation', ['Explicit treatment is documented.', 'The mutation does not imply inhibitor therapy.'])
def test_explanations_without_inference_are_unchanged(explanation):
    result, flags = assess(explanation)
    assert result[0].status == 'DOES_NOT_MEET'
    assert flags == []


def test_unverified_or_negative_treatment_does_not_rescue_inference():
    negative = record('prior_treatment', 'No prior inhibitor therapy')
    result, flags = assess('ABC V123D indicating inhibitor therapy.', [negative])
    assert result[0].status == 'UNKNOWN'
    assert flags
