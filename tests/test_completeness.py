import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path

from src.evidence_extraction import (
    EvidenceExtractionError, complete_extraction, uncovered_content_lines,
    verify_quotes,
)
from src.schemas import DocumentPage, EvidenceItem
from src.workflow import prepare_human_review_node


def page():
    return DocumentPage(filename='source.txt', page_number=2, extraction_method='TXT',
        text='SYNTHETIC PATIENT - FICTIONAL DATA\nClinical note\nPatient ID: TEST\nDocument date: 2026-01-01\nHistory:\nFinding A.\nFinding B.\nFamily history: relative with condition\nPage 2 of 2')


def fact(quote='Finding A.', verified=True):
    return EvidenceItem(category='comorbidity', value=quote, evidence_text=quote,
                        source_file='source.txt', source_page=2, quote_verified=verified)


def test_second_pass_captures_missing_line_once_without_duplicates():
    calls = []
    def extractor(pages):
        calls.append(pages)
        return [fact(), fact('Finding B.')]
    items, gaps = complete_extraction([page()], [fact()], extractor)
    assert len(calls) == 1 and calls[0] == [page()]
    assert len(items) == 2
    assert all(e.quote_verified for e in items)
    assert [g['text'] for g in gaps] == ['Family history: relative with condition']
    assert gaps[0]['message'] == 'Not captured by the tool, review manually'


def test_missing_line_is_visible_when_retry_skips_it():
    calls = []
    items, gaps = complete_extraction([page()], [fact()], lambda pages: calls.append(pages) or [fact()])
    assert len(calls) == 1 and len(items) == 1
    assert 'Finding B.' in [g['text'] for g in gaps]
    assert all(g['source_file'] == 'source.txt' and g['source_page'] == 2 for g in gaps)


def test_failed_retry_retains_initial_facts_and_manual_review_lines():
    def fail(pages):
        raise EvidenceExtractionError('Synthetic failure')
    items, gaps = complete_extraction([page()], [fact()], fail)
    assert len(items) == 1
    assert 'Finding B.' in [g['text'] for g in gaps]


def test_verification_is_recomputed_and_wrong_page_cannot_hide_gaps():
    wrong = fact('Finding B.').model_copy(update={'source_page': 1})
    gaps = uncovered_content_lines([page()], [wrong])
    assert 'Finding B.' in [g['text'] for g in gaps]


def test_covered_page_has_no_retry_and_whitespace_normalizes():
    source = page().model_copy(update={'text': 'Finding   A.\nFinding B.'})
    items, gaps = complete_extraction([source], [fact('Finding A.\nFinding B.')], lambda pages: pytest.fail('Unexpected retry'))
    assert len(items) == 1 and gaps == []


def test_retries_only_affected_pages_and_rejects_other_page_results():
    covered = page().model_copy(update={'page_number': 1, 'text': 'Finding A.'})
    initial = fact().model_copy(update={'source_page': 1})
    calls = []
    def retry(pages):
        calls.extend(pages)
        return [fact('Finding B.').model_copy(update={'source_page': 99})]
    items, gaps = complete_extraction([covered, page()], [initial], retry)
    assert [p.page_number for p in calls] == [2]
    assert len(items) == 1
    assert 'Finding B.' in [g['text'] for g in gaps]


def test_human_review_contains_uncovered_lines_even_without_candidates():
    gaps = uncovered_content_lines([page()], [fact()])
    result = prepare_human_review_node({'extraction_gaps': gaps})
    assert result['human_review']['extraction_gaps'] == gaps
    assert result['human_review']['requires_human_review']


def test_app_displays_persistent_gaps():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'))
    app.session_state['run'] = {'evidence': [], 'pages': [], 'candidate_trials': [],
                                'extraction_gaps': uncovered_content_lines([page()], [fact()])}
    app.run(timeout=15)
    assert not app.exception
    assert any('Not captured by the tool, review manually' in w.value and 'Finding B.' in w.value for w in app.warning)


@pytest.mark.parametrize('header,expected', [('Document date: 2026-01-01\n', '2026-01-01'), ('', None)])
def test_snapshot_provenance_and_document_date_are_code_verified(header, expected):
    source = page().model_copy(update={'text': 'Medication list\n' + header + 'Drug listed (started 2025-01-01)'})
    item = fact('Drug listed (started 2025-01-01)').model_copy(update={'category': 'current_medication', 'date': '2025-01-01'})
    result = verify_quotes([item], [source])[0]
    assert result.source_kind == 'medication_list'
    assert result.date == expected
    assert result.quote_verified
