from src.schemas import DocumentPage,EvidenceItem
from src.evidence_extraction import complete_extraction


def test_skipped_diagnosis_remains_visible_and_triggers_retry_on_its_page():
    diagnosis="Assessment: a clinical event occurred on 2026-01-03."
    other="Examination is normal."
    page=DocumentPage(filename="note.txt",page_number=1,extraction_method="TXT",text=other+"\n"+diagnosis)
    fact=EvidenceItem(category="comorbidity",value=other,evidence_text=other,source_file="note.txt",source_page=1,quote_verified=True)
    calls=[]
    def extractor(pages):
        calls.extend(pages); return [fact]
    items,gaps=complete_extraction([page],[fact],extractor)
    assert len(calls)==1 and calls[0].filename=="note.txt"
    assert [g["text"] for g in gaps]==[diagnosis]
    assert gaps[0]["source_file"]=="note.txt" and gaps[0]["source_page"]==1
