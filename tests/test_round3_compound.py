from types import SimpleNamespace
from src.eligibility import assess_free_text_criterion,_LLMAssessment,_LLMPart
from src.schemas import TrialCriterion,EvidenceItem
from src.safety import review_assessments


def test_compound_calls_model_and_keeps_unaddressed_part_visible():
    calls=[]
    def parse(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(output=[],output_parsed=_LLMAssessment(status="UNKNOWN",evidence_indices=[0,1],explanation="Other condition unaddressed.",parts=[
            _LLMPart(text="Condition X",status="UNKNOWN",evidence_indices=[],explanation="Not documented.",clearance_basis="absence"),
            _LLMPart(text="drug Y within 7 days before first study dose",status="APPLIES",evidence_indices=[0,1],window_evidence_index=0,explanation="Dates require code.")]))
    facts=[EvidenceItem(category="current_medication",value="Drug Y oral",date="2026-01-01",evidence_text="Drug Y administered 2026-01-01.",source_file="event.txt",source_page=1,quote_verified=True),
        EvidenceItem(category="planned_study_event",value="Study dose",date="2026-02-01",evidence_text="First study dose scheduled 2026-02-01.",source_file="plan.txt",source_page=1,quote_verified=True)]
    criterion=TrialCriterion(criterion_id="EXC-01",type="exclusion",text="Condition X or drug Y within 7 days before first study dose")
    raw=assess_free_text_criterion(criterion,facts,[],client=SimpleNamespace(responses=SimpleNamespace(parse=parse)))
    checked,flags=review_assessments([raw])
    assert len(calls)==1 and checked[0].status=="UNKNOWN"
    assert len(checked[0].parts)==2 and "Condition X" in checked[0].explanation and "drug Y" in checked[0].explanation
    assert any("Compound criterion guard" in f for f in flags)


def test_any_exclusion_part_wins_but_absence_cannot_clear_all_parts():
    from src.schemas import CriterionAssessment
    base=CriterionAssessment(criterion_id="EXC-01",criterion_type="exclusion",criterion_text="A or B within 7 days before first study dose",status="UNKNOWN",method="llm",patient_evidence=[],explanation="Parts assessed.")
    a=base.model_copy(update={"criterion_text":"A","status":"DOES_NOT_MEET","patient_evidence":[EvidenceItem(category="diagnosis",value="A present",evidence_text="A present",source_file="r.txt",source_page=1,quote_verified=True)]})
    b=base.model_copy(update={"criterion_text":"B","parts":[],"status":"UNKNOWN"})
    assert review_assessments([base.model_copy(update={"parts":[a,b]})])[0][0].status=="DOES_NOT_MEET"
