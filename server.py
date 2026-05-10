"""Waypoint MCP server.

Exposes student IEPs and lessons to Claude as resources, tools, and prompts so a teacher
can ask Claude to differentiate a specific lesson for a specific student.

Run locally:
    python server.py

Configure in Claude Desktop's claude_desktop_config.json:
    {
      "mcpServers": {
        "waypoint": {
          "command": "python",
          "args": ["<absolute path>/server.py"]
        }
      }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from core import data_loader
from core.prompts import (
    DIFFERENTIATION_SYSTEM_PROMPT,
    build_differentiation_prompt,
    build_quick_summary_prompt,
)

mcp = FastMCP("Waypoint Learning")


# ---------- Resources ----------
# Resources let Claude pull data into context by URI. We expose IEPs and lessons whole
# (for full reasoning) and by section (for narrow questions).


@mcp.resource("students://list")
def students_index() -> str:
    """Index of all available students."""
    students = data_loader.list_students()
    lines = ["# Available Students\n"]
    for s in students:
        lines.append(f"- **{s['name']}** (id: `{s['student_id']}`, grade {s['grade']}, {s['disability']})")
    return "\n".join(lines)


@mcp.resource("lessons://list")
def lessons_index() -> str:
    """Index of all available lessons."""
    lessons = data_loader.list_lessons()
    lines = ["# Available Lessons\n"]
    for l in lessons:
        lines.append(
            f"- **{l['title']}** (id: `{l['lesson_id']}`, grade {l['grade']} {l['subject']}, {l['duration_minutes']} min)"
        )
    return "\n".join(lines)


@mcp.resource("iep://{student_id}")
def iep_full(student_id: str) -> str:
    """Full structured IEP for one student."""
    return data_loader.load_iep(student_id).model_dump_json(indent=2)


@mcp.resource("iep://{student_id}/{section}")
def iep_section(student_id: str, section: str) -> str:
    """One section of an IEP. Sections: profile, present_levels, accommodations, modifications, goals, services, vision, assessment_accommodations."""
    import json

    data = data_loader.get_iep_section(student_id, section)
    return json.dumps(data, indent=2)


@mcp.resource("lesson://{lesson_id}")
def lesson_full(lesson_id: str) -> str:
    """Full structured lesson."""
    return data_loader.load_lesson(lesson_id).model_dump_json(indent=2)


@mcp.resource("lesson://{lesson_id}/{part_name}")
def lesson_part(lesson_id: str, part_name: str) -> str:
    """One part of a lesson. Parts: intro, during_reading, independent_practice, discussion."""
    import json

    return json.dumps(data_loader.get_lesson_part(lesson_id, part_name), indent=2)


# ---------- Tools ----------
# Tools are functions Claude can call. We use tools (rather than resources alone) when
# Claude needs to *act* on parameters or when the data is small and targeted.


@mcp.tool()
def list_students() -> list[dict]:
    """List every student with an IEP available in the system."""
    return data_loader.list_students()


@mcp.tool()
def list_lessons() -> list[dict]:
    """List every lesson available in the system."""
    return data_loader.list_lessons()


@mcp.tool()
def get_iep_section(student_id: str, section: str) -> dict | list:
    """Retrieve one named section of a student's IEP.

    Args:
        student_id: The student's ID (e.g., 'jasmine_bailey'). Use list_students() to discover.
        section: One of 'profile', 'present_levels', 'accommodations', 'modifications',
                 'goals', 'services', 'vision', 'assessment_accommodations'.
    """
    return data_loader.get_iep_section(student_id, section)


@mcp.tool()
def get_lesson_part(lesson_id: str, part_name: str) -> dict:
    """Retrieve one part of a lesson (intro, during_reading, independent_practice, discussion).

    Args:
        lesson_id: The lesson's ID (e.g., 'unit1_lesson1'). Use list_lessons() to discover.
        part_name: One of 'intro', 'during_reading', 'independent_practice', 'discussion'.
    """
    return data_loader.get_lesson_part(lesson_id, part_name)


@mcp.tool()
def differentiate_lesson(student_id: str, lesson_id: str) -> dict:
    """Bundle a student's IEP and a lesson into a single payload for differentiation.

    Use this as the primary entry point when a teacher asks 'modify this lesson for this student.'
    Returns the IEP, lesson, and a system prompt with rules for producing grounded modifications.

    Args:
        student_id: The student's ID (e.g., 'jasmine_bailey').
        lesson_id: The lesson's ID (e.g., 'unit1_lesson1').
    """
    iep = data_loader.load_iep(student_id)
    lesson = data_loader.load_lesson(lesson_id)
    return {
        "system_prompt": DIFFERENTIATION_SYSTEM_PROMPT,
        "instructions": (
            "Produce a part-by-part modification plan grounded in the student's specific accommodations, goals, "
            "and present levels, and tied to specific paragraphs/questions in the lesson. Follow the rules in "
            "system_prompt. Conclude with a 'Materials to Prepare' checklist."
        ),
        "student_iep": iep.model_dump(),
        "lesson": lesson.model_dump(),
    }


# ---------- Prompts ----------
# Prompts are reusable templates a user can invoke (e.g., a "/differentiate" command).


@mcp.prompt()
def differentiate(student_id: str, lesson_id: str) -> str:
    """Build the full differentiation prompt for a (student, lesson) pair.

    The user invokes this in Claude Desktop and the structured IEP + lesson + rules
    are dropped into the conversation.
    """
    return build_differentiation_prompt(student_id, lesson_id)


@mcp.prompt()
def student_snapshot(student_id: str) -> str:
    """Generate a 'tell me about this student in 60 seconds' summary — useful for substitute teachers."""
    return build_quick_summary_prompt(student_id)


if __name__ == "__main__":
    mcp.run()
