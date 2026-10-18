from src.evidence_extraction import complete_extraction, extract_labeled_facts
from src.schemas import DocumentPage, EvidenceItem


def source(text):
    return DocumentPage(filename='arbitrary.txt', page_number=1, text=text, extraction_method='TXT')


def test_explicit_biopsy_labs_and_biomarkers_do_not_depend_on_model():
    page = source('Document date: 2026-01-02\nSpecimen: lung biopsy, carcinoma\nHemoglobin: 12 g/dL\nBRAF: wild type')
    items, gaps = complete_extraction([page], [], lambda pages: [])
    assert [e.category for e in items] == ['diagnosis', 'lab', 'biomarker']
    assert all(e.quote_verified and e.date == '2026-01-02' for e in items)
    assert gaps == []


def test_label_parser_ignores_family_and_administrative_or_unreadable_fields():
    items = extract_labeled_facts([source('Family history: relative had cancer\nPatient ID: X\nSex: UNKNOWN\nAge: [UNREADABLE]')])
    assert items == []


def test_existing_label_quote_is_not_duplicated_by_deterministic_reader():
    page = source('Hemoglobin: 12 g/dL')
    existing = EvidenceItem(category='lab', value='12 g/dL', evidence_text=page.text,
        source_file=page.filename, source_page=1)
    items, gaps = complete_extraction([page], [existing], lambda pages: [])
    assert len(items) == 1 and gaps == []


def test_missing_placeholders_and_sex_inferred_from_relatives_do_not_cover_lines():
    page = source('Finding A.\nFamily history: mother had cancer')
    records = [EvidenceItem(category='sex', value='Male', source_file=page.filename,
        source_page=1, evidence_text='Family history: mother had cancer'),
        EvidenceItem(category='sex', value='UNKNOWN', source_file=page.filename,
        source_page=1, evidence_text=page.text)]
    items, gaps = complete_extraction([page], records, lambda pages: records)
    assert items == []
    assert len(gaps) == 2
