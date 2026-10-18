"""Output guardrails for research-trial prescreening."""

from __future__ import annotations

import re
import calendar
from datetime import date, timedelta

from .schemas import CriterionAssessment


DISCLAIMER = (
    "AI-assisted prescreening only.\n"
    "This system does not determine final clinical-trial eligibility.\n"
    "Research staff must verify source records and trial criteria."
)
INJECTION_PATTERNS = (
    re.compile(r"\bsystem\s+instruction\s*:", re.I),
    re.compile(r"\bignore\s+(?:all\s+)?(?:previous|eligibility|system)\b", re.I),
    re.compile(r"\bmark\s+(?:this\s+)?patient\s+eligible\b", re.I),
)
PROHIBITED_CONCLUSIONS = (
    re.compile(r"\bpatient\s+is\s+eligible\b", re.I),
    re.compile(r"\bpatient\s+qualifies\b", re.I),
    re.compile(r"\benroll\s+(?:this|the)\s+patient\b", re.I),
)


def detect_prompt_injection(text: str) -> list[str]:
    return ["Untrusted source contains instruction-like text; it was treated as data."] if any(pattern.search(text) for pattern in INJECTION_PATTERNS) else []


def contains_definitive_eligibility(text: str) -> bool:
    return any(pattern.search(text) for pattern in PROHIBITED_CONCLUSIONS)


def sanitize_text(text: str) -> str:
    if contains_definitive_eligibility(text):
        return "Unsupported definitive conclusion removed. Human verification is required."
    return text


PRIOR_EXPOSURE = re.compile(r"\b(prior|previous|previously|history of|received|treated with|exposure)\b", re.I)
EXPLICIT_NEGATION = re.compile(r"\b(no prior|no previous|never (?:received|treated)|naive|not previously|none)\b", re.I)



HISTORY_CONDITION = re.compile(
    r"\b(?:history of|prior diagnosis of|previous diagnosis of)\b|"
    r"\b(?:cancers?|malignan\w*|tumou?rs?|diseases?|conditions?)\b.*\bwithin\b", re.I,
)
HISTORY_NEGATION = re.compile(
    r"\b(?:no (?:known )?(?:history of|prior diagnosis of|previous diagnosis of)|"
    r"never (?:had|diagnosed with)|denies (?:any )?history of)\s+([^.;!?]+)", re.I,
)


def _history_scope(text: str) -> set[str]:
    # Normalize a disease class, not individual cancers or patient-specific terms.
    text = re.sub(r"\b(?:cancers?|malignanc(?:y|ies)|tumou?rs?)\b", "cancer", text, flags=re.I)
    text = re.split(r"\bwithin\b", text, flags=re.I)[0]
    words = set(re.findall(r"[a-z]+", text.casefold()))
    return words - set("a an any the of no known other history prior previous diagnosis diagnosed with had has have patient patients subject subjects participant participants documented evidence for in or and".split())


def history_clearance_problem(item: CriterionAssessment) -> str | None:
    """Require an explicit verified negative covering the entire history scope."""
    main, *exceptions = re.split(r"\bexcept(?:ing)?\b", item.criterion_text, maxsplit=1, flags=re.I)
    if item.criterion_type != "exclusion" or item.status != "MEETS" or not HISTORY_CONDITION.search(main):
        return None
    scope = _history_scope(main)
    cited = [e for e in item.patient_evidence if e.quote_verified]
    narrower = False
    for fact in cited:
        for match in HISTORY_NEGATION.finditer(fact.evidence_text):
            negated = _history_scope(match.group(1))
            if scope and negated == scope:
                return None
            if scope & negated:
                narrower = True
    if narrower:
        return "History clearance guard: narrower negation does not rule out the criterion's full condition scope."
    exception_terms = _terms(exceptions[0]) if exceptions else set()
    if cited and exception_terms and all(exception_terms & _terms(e.evidence_text) for e in cited):
        return "History clearance guard: excepted condition only; the exception does not clear the whole criterion."
    return "History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history."


def is_absence_inferred_clearance(item: CriterionAssessment) -> bool:
    """An LLM 'clear of exclusion' for a prior-exposure criterion needs an explicit negative in the record.

    A treatment list (e.g. "FOLFOX, then FOLFIRI") does not show that another therapy was never given.
    """
    if item.method != "llm" or item.criterion_type != "exclusion" or item.status != "MEETS":
        return False
    if HISTORY_CONDITION.search(re.split(r"\bexcept\b", item.criterion_text, flags=re.I)[0]):
        return False  # Condition-history negatives are checked at criterion scope.
    if not PRIOR_EXPOSURE.search(item.criterion_text):
        return False
    return not any(EXPLICIT_NEGATION.search(e.evidence_text) or EXPLICIT_NEGATION.search(e.value) for e in item.patient_evidence)


