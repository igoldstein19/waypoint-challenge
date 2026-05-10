"""Filesystem-based data loader.

Adding a new student or lesson = drop a JSON file into data/students/ or data/lessons/.
No code changes required.
"""

import json
from pathlib import Path

from core.schemas import IEP, Lesson

DATA_ROOT = Path(__file__).parent.parent / "data"
STUDENTS_DIR = DATA_ROOT / "students"
LESSONS_DIR = DATA_ROOT / "lessons"


def list_students() -> list[dict[str, str]]:
    """Return summary info for every available student."""
    out = []
    for path in sorted(STUDENTS_DIR.glob("*.json")):
        iep = load_iep(path.stem)
        out.append({
            "student_id": path.stem,
            "name": iep.student.name,
            "grade": iep.student.grade,
            "disability": ", ".join(iep.student.disability),
        })
    return out


def list_lessons() -> list[dict[str, str | int]]:
    """Return summary info for every available lesson."""
    out = []
    for path in sorted(LESSONS_DIR.glob("*.json")):
        lesson = load_lesson(path.stem)
        out.append({
            "lesson_id": path.stem,
            "title": lesson.title,
            "subject": lesson.subject,
            "grade": lesson.grade,
            "duration_minutes": lesson.duration_minutes,
        })
    return out


def load_iep(student_id: str) -> IEP:
    path = STUDENTS_DIR / f"{student_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No IEP found for student '{student_id}'. Available: {[p.stem for p in STUDENTS_DIR.glob('*.json')]}")
    return IEP.model_validate_json(path.read_text(encoding="utf-8"))


def load_lesson(lesson_id: str) -> Lesson:
    path = LESSONS_DIR / f"{lesson_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No lesson found for '{lesson_id}'. Available: {[p.stem for p in LESSONS_DIR.glob('*.json')]}")
    return Lesson.model_validate_json(path.read_text(encoding="utf-8"))


IEP_SECTIONS = {
    "profile": lambda iep: {"student": iep.student.model_dump(), "iep_dates": iep.iep_dates, "placement": iep.placement},
    "present_levels": lambda iep: [pl.model_dump() for pl in iep.present_levels],
    "accommodations": lambda iep: iep.accommodations.model_dump(),
    "modifications": lambda iep: iep.modifications.model_dump(),
    "goals": lambda iep: [g.model_dump() for g in iep.goals],
    "services": lambda iep: [s.model_dump() for s in iep.services],
    "vision": lambda iep: iep.student_vision.model_dump(),
    "assessment_accommodations": lambda iep: iep.assessment_accommodations,
}


def get_iep_section(student_id: str, section: str) -> dict | list:
    """Return one named section of an IEP. Letting Claude pull just what it needs keeps context clean."""
    if section not in IEP_SECTIONS:
        raise ValueError(f"Unknown IEP section '{section}'. Available: {list(IEP_SECTIONS.keys())}")
    iep = load_iep(student_id)
    return IEP_SECTIONS[section](iep)


def get_lesson_part(lesson_id: str, part_name: str) -> dict:
    """Return one part of a lesson (e.g. 'during_reading')."""
    lesson = load_lesson(lesson_id)
    for part in lesson.parts:
        if part.name == part_name:
            return part.model_dump()
    available = [p.name for p in lesson.parts]
    raise ValueError(f"Unknown lesson part '{part_name}'. Available: {available}")
