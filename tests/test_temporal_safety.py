import pytest

from src.safety import review_assessments
from src.schemas import CriterionAssessment, EvidenceItem


def evidence(category='prior_treatment', date='2026-01-05', **kwargs):
    return EvidenceItem(category=category, value='Documented treatment', date=date,
                        source_file='record.pdf', source_page=1,
                        evidence_text='Treatment administered 2026-01-05', quote_verified=True, **kwargs)


def decision(items, text='Therapy within 4 weeks', status='DOES_NOT_MEET'):
    return CriterionAssessment(criterion_id='EXC-01', criterion_text=text, criterion_type='exclusion',
                               status=status, method='llm', patient_evidence=items,
                               explanation='The cited therapy establishes the exclusion.')


@pytest.mark.parametrize('status', ['MEETS', 'DOES_NOT_MEET'])
def test_undated_temporal_decisions_are_unknown(status):
    reviewed, flags = review_assessments([decision([evidence(date=None)], status=status)])
    assert reviewed[0].status == 'UNKNOWN'
    assert any('lacks dated' in f for f in flags)


@pytest.mark.parametrize('category', ['current_medication', 'prior_treatment'])
def test_dated_medication_snapshot_cannot_decide_washout(category):
    reviewed, flags = review_assessments([decision([evidence(category, source_kind='medication_list')])])
    assert reviewed[0].status == 'UNKNOWN'
    assert any('snapshots' in f for f in flags)


def test_snapshot_can_establish_prior_exposure_without_time_window():
    result, flags = review_assessments([decision([evidence('current_medication', source_kind='medication_list')], text='Prior targeted therapy')])
    assert result[0].status == 'DOES_NOT_MEET'
    assert flags == []


@pytest.mark.parametrize('anchor', ['first study dose', 'first study-dose', 'first trial-dose', 'study-start', 'randomization'])
def test_dated_administration_needs_actual_study_reference(anchor):
    result, flags = review_assessments([decision([evidence()], text='Therapy within 4 weeks before ' + anchor)])
    assert result[0].status == 'UNKNOWN'
    assert any('reference date' in f for f in flags)


def test_documented_study_reference_and_dated_event_are_not_blocked():
    item = evidence().model_copy(update={'evidence_text': 'Treatment administered 2026-01-05; first study dose: 2026-01-10'})
    reference = evidence('planned_study_event', date='2026-01-10').model_copy(update={'evidence_text': 'First study dose scheduled for 2026-01-10.'})
    selected = decision([item, reference], text='Therapy within 4 weeks before first study dose').model_copy(update={'window_evidence_index': 0})
    result, flags = review_assessments([selected])
    assert result[0].status == 'DOES_NOT_MEET'
    assert any('code-computed interval 5 days' in f for f in flags)


@pytest.mark.parametrize('wording', ['The patient is currently taking a targeted drug.',
    'Documented current medication with a targeted drug.', 'The patient is currently on therapy.'])
def test_snapshot_current_use_wording_is_corrected_without_weakening_prior_exposure(wording):
    item = decision([evidence('current_medication', source_kind='medication_list')], text='Prior targeted therapy').model_copy(update={'explanation': wording})
    result, flags = review_assessments([item])
    assert result[0].status == 'DOES_NOT_MEET'
    assert 'currently taking' not in result[0].explanation
    assert 'current medication' not in result[0].explanation
    assert 'currently on' not in result[0].explanation
    assert 'use at screening is not established' in result[0].explanation
    assert any('current-use wording corrected' in f for f in flags)


def test_snapshot_wording_correction_does_not_rescue_temporal_decision():
    item = decision([evidence('current_medication', source_kind='medication_list')]).model_copy(update={'explanation': 'The patient is currently taking a drug.'})
    result, flags = review_assessments([item])
    assert result[0].status == 'UNKNOWN'
    assert 'currently taking' not in result[0].explanation
    assert any('snapshots' in f for f in flags)


def test_correct_negative_snapshot_caveat_is_not_reversed():
    from src.safety import snapshot_explanation
    item = decision([evidence('current_medication', source_kind='medication_list')])
    text = 'The dated list does not establish current use; the patient is not currently taking a documented dose.'
    assert snapshot_explanation(item, text) == text