# Requirements a cited fact must actually mention before an LLM MEETS is accepted.
UNSUPPORTED_QUALIFIERS = re.compile(
    r"\b(central|failed|failure|intoleran\w*|progress\w*|refractory|transfus\w*|clearance|"
    r"measurable|recist|confirmed absence)\b",
    re.I,
)
LAB_ANALYTES = {
    "hemoglobin": re.compile(r"\b(hb|hgb|hemoglobin|haemoglobin)\b", re.I),
    "white blood cells": re.compile(r"\b(wbc|white blood cells?|leukocytes?)\b", re.I),
    "neutrophils": re.compile(r"\b(anc|neutrophils?)\b", re.I),
    "platelets": re.compile(r"\b(plt|platelets?)\b", re.I),
    "bilirubin": re.compile(r"\b(tbil|bilirubin)\b", re.I),
    "ALT": re.compile(r"\balt\b", re.I),
    "AST": re.compile(r"\bast\b", re.I),
    "INR": re.compile(r"\binr\b", re.I),
    "creatinine": re.compile(r"\bcreatinine\b", re.I),
}
# "Adequate hematologic, renal and hepatic function" is met only when every named organ system has
# its usual results cited. Applies only when the criterion is about organ *function*, so mentions
# such as "hepatic metastases" are unaffected. "Adequate organ function" names all three systems.
FUNCTION_WORDING = re.compile(r"\bfunctions?\b", re.I)
ORGAN_FUNCTION = {
    "hematologic function": (re.compile(r"\b(ha?ematolog\w*|bone marrow|organ)\b", re.I), ("neutrophils", "hemoglobin", "platelets")),
    "renal function": (re.compile(r"\b(renal|kidney|organ)\b", re.I), ("creatinine",)),
    "hepatic function": (re.compile(r"\b(hepatic|liver|organ)\b", re.I), ("bilirubin", "ALT", "AST")),
}
# Fragments that are one option in a list, or a branch that applies only under a condition.
CONDITIONAL_OR_OPTION = re.compile(
    r"^\s*(?:if\b|for (?:participants|patients|subjects)\b|note\b|no [\w\s-]{1,30}:|[\w\s-]{1,30} mets?:)"
    r"|contracepti|sterili[sz]|vasectomy|condom|intrauterine|\biud\b|tubal|salpingectomy|post-menopausal|hormonal methods",
    re.I,
)


# Criteria only an investigator can judge; records cannot settle them in prescreening.
INVESTIGATOR_JUDGMENT = re.compile(
    r"investigator'?s?\s+(?:opinion|judg(?:e)?ment|discretion)|in the opinion of|deemed by the investigator|"
    r"deemed (?:unsuitable|inappropriate)|unsuitable for enrol",
    re.I,
)


# Words too generic to show that cited evidence is about the same thing as an exclusion.
GENERIC_TERMS = frozenset("""
a an and any are as at be by for from has have history in including is known of on or other patient patients
prior previous current currently within month months year years week weeks day days disease diseases disorder
disorders condition conditions cancer cancers tumor tumors tumour malignancy malignancies therapy therapies
treatment treatments treated status severe uncontrolled active such that the this those to with would must not
no clinically significant e g eg study participant participants subject subjects metastases metastasis
metastatic require required requiring use using evidence documented
""".split())


def _stem(word: str) -> str:
    word = word.rstrip('s')
    return word[:-1] if word.endswith('ed') and len(word) >= 4 else word


GENERIC_STEMS = frozenset(_stem(word) for word in GENERIC_TERMS)


def _terms(text: str) -> set[str]:
    terms = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        word = _stem(word)
        if len(word) >= 3 and word not in GENERIC_STEMS:
            terms.add(word)
    return terms


