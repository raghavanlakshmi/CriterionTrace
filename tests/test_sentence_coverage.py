from src.evidence_extraction import uncovered_content_lines
from src.schemas import DocumentPage, EvidenceItem


def source(text):
    return DocumentPage(filename='record.txt', page_number=3, extraction_method='TXT', text=text)


def fact(quote):
    return EvidenceItem(category='comorbidity', value=quote, evidence_text=quote,
        source_file='record.txt', source_page=3)


def test_wraps_are_joined_and_verified_sentence_is_covered():
    page = source('Survivorship summary\nThe patient had a prior condition treated\nin 2024 with complete recovery.\nFamily history: father with cancer.')
    evidence = [fact('The patient had a prior condition treated in 2024 with complete recovery.')]
    gaps = uncovered_content_lines([page], evidence)
    assert [g['text'] for g in gaps] == ['Family history: father with cancer.']
    assert gaps[0]['source_file'] == 'record.txt' and gaps[0]['source_page'] == 3
    assert gaps[0]['sentence_number'] == 2


def test_partial_quote_does_not_hide_remaining_sentence():
    page = source('Condition treated. A separate condition was discussed\nbut never treated.')
    gaps = uncovered_content_lines([page], [fact('Condition treated.')])
    assert [g['text'] for g in gaps] == ['A separate condition was discussed but never treated.']


def test_headings_are_skipped_but_labelled_facts_and_decimal_values_survive():
    page = source('Screening plan\nConsultation summary\nClinical Findings\nHemoglobin: 12.4 g/dL\nNo further cycles scheduled at this clinic.')
    gaps = uncovered_content_lines([page], [])
    assert [g['text'] for g in gaps] == ['Hemoglobin: 12.4 g/dL', 'No further cycles scheduled at this clinic.']


def test_wrong_page_quote_cannot_hide_sentence():
    item = fact('Condition is present.').model_copy(update={'source_page': 1})
    gaps = uncovered_content_lines([source('Condition is present.')], [item])
    assert len(gaps) == 1


def test_verified_fragment_keeps_full_source_sentence_context_without_new_fact():
    from src.evidence_extraction import complete_quote_context, verify_quotes
    text = 'The patient had a condition treated in 2024; she remains in remission.'
    page = source(text)
    item = fact('a condition treated in 2024')
    result = complete_quote_context(verify_quotes([item], [page]), [page])
    assert len(result) == 1 and result[0].value == item.value
    assert result[0].evidence_text == text and result[0].quote_verified
    assert uncovered_content_lines([page], result) == []


def test_invalid_fragment_is_never_expanded_into_a_verified_quote():
    from src.evidence_extraction import complete_quote_context, verify_quotes
    page = source('No history of the condition.')
    item = fact('Condition is present.')
    result = complete_quote_context(verify_quotes([item], [page]), [page])
    assert not result[0].quote_verified
    assert result[0].evidence_text == item.evidence_text
