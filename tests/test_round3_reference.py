from src.safety import review_assessments, time_window_problem
from src.schemas import CriterionAssessment, EvidenceItem


def test_planned_reference_suppresses_older_guard():
    facts=[EvidenceItem(category="diagnosis",value="Event",date="2026-01-01",evidence_text="Event on 2026-01-01.",source_file="event.txt",source_page=1,quote_verified=True),
           EvidenceItem(category="planned_study_event",value="Cycle 1 day 1",date="2026-02-01",evidence_text="Cycle 1 day 1 of study treatment is scheduled for 2026-02-01.",source_file="plan.txt",source_page=1,quote_verified=True)]
    item=CriterionAssessment(criterion_id="EXC-01",criterion_type="exclusion",criterion_text="Clinical event within 6 months before first study dose",status="DOES_NOT_MEET",method="llm",patient_evidence=facts,explanation="The exclusion applies.",window_evidence_index=0)
    assert time_window_problem(item) is None
    result,flags=review_assessments([item]); assert result[0].status=="DOES_NOT_MEET"
    assert not any("study reference" in f for f in flags)