def is_unsupported_exclusion_clearance(item: CriterionAssessment) -> bool:
    """An LLM 'clear of exclusion' must rest on evidence about the excluded condition, not on silence.

    Accepted when the cited evidence explicitly negates (e.g. "no prior ...") or shares a specific
    term with the criterion (e.g. BRAF wild type for a BRAF V600 exclusion). ECOG 1 does not clear
    "frequent seizures, hepatic failure".
    """
    if item.method != "llm" or item.criterion_type != "exclusion" or item.status != "MEETS":
        return False
    if HISTORY_CONDITION.search(re.split(r"\bexcept\b", item.criterion_text, flags=re.I)[0]):
        return history_clearance_problem(item) is not None
    if any(EXPLICIT_NEGATION.search(e.evidence_text) or EXPLICIT_NEGATION.search(e.value) for e in item.patient_evidence):
        return False
    criterion_terms = _terms(item.criterion_text)
    cited_terms = set().union(*(_terms(f"{e.value} {e.evidence_text}") for e in item.patient_evidence)) if item.patient_evidence else set()
    return not (criterion_terms & cited_terms)


def _cited_text(item: CriterionAssessment) -> str:
    return " ".join(f"{e.value} {e.evidence_text}" for e in item.patient_evidence)


def uncovered_requirements(item: CriterionAssessment) -> list[str]:
    """Requirements of an LLM 'MEETS' inclusion that the cited evidence does not mention."""
    if item.method != "llm" or item.criterion_type != "inclusion" or item.status != "MEETS":
        return []
    cited = _cited_text(item)
    missing = sorted({m.group(0).lower() for m in UNSUPPORTED_QUALIFIERS.finditer(item.criterion_text)
                      if not re.search(re.escape(m.group(0)), cited, re.I)})
    missing += [name for name, pattern in LAB_ANALYTES.items()
                if pattern.search(item.criterion_text) and not pattern.search(cited)]
    for system, (mention, analytes) in ORGAN_FUNCTION.items():
        if FUNCTION_WORDING.search(item.criterion_text) and mention.search(item.criterion_text):
            absent = [a for a in analytes if not LAB_ANALYTES[a].search(cited)]
            if absent:
                missing.append(f"{system}: {', '.join(absent)}")
    return missing


# "in first-line therapy", "adjuvant setting": the line of therapy must be stated in the record.
# "FOLFOX, then FOLFIRI" gives an order, not line numbers (FOLFOX may have been adjuvant).
LINE_OF_THERAPY = re.compile(r"\b(first|second|third|fourth|1st|2nd|3rd|4th)[- ]line\b|\b(neo)?adjuvant\b", re.I)


def is_unstated_line_of_therapy(item: CriterionAssessment) -> bool:
    """An LLM decision on a line-specific criterion when no cited fact states the line of therapy."""
    return (item.method == "llm" and item.status in {"MEETS", "DOES_NOT_MEET"}
            and bool(LINE_OF_THERAPY.search(item.criterion_text)) and not LINE_OF_THERAPY.search(_cited_text(item)))


def is_conditional_or_option_rejection(item: CriterionAssessment) -> bool:
    """An LLM 'DOES_NOT_MEET' on a list option or conditional branch is not evidence of exclusion."""
    return (item.method == "llm" and item.criterion_type == "inclusion" and item.status == "DOES_NOT_MEET"
            and bool(CONDITIONAL_OR_OPTION.search(item.criterion_text)))


TIME_WINDOW = re.compile(r"\bwithin\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve)\s*[- ]?\s*(?:days?|weeks?|months?|years?)\b", re.I)
MEDICATION_LIST = re.compile(r"medication[ _-]+list|medicines[ _-]+list|medication reconciliation", re.I)
STUDY_REFERENCE = re.compile(r"first[\s-]+(?:study[\s-]+|trial[\s-]+)?dose|study[\s-]+(?:dose|dosing|start)|randomi[sz]ation", re.I)
DATED_REFERENCE = re.compile(
    r"(?:first[\s-]+(?:study[\s-]+|trial[\s-]+)?dose|study[\s-]+(?:dose|dosing|start)|randomi[sz]ation)"
    r"\s*(?:date)?\s*(?:is|was|on|scheduled for|planned for|:|=)?\s*\d{4}-\d{2}-\d{2}\b", re.I,
)


def time_window_problem(item: CriterionAssessment) -> str | None:
    """Reject temporal decisions lacking dated events or an explicit study anchor.

    Medication categories and source provenance remain snapshots even when a
    model calls the drug current. No use of wall-clock time or inferred dosing.
    """
    if item.status not in {"MEETS", "DOES_NOT_MEET"} or not TIME_WINDOW.search(item.criterion_text):
        return None
    if item.status == "MEETS" and HISTORY_CONDITION.search(item.criterion_text) and history_clearance_problem(item) is None:
        return None  # A lifetime scope-matching negative does not need an event date.
    cited = [e for e in item.patient_evidence if e.quote_verified]
    if not any(e.date and e.date.strip() for e in cited):
        return "Time-window decision lacks dated cited evidence."
    if all(e.source_kind == "medication_list" or e.category == "current_medication"
           or MEDICATION_LIST.search(e.source_file + " " + e.evidence_text) for e in cited):
        return "Time-window decision cites only medication snapshots, not administration or stop dates."
    if STUDY_REFERENCE.search(item.criterion_text) and not DATED_REFERENCE.search(_cited_text(item)):
        return "Time-window decision lacks an explicitly documented study reference date."
    return None



