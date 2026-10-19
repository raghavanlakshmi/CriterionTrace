import pytest

from src.safety import review_assessments
from src.schemas import CriterionAssessment, EvidenceItem


@pytest.mark.parametrize('kind,status,explanation,conclusion,expected', [
    ('exclusion', 'MEETS', 'The exclusion applies.', None, 'UNKNOWN'),
    ('exclusion', 'DOES_NOT_MEET', 'The exclusion does not apply.', None, 'UNKNOWN'),
    ('exclusion', 'MEETS', 'The exclusion does not apply.', None, 'MEETS'),
    ('exclusion', 'DOES_NOT_MEET', 'The exclusion applies.', None, 'DOES_NOT_MEET'),
    ('exclusion', 'MEETS', 'The exclusion is not applicable.', None, 'MEETS'),
    ('exclusion', 'MEETS', 'Review complete.', 'APPLIES', 'UNKNOWN'),
    ('exclusion', 'MEETS', 'The exclusion applies.', 'DOES_NOT_APPLY', 'UNKNOWN'),
    ('exclusion', 'MEETS', 'Review complete.', 'DOES_NOT_APPLY', 'MEETS'),
    ('inclusion', 'MEETS', 'The criterion is not met.', None, 'UNKNOWN'),
    ('inclusion', 'DOES_NOT_MEET', 'The patient meets the criterion.', None, 'UNKNOWN'),
    ('inclusion', 'DOES_NOT_MEET', 'The patient does not meet the criterion.', None, 'DOES_NOT_MEET'),
    ('inclusion', 'MEETS', 'The criterion is met.', 'MEETS', 'MEETS'),
    ('inclusion', 'MEETS', 'Review complete.', 'UNKNOWN', 'UNKNOWN'),
])
def test_label_and_final_conclusion_agree(kind, status, explanation, conclusion, expected):
    fact = EvidenceItem(category='biomarker', value='Marker absent', evidence_text='Marker absent',
        source_file='record.txt', source_page=1, quote_verified=True)
    item = CriterionAssessment(criterion_id='EXC-01' if kind == 'exclusion' else 'INC-01',
        criterion_text='Marker', criterion_type=kind, status=status, method='llm',
        patient_evidence=[fact], explanation=explanation, final_conclusion=conclusion, clearance_basis="explicit_negative")
    reviewed, flags = review_assessments([item])
    assert reviewed[0].status == expected
    if expected == 'UNKNOWN':
        assert any('status contradicts explanation' in f for f in flags)
        assert explanation in reviewed[0].explanation
    else:
        assert not flags
