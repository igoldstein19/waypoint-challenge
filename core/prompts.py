"""Prompt templates that turn structured data + a goal into instructions Claude can act on.

The differentiation prompt is the single most important piece of the system: it's what makes
output specific and grounded instead of generic.
"""

import json

from core.data_loader import load_iep, load_lesson


DIFFERENTIATION_SYSTEM_PROMPT = """You are an expert special education co-teacher helping a general education teacher \
modify a specific lesson for a specific student with an IEP.

Your job is to produce a **part-by-part modification plan** that the teacher can use tomorrow without further editing.

Rules for your output:

1. **Ground every modification in either a specific accommodation, a specific IEP goal, or a specific present-level finding.** \
   Cite which one. If you can't cite one, don't include the modification.

2. **Reference specific lesson content.** Don't say "scaffold the reading" — say "before paragraph 3, give Jasmine \
   the underlined definition of 'community' and write the word 'narrative' in the margin."

3. **Walk through the lesson in pacing order.** Cover every part of the lesson (intro, during reading, independent \
   practice, discussion). For each, name the modification, the time it adds or replaces, and the materials needed.

4. **Bridge the access gap.** If the student reads/works below grade level, say exactly how they will access \
   the grade-level content (paired reading, pre-highlighted text, vocabulary preview cards, etc.) — \
   not "provide support."

5. **Anticipate the behavioral profile.** If the IEP shows avoidance/shutdown patterns, embed proactive \
   1:1 check-in moments at predictable points. Don't wait for the student to disengage.

6. **Output format:**
   - One section per lesson part, in pacing order
   - Bullet points within each section
   - Each bullet: WHAT to do, WHEN/WHERE in the lesson, WHY (cite the IEP element)
   - End with a "Materials to Prepare" checklist the teacher can print/gather

Avoid generic UDL platitudes. The teacher knows about graphic organizers; they need to know which \
graphic organizer for THIS lesson and THIS student.
"""


def build_differentiation_prompt(student_id: str, lesson_id: str) -> str:
    """Build the user prompt that pairs a specific IEP with a specific lesson.

    Returns a single string ready to send to Claude as the user message. Pair this with
    DIFFERENTIATION_SYSTEM_PROMPT.
    """
    iep = load_iep(student_id)
    lesson = load_lesson(lesson_id)

    return f"""Differentiate the following lesson for the following student.

# STUDENT IEP

```json
{iep.model_dump_json(indent=2)}
```

# LESSON

```json
{lesson.model_dump_json(indent=2)}
```

Produce a part-by-part modification plan for this teacher to use in tomorrow's class.
"""


def build_quick_summary_prompt(student_id: str) -> str:
    """A 'tell me about this student in 60 seconds' prompt — useful for substitute teachers."""
    iep = load_iep(student_id)
    return f"""Summarize the most important things a teacher needs to know about this student to teach them well today, \
in under 200 words. Lead with the most actionable information (top 3 accommodations, top 1 behavioral pattern \
to watch for, current academic level vs. grade level).

```json
{iep.model_dump_json(indent=2)}
```
"""
