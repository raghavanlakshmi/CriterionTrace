import pytest

from src.evidence_extraction import extract_planned_study_events
from src.safety import review_assessments
from src.schemas import CriterionAssessment, DocumentPage, EvidenceItem


def event(category, day, quote):
    return EvidenceItem(category=category, date=day, value=quote, evidence_text=quote,
        source_file='record.txt', source_page=1, quote_verified=True)


def assess(events, text='Anti-cancer therapy within 4 weeks before first study dose'):
    return review_assessments([CriterionAssessment(criterion_id='EXC-01', criterion_type='exclusion',
        criterion_text=text, status='UNKNOWN', method='llm', patient_evidence=events,
        explanation='Dates need review.')])


@pytest.mark.parametrize('day,expected,interval', [('2026-04-08', 'DOES_NOT_MEET', 12),
    ('2026-02-01', 'UNKNOWN', 78), ('2026-03-23', 'DOES_NOT_MEET', 28)])
def test_compute_window_from_actual_and_planned_dates(day, expected, interval):
    facts = [event('prior_treatment', day, f'Chemotherapy administered on {day}.'),
        event('planned_study_event', '2026-04-20', 'First study dose scheduled for 2026-04-20.')]
    reviewed, flags = assess(facts)
    assert reviewed[0].status == expected
    assert f'code-computed interval {interval} days' in reviewed[0].explanation
    assert any('Computed time-window guard' in f for f in flags)


def test_missing_reference_is_unknown_and_flagged():
    reviewed, flags = assess([event('prior_treatment', '2026-04-08', 'Dose administered 2026-04-08.')])
    assert reviewed[0].status == 'UNKNOWN'
    assert any('missing dated administration or planned first-dose reference date' in f for f in flags)


def test_medication_snapshot_is_not_an_administration():
    medication = event('current_medication', '2026-04-08', 'Drug listed 2026-04-08.')
    reviewed, _ = assess([medication, event('planned_study_event', '2026-04-20', 'First study dose scheduled 2026-04-20.')])
    assert reviewed[0].status == 'UNKNOWN'


def test_conflicting_planned_dates_remain_unknown():
    facts = [event('prior_treatment', '2026-04-08', 'Dose administered 2026-04-08.')]
    facts += [event('planned_study_event', day, f'First study dose scheduled {day}.') for day in ('2026-04-20', '2026-06-20')]
    reviewed, flags = assess(facts)
    assert reviewed[0].status == 'UNKNOWN'
    assert any('conflicting planned' in f for f in flags)


def test_calendar_month_window_uses_calendar_boundary():
    facts = [event('prior_treatment', '2026-02-28', 'Dose administered 2026-02-28.'),
        event('planned_study_event', '2026-03-31', 'First study dose scheduled 2026-03-31.')]
    reviewed, _ = assess(facts, 'Anti-cancer therapy within 1 month before first study dose')
    assert reviewed[0].status == 'DOES_NOT_MEET'
    assert 'starts 2026-02-28' in reviewed[0].explanation


def test_explicit_planned_cycle_date_is_extracted_with_quote_and_event_date():
    quote = 'If confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-06-15.'
    page = DocumentPage(filename='letter.txt', page_number=1, extraction_method='TXT',
        text='Document date: 2026-06-01\n' + quote)
    facts = extract_planned_study_events([page])
    assert len(facts) == 1 and facts[0].quote_verified
    assert facts[0].category == 'planned_study_event' and facts[0].date == '2026-06-15'
    assert quote in facts[0].evidence_text


def test_planned_date_extractor_ignores_undated_or_nonstudy_appointments():
    page = DocumentPage(filename='letter.txt', page_number=1, extraction_method='TXT',
        text='First study dose is planned. Dental visit scheduled for 2026-06-15.')
    assert extract_planned_study_events([page]) == []


def test_planned_metadata_uses_event_date_in_quote_not_letter_date():
    from src.evidence_extraction import verify_quotes
    quote = 'First study dose scheduled for 2026-06-15.'
    page = DocumentPage(filename='record.txt', page_number=1, extraction_method='TXT',
        text='Document date: 2026-06-01\n' + quote)
    wrong = event('planned_study_event', '2026-06-01', quote)
    verified = verify_quotes([wrong], [page])[0]
    assert verified.date == '2026-06-15' and verified.quote_verified


def test_actual_administration_mistagged_as_plan_is_not_verified_as_plan():
    from src.evidence_extraction import verify_quotes
    quote = 'Cycle 10 administered on 2026-06-01.'
    page = DocumentPage(filename='record.txt', page_number=1, extraction_method='TXT', text=quote)
    assert not verify_quotes([event('planned_study_event', '2026-06-01', quote)], [page])[0].quote_verified


def test_computable_window_bypasses_model_and_retains_both_sources():
    from src.eligibility import assess_free_text_criterion
    from src.schemas import TrialCriterion
    facts = [event('prior_treatment', '2026-06-01', 'Chemotherapy administered 2026-06-01.'),
        event('planned_study_event', '2026-06-15', 'First study dose scheduled for 2026-06-15.')]
    result = assess_free_text_criterion(TrialCriterion(criterion_id='EXC-01', type='exclusion',
        text='Anti-cancer therapy within 4 weeks before first study dose'), facts, [], client=None)
    assert result.status == 'DOES_NOT_MEET' and result.method == 'rule'
    assert result.patient_evidence == facts
    assert 'code-computed interval 14 days' in result.explanation