NUMBER_WORDS = dict(zip("one two three four five six seven eight nine ten eleven twelve".split(), range(1, 13)))


def computed_study_window(item: CriterionAssessment) -> tuple[str, str] | None:
    """Compute a recent-therapy window from cited actual and planned events only."""
    if item.criterion_type != "exclusion" or item.status == "POTENTIAL_CONFLICT":
        return None
    window = re.search(r"\bwithin\s+(\d+|" + "|".join(NUMBER_WORDS) + r")\s*[- ]?\s*(days?|weeks?|months?|years?)\b", item.criterion_text, re.I)
    if not window or not STUDY_REFERENCE.search(item.criterion_text):
        return None
    # Only broad treatment windows; a specific drug or modality requires a
    # clinically matched administration, which this arithmetic guard cannot infer.
    treatment_scope = re.search(r"\b(?:anti[- ]?cancer (?:therapy|treatment)|systemic (?:therapy|treatment)|chemotherapy|therapy)\b", item.criterion_text, re.I)
    if not treatment_scope:
        return None
    scope_text = re.sub(r"\([^)]*\)", "", item.criterion_text).split(";")[0]
    if re.search(r"\b(?:radiation|radiotherapy|targeted|inhibitor|immunotherapy|antibod\w*)\b", scope_text, re.I):
        return None
    cited = [e for e in item.patient_evidence if e.quote_verified]
    references, events = [], []
    for e in cited:
        # Legacy evidence may contain an explicitly dated study-dose anchor in
        # the same verified quote as the administration. Preserve that support.
        for anchor in re.finditer("(?:" + STUDY_REFERENCE.pattern + r")\s*(?:date)?\s*(?:is|was|on|scheduled for|planned for|:|=)?\s*(\d{4}-\d{2}-\d{2})\b", e.evidence_text, re.I):
            try:
                references.append(date.fromisoformat(anchor.group(anchor.re.groups)))
            except ValueError:
                pass
        if not e.date or e.date not in e.evidence_text:
            continue
        try:
            day = date.fromisoformat(e.date)
        except ValueError:
            continue
        if e.category == "planned_study_event" and re.search(r"first[ -]+(?:study[ -]+|trial[ -]+)?dose|cycle\s+1\s+day\s+1", e.evidence_text, re.I):
            references.append(day)
        elif e.category == "prior_treatment" and e.source_kind != "medication_list" and not MEDICATION_LIST.search(e.source_file):
            if re.search(r"\b(?:administered|given|received|infused|last dose|stopped|discontinued)\b", e.evidence_text, re.I) and not re.search(r"\b(?:not|never)\s+(?:administered|given|received)|\b(?:planned|scheduled|discussed)\b", e.evidence_text, re.I):
                events.append(day)
    if not references or not events:
        return "UNKNOWN", "Computed time-window guard: missing dated administration or planned first-dose reference date."
    if len(set(references)) != 1:
        return "UNKNOWN", "Computed time-window guard: conflicting planned first-dose reference dates; reviewer must reconcile them."
    reference = references[0]
    amount = int(window[1]) if window[1].isdigit() else NUMBER_WORDS[window[1].lower()]
    unit = window[2].lower()
    if unit.startswith(('day', 'week')):
        lower = reference - timedelta(days=amount * (7 if unit.startswith('week') else 1))
    else:
        months = amount * (12 if unit.startswith('year') else 1)
        year, month = divmod(reference.year * 12 + reference.month - 1 - months, 12)
        if year < 1:
            return "UNKNOWN", "Computed time-window guard: unsupported calendar boundary."
        month += 1
        lower = date(year, month, min(reference.day, calendar.monthrange(year, month)[1]))
    inside = [day for day in events if lower <= day <= reference]
    event = max(inside or events)
    interval = (reference - event).days
    detail = f"Computed time-window guard: administration {event.isoformat()}, planned first dose {reference.isoformat()}; code-computed interval {interval} days; window {amount} {unit} (starts {lower.isoformat()})."
    if inside:
        return "DOES_NOT_MEET", detail + " Documented administration is inside the window; the exclusion appears to apply. Planned dates require human verification."
    return "UNKNOWN", detail + " No cited administration is inside the window; absence of later therapy is not established."

