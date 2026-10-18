import pytest

from src.safety import review_assessments
from src.schemas import CriterionAssessment, EvidenceItem


def decision(quote=None, status='MEETS', text='Other malignancies within 5 years, except adequately treated skin neoplasms'):
    facts = [] if quote is None else [EvidenceItem(category='comorbidity', value=quote,
        date='2025-01-01' if quote and '2025-01-01' in quote else None,
        evidence_text=quote, source_file='record.txt', source_page=1, quote_verified=True)]
    return CriterionAssessment(criterion_id='EXC-01', criterion_text=text,
        criterion_type='exclusion', status=status, method='llm', patient_evidence=facts,
        explanation='Source record reviewed.')


@pytest.mark.parametrize('quote,reason', [
    ('Skin neoplasms adequately treated.', 'excepted condition only'),
    (None, 'absence'),
    ('No history of blood cancer.', 'narrower negation'),
    ('No history of cancer in the family.', 'narrower negation'),
])
def test_history_clearance_requires_whole_scope_negative(quote, reason):
    reviewed, flags = review_assessments([decision(quote)])
    assert reviewed[0].status == 'UNKNOWN'
    assert any(reason in flag for flag in flags)


def test_explicit_scope_matching_negative_clears_history():
    reviewed, flags = review_assessments([decision('No history of cancer.')])
    assert reviewed[0].status == 'MEETS'
    assert not flags


def test_nonexcepted_documented_condition_is_not_downgraded():
    reviewed, flags = review_assessments([decision('Sarcoma diagnosed 2025-01-01.', 'DOES_NOT_MEET')])
    assert reviewed[0].status == 'DOES_NOT_MEET'
    assert not flags


def test_history_guard_is_general_to_conditions_beyond_cancer():
    for text, quote in [('History of epilepsy', 'No history of epilepsy.'),
                        ('Prior diagnosis of diabetes', 'No prior diagnosis of diabetes.')]:
        reviewed, flags = review_assessments([decision(quote, text=text)])
        assert reviewed[0].status == 'MEETS'
        assert not flags


def test_unverified_negative_never_clears_history():
    item = decision('No history of cancer.')
    item.patient_evidence[0].quote_verified = False
    reviewed, flags = review_assessments([item])
    assert reviewed[0].status == 'UNKNOWN'
    assert flags
