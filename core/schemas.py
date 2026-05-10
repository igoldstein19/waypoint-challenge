"""Pydantic schemas for student IEPs and lessons.

These shape how Claude reads our data: clean semantic sections instead of raw PDF text.
"""

from pydantic import BaseModel, Field


class StudentInfo(BaseModel):
    name: str
    student_id: str
    grade: int
    age: int
    disability: list[str]
    school: str
    primary_language: str = "English"


class PresentLevel(BaseModel):
    """Present level of academic or functional performance in one area."""

    area: str = Field(description="Subject area or domain, e.g. 'ela', 'math', 'behavioral'")
    current_grade_level: int | None = Field(
        default=None, description="Functional grade level if measured (e.g. 3 for 3rd grade reading)"
    )
    subcategories: dict[str, int] | None = Field(
        default=None, description="Sub-skill levels, e.g. {'vocabulary': 3, 'lit_comprehension': 3}"
    )
    summary: str = Field(description="Narrative description of current performance")
    strengths: str = Field(description="Strengths, interests, preferences")
    impact_of_disability: str = Field(description="How the disability affects general ed access")


class Accommodations(BaseModel):
    """Accommodations grouped by category. These are environmental/procedural supports.

    Distinct from modifications, which change what the student is expected to learn or produce.
    """

    presentation: list[str] = Field(default_factory=list)
    response: list[str] = Field(default_factory=list)
    timing: list[str] = Field(default_factory=list)
    setting: list[str] = Field(default_factory=list)


class Modifications(BaseModel):
    content: list[str] = Field(default_factory=list)
    instruction: list[str] = Field(default_factory=list)
    student_output: list[str] = Field(default_factory=list)


class Goal(BaseModel):
    """A measurable annual IEP goal."""

    goal_id: int
    area: str = Field(description="Goal domain, e.g. 'Counseling/Self-Regulation', 'ELA'")
    baseline: str = Field(description="What the student can currently do")
    annual_target: str = Field(description="Skill the student should attain by end of IEP year")
    measurement_criteria: str = Field(description="e.g. 'From 50% to 75%' or '4 of 5 opportunities'")
    method: str = Field(description="How progress is measured")
    schedule: str = Field(description="How frequently progress is reported")
    person_responsible: str
    benchmarks: list[str] = Field(description="Short-term objectives between baseline and annual target")


class Service(BaseModel):
    goal_ids: list[int]
    type_of_service: str
    provided_by: str
    location: str
    frequency: str
    duration_minutes: int
    direct_or_consultation: str = Field(description="'consultation', 'direct_in_general_ed', or 'direct_other'")


class StudentVision(BaseModel):
    this_year: dict[str, str] = Field(default_factory=dict, description="Subject-specific goals")
    long_term: list[str] = Field(default_factory=list)


class IEP(BaseModel):
    """Structured IEP document."""

    student: StudentInfo
    iep_dates: dict[str, str] = Field(description="from/to dates for IEP validity")
    parent_concerns: str = ""
    student_vision: StudentVision
    present_levels: list[PresentLevel]
    accommodations: Accommodations
    modifications: Modifications
    goals: list[Goal]
    services: list[Service]
    placement: str = Field(description="e.g. 'Full Inclusion Program'")
    assessment_accommodations: list[str] = Field(default_factory=list)


# ---------- Lesson schemas ----------


class LessonQuestion(BaseModel):
    """A During Reading question or discussion question."""

    label: str = Field(description="e.g. 'A', 'B', '1', '2'")
    question_type: str = Field(description="'think_share', 'write', 'turn_talk', 'find_evidence', 'mcq'")
    optional: bool = False
    prompt: str
    sample_answer: str | None = None
    options: list[str] | None = None  # for MCQ


class LessonPart(BaseModel):
    """One pacing segment of a lesson."""

    name: str = Field(description="'intro', 'during_reading', 'independent_practice', 'discussion'")
    duration_minutes: int
    description: str
    modality: str | None = Field(default=None, description="'whole_class', 'partner', 'independent', 'mixed'")
    paragraphs_covered: list[int] | None = None
    text: str | None = Field(default=None, description="The student-facing text for this part, if any")
    questions: list[LessonQuestion] = Field(default_factory=list)
    short_response_prompt: str | None = None
    self_checklist: list[str] | None = None


class Lesson(BaseModel):
    """Structured lesson document."""

    lesson_id: str
    title: str
    author: str | None = None
    text_type: str = Field(description="'informational', 'short_story', 'poem', 'essay', etc.")
    grade: int
    subject: str
    unit: str
    lesson_number: int
    skill_focus: str
    standard: str = Field(description="e.g. 'RI.7.2'")
    duration_minutes: int
    purpose: str
    knowledge_focus: str
    vocabulary: list[str]
    teacher_notes: list[str] = Field(default_factory=list)
    parts: list[LessonPart]
    full_text_by_paragraph: dict[int, str] = Field(
        default_factory=dict,
        description="Paragraph number → paragraph text. Lets Claude cite specific paragraphs in modifications.",
    )