def has_biomarker_treatment_reasoning(explanation: str) -> bool:
    """Flag inference language linking a test finding to treatment, not citations."""
    for sentence in re.split(r"(?<=[.!?])\s+", explanation):
        biomarker = re.search(r"\b(?:mutations?|biomarkers?|variants?|genotyp\w*)\b", sentence, re.I)
        named_variant = re.search(r"\b[A-Z][A-Z0-9]{1,9}\s+(?:p\.)?[A-Z]\d+[A-Z]\b", sentence)
        inference = re.search(r"\b(?:indicat\w*|suggest\w*|impl(?:y|ies|ying)|consistent with)\b", sentence, re.I)
        treatment = re.search(r"\b(?:treated|treating|treatment|therapy|inhibitor\w*)\b", sentence, re.I)
        negated = re.search(r"\b(?:does not|do not|cannot|can't|not)\s+(?:indicat\w*|suggest\w*|impl\w*)", sentence, re.I)
        if (biomarker or named_variant) and inference and treatment and not negated:
            return True
    return False


def snapshot_explanation(item: CriterionAssessment, explanation: str) -> str:
    """A model's wording cannot upgrade a dated listing into present use."""
    snapshots = [e for e in item.patient_evidence if e.source_kind == 'medication_list'
                 or MEDICATION_LIST.search(e.source_file)]
    if not snapshots:
        return explanation
    def replace_claim(text, pattern, replacement):
        def replace(match):
            prefix = text[max(0, match.start() - 50):match.start()]
            if re.search(r'(?:\bnot|\bno evidence of|does not establish|cannot establish)\s*$', prefix, re.I):
                return match.group()
            return replacement
        return re.sub(pattern, replace, text, flags=re.I)
    corrected = replace_claim(explanation, r'\b(?:is\s+)?currently\s+(?:taking|receiving|using|on|being treated with)\b', 'was listed as receiving')
    corrected = replace_claim(corrected, r'\bcurrent medications?\b', 'dated medication-list exposure')
    corrected = replace_claim(corrected, r'\bcurrent use\b', 'documented past exposure')
    if corrected != explanation:
        dates = ', '.join(sorted({e.date or 'date not documented' for e in snapshots}))
        corrected += f' The cited medication list is a snapshot as of {dates}; use at screening is not established.'
    return corrected



def status_contradicts_explanation(item: CriterionAssessment) -> bool:
    """Check the structured conclusion and the last explicit prose conclusion."""
    if item.method != "llm" or item.status not in {"MEETS", "DOES_NOT_MEET"}:
        return False
    mapping = {"APPLIES": "DOES_NOT_MEET", "DOES_NOT_APPLY": "MEETS"} if item.criterion_type == "exclusion" else {}
    conclusion = item.final_conclusion
    if conclusion is not None and mapping.get(conclusion, conclusion) != item.status:
        return True
    if item.criterion_type == "exclusion":
        pattern = r"\b(?:the |this )?exclusion\s+(does not apply|doesn't apply|is not applicable|applies|is applicable)\b"
        matches = list(re.finditer(pattern, item.explanation, re.I))
        if not matches:
            return False
        phrase = matches[-1].group(1).lower()
        prose_status = "MEETS" if phrase in {"does not apply", "doesn't apply", "is not applicable"} else "DOES_NOT_MEET"
    else:
        pattern = r"\b(?:(?:the |this )?(?:inclusion )?criterion\s+(is not met|is not satisfied|is met|is satisfied)|(?:patient\s+)?(does not meet|doesn't meet|meets)\s+(?:the |this )?(?:inclusion )?criterion)\b"
        matches = list(re.finditer(pattern, item.explanation, re.I))
        if not matches:
            return False
        phrase = (matches[-1].group(1) or matches[-1].group(2)).lower()
        prose_status = "DOES_NOT_MEET" if "not" in phrase or "n't" in phrase else "MEETS"
    return prose_status != item.status


