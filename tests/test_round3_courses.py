import pytest
from src.schemas import EvidenceItem,CriterionAssessment
from src.safety import review_assessments
from src.evidence_extraction import verify_quotes
from src.date_math import date_bounds


def course(start="2026-06-14",end="2026-06-18"):
    return EvidenceItem(category="current_medication",value="Systemic drug, oral tablets",date=start,start_date=start,end_date=end,evidence_text=f"Systemic drug by mouth from {start} through {end}." if end else f"Systemic drug started {start}.",source_file="record.txt",source_page=1,quote_verified=True)


def assess(fact,reference="2026-06-22"):
    plan=EvidenceItem(category="planned_study_event",value="Study dose",date=reference,evidence_text=f"First study dose scheduled {reference}.",source_file="plan.txt",source_page=1,quote_verified=True)
    item=CriterionAssessment(criterion_id="EXC-01",criterion_text="Systemic drug within 7 days before first study dose",criterion_type="exclusion",status="UNKNOWN",method="llm",patient_evidence=[fact,plan],window_evidence_index=0,explanation="Compute date.")
    return review_assessments([item])


def test_course_end_not_start_drives_window():
    result,flags=assess(course()); assert result[0].status=="DOES_NOT_MEET"
    assert "interval 4 days" in result[0].explanation
    assert assess(course(end=None))[0][0].status=="UNKNOWN"


def test_numeric_course_dates_are_code_verified():
    from src.schemas import DocumentPage
    fact=course().model_copy(update={"start_date":None,"end_date":None})
    page=DocumentPage(filename="record.txt",page_number=1,text=fact.evidence_text,extraction_method="TXT")
    checked=verify_quotes([fact],[page])[0]
    assert checked.start_date=="2026-06-14" and checked.end_date=="2026-06-18"


def test_month_precision_never_invents_day_and_handles_boundary():
    fact=course().model_copy(update={"date":None,"start_date":None,"end_date":"2026-06","evidence_text":"Course completed in June 2026."})
    result,flags=assess(fact,"2026-07-02")
    assert result[0].status=="UNKNOWN" and "straddles" in result[0].explanation
    assert fact.end_date=="2026-06"
    assert date_bounds("April 2025")[0].isoformat()=="2025-04-01"


def test_unquoted_end_date_is_not_used():
    fact=course().model_copy(update={"end_date":"2026-06-20"})
    assert assess(fact)[0][0].status=="UNKNOWN"