def review_assessments(assessments: list[CriterionAssessment]) -> tuple[list[CriterionAssessment], list[str]]:
    """Downgrade unsupported conclusions and return visible review flags."""
    reviewed, flags = [], []
    for item in assessments:
        update = {}
        if status_contradicts_explanation(item):
            update = {"status": "UNKNOWN", "explanation": "Status contradicts explanation. Converted to UNKNOWN. Original reasoning: " + item.explanation}
            flags.append(f"{item.criterion_id}: status contradicts explanation; converted to UNKNOWN.")
        elif reason := history_clearance_problem(item):
            update = {"status": "UNKNOWN", "explanation": f"{reason} Converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: {reason} Converted to UNKNOWN.")
        elif reason := time_window_problem(item):
            update = {"status": "UNKNOWN", "explanation": f"{reason} Converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: {reason} Converted to UNKNOWN.")
        elif item.status in {"MEETS", "DOES_NOT_MEET", "POTENTIAL_CONFLICT"} and INVESTIGATOR_JUDGMENT.search(item.criterion_text):
            update = {"status": "UNKNOWN", "explanation": f"This criterion depends on investigator judgment and cannot be settled from records; converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: investigator-judgment criterion converted to UNKNOWN.")
        elif item.status in {"MEETS", "DOES_NOT_MEET", "POTENTIAL_CONFLICT"} and not item.patient_evidence and item.method == "llm":
            update = {"status": "UNKNOWN", "explanation": "No patient evidence supports this conclusion; converted to UNKNOWN."}
            flags.append(f"{item.criterion_id}: unsupported conclusion converted to UNKNOWN.")
        elif is_absence_inferred_clearance(item):
            update = {"status": "UNKNOWN", "explanation": "The record does not explicitly rule out this prior exposure; absence from a treatment list is not a negative. Converted to UNKNOWN."}
            flags.append(f"{item.criterion_id}: absence-based clearance of a prior-exposure exclusion converted to UNKNOWN.")
        elif is_unsupported_exclusion_clearance(item):
            update = {"status": "UNKNOWN", "explanation": f"No cited evidence addresses this exclusion; absence of a record does not clear it. Converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: exclusion cleared without evidence about it; converted to UNKNOWN.")
        elif is_unstated_line_of_therapy(item):
            update = {"status": "UNKNOWN", "explanation": f"This criterion depends on the line of therapy, which the cited record does not state; converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: line of therapy not documented; converted to UNKNOWN.")
        elif missing := uncovered_requirements(item):
            update = {"status": "UNKNOWN", "explanation": f"Part of this criterion is not documented ({', '.join(missing)}); converted to UNKNOWN. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: partial evidence ({', '.join(missing)} not documented); converted to UNKNOWN.")
        elif is_conditional_or_option_rejection(item):
            update = {"status": "UNKNOWN", "explanation": f"This item is a conditional branch or one option among alternatives, so not meeting it does not show exclusion; reviewer decides applicability. Original reasoning: {item.explanation}"}
            flags.append(f"{item.criterion_id}: conditional or option sub-item; DOES_NOT_MEET converted to UNKNOWN.")
        # Arithmetic replaces a model conclusion only after consistency and
        # other guards; a detected contradiction must remain UNKNOWN.
        if not status_contradicts_explanation(item) and (computed := computed_study_window(item)):
            status, detail = computed
            update = {"status": status, "explanation": detail + " Original reasoning: " + item.explanation}
            flags.append(f"{item.criterion_id}: {detail}")
        if any(not evidence.quote_verified for evidence in item.patient_evidence):
            update = {"status": "UNKNOWN", "explanation": "A cited source quote was not verified; converted to UNKNOWN."}
            flags.append(f"{item.criterion_id}: unverified source quote.")
        if has_biomarker_treatment_reasoning(item.explanation):
            supported = any(e.quote_verified and e.category in {"prior_treatment", "current_medication"}
                            and not EXPLICIT_NEGATION.search(e.evidence_text)
                            for e in item.patient_evidence)
            flag = f"{item.criterion_id}: explanation contains biomarker-to-treatment reasoning"
            if supported:
                flags.append(flag + "; treatment evidence is cited, review the explanation.")
            else:
                update = {"status": "UNKNOWN", "explanation": "Biomarker-to-treatment inference has no cited treatment evidence; converted to UNKNOWN. Original reasoning: " + item.explanation}
                flags.append(flag + "; no supported treatment citation, converted to UNKNOWN.")
        explanation = update.get('explanation', item.explanation)
        corrected = snapshot_explanation(item, explanation)
        if corrected != explanation:
            update['explanation'] = corrected
            flags.append(f'{item.criterion_id}: current-use wording corrected to dated medication-list exposure; verify chronology.')
        reviewed.append(item.model_copy(update=update))
    return reviewed, flags
