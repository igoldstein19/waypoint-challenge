# Waypoint Learning: The Special Education Challenge

Build an MCP server that helps a teacher differentiate instruction for a student with an Individualized Education Program (IEP).

**Prize:** $500 to the winner. Top 5 submissions get an immediate final-round interview for the founding engineer role at Waypoint Learning The challenge is designed to take no more than a few hours.

**Deadline:** Monday, May 11 @ 12pm ET

---

## The Challenge

Almost 10 million U.S. students have IEPs — legally binding documents that describe exactly what a student needs in the classroom every day. But teachers can't act on them well, because translating a 20+ page IEP into a modified version of tomorrow's lesson takes hours of prep they don't have.

Your job: build an MCP server that gives Claude the context it needs to help a teacher do this in minutes instead of hours.

Given a lesson and a student's IEP, the system should produce **specific, actionable instructional modifications** — scaffolded questions, modified materials, alternative assessments, accommodation reminders. Things a teacher can actually use in the classroom.

## What's in This Repo

lesson/           # Sample lesson from a real K-8 curriculum

iep/              # Sample IEP document (anonymized)

README.md

## What You'll Build

An MCP server (TypeScript or Python) that:

1. Exposes the curriculum and IEP data to Claude as resources and/or tools
2. Lets Claude reason about the intersection of a specific lesson and a specific student's needs
3. Produces concrete modifications a teacher can use without further editing

The architecture is up to you. Some questions worth thinking through:

- How do you chunk and surface the IEP so Claude can reason about goals, accommodations, and present levels effectively?
- How do you ground modifications in *both* the curriculum and the IEP, rather than producing generic strategies?
- What does the teacher actually see and how to they easily navigate the UI/UX of the tool? 

Feel free to research Universal Design for Learning (UDL) and other pedagogical frameworks. The ability to learn quickly is part of what we're evaluating.

This is intentionally open-ended. There's no single "right" architecture. We want to see how you think about structuring domain data for an LLM: what becomes a resource, what becomes a tool, how you handle context, and whether the output is actually useful to a teacher. A thoughtful, well-structured solution that handles one lesson well is better than a sprawling system that handles many lessons poorly.

## Getting Started

### Prerequisites

- Node.js 18+ (for TypeScript) **or** Python 3.10+ (for Python)
- An Anthropic API key or Claude Desktop installed
- Familiarity with the [Model Context Protocol]

### Setup

```bash
git clone https://github.com/igoldstein19/waypoint-challenge.git
cd waypoint-challenge
```

## Evaluation Criteria

We'll evaluate submissions on four dimensions:

| Dimension | What we're looking for |
|---|---|
| **Output quality** | Are the instructional modifications specific, actionable, and grounded in both the curriculum and the IEP? Would a real teacher use this? |
| **Architecture decisions** | How did you structure curriculum and IEP data for Claude? What trade-offs did you make and why? Your README should explain this. |
| **Code quality** | Clean, readable, well-organized. Comments where they matter. Tests if you have time. |
| **Domain understanding** | Does the solution reflect real thinking about what a teacher needs, not just what's technically interesting? How did you provide additional context that increased the quality of output? |

## How to Submit

1. Push your code to a **public GitHub repo**
2. Include a README that:
   - Explains how to run your server
   - Walks through your architecture decisions
   - Shows 1-2 example outputs (lesson + IEP → modifications)
3. Email **isaac@waypoint-learning.org** with:
   - Subject: `Waypoint Challenge: [Your Name]`
   - A link to your repo
   - (Optional) A short demo video

**Deadline: Monday, May 11 @ 12pm ET.** Late submissions won't be considered.

## FAQ

**Can I use models other than Claude?**
Yes, feel free.

**Can I team up?**
Solo submissions only for this round.

**What if it's taking too long?**
A focused, partial solution with clear thinking beats nothing.

**Can I use additional libraries / RAG / fine-tuning / etc.?**
Yes. Use whatever helps you build the best solution.

**I have a question that isn't here.**
Comment in HN or email isaac@waypoint-learning.org.

## A Note on the Data

Please don't redistribute these materials outside the context of this challenge.

## About the Role

We're looking for a founding engineer who wants to build the technical foundation of a company that could genuinely change how millions of students experience school. You'd be working directly with me (Isaac) to go from MVP to full product.

The work involves building AI-powered tools for teachers — ingesting and understanding curriculum, reasoning about IEPs, generating actionable instructional modifications, automating reporting workflows, and creating tight feedback loops so teachers know what's working. The stack is early and flexible.

This role is ideal for a strong engineer who wants massive ownership, cares about education, and is excited about building with LLMs in a domain where the work genuinely matters.

## About Waypoint Learning

Waypoint is building AI tools that help teachers serve students with disabilities by both streamlining administrative work and supporting fundamentally better instruction. We believe the highest-leverage point in education is the teacher, and the hardest thing teachers do is differentiate instruction for students with diverse learning needs.

Founder & CEO: Isaac Goldstein studied CS at Stanford and is finishing is MBA at Harvard. He hasive years in education at EY-Parthenon, BCG, and Great Minds, where he led a 330-person curriculum implementation team - and he's looking to partner with a great engineer to build a very impactful business.

---

# Submission — Waypoint MCP Server

A Python MCP server that gives Claude the structured context it needs to differentiate a lesson for a student with an IEP, in minutes instead of hours. The teacher's UI is **Claude Desktop** — no separate web app, no API key required.

## What's built

```
core/
  schemas.py       # Pydantic models for IEP and Lesson
  data_loader.py   # Filesystem-based loaders (drop-in JSON = new student/lesson)
  prompts.py       # Differentiation system prompt + user prompt builders
data/
  students/jasmine_bailey.json    # Hand-authored from the source IEP PDF
  lessons/unit1_lesson1.json      # Hand-authored from the Community lesson PDF
server.py          # FastMCP server: 5 tools, 6 resources, 2 prompts
requirements.txt
```

**MCP surface exposed to Claude:**

| Type | Name | Purpose |
|---|---|---|
| Tool | `list_students`, `list_lessons` | Discovery |
| Tool | `get_iep_section(student_id, section)` | Pull one IEP section (`accommodations`, `goals`, `present_levels`, etc.) |
| Tool | `get_lesson_part(lesson_id, part_name)` | Pull one lesson part (`intro`, `during_reading`, …) |
| Tool | `differentiate_lesson(student_id, lesson_id)` | **Primary entry point** — bundles full IEP + lesson + the system prompt |
| Resource | `students://list`, `lessons://list`, `iep://{id}`, `iep://{id}/{section}`, `lesson://{id}`, `lesson://{id}/{part}` | Same data as tools, addressable by URI |
| Prompt | `/differentiate <student_id> <lesson_id>` | Slash-command for the core flow |
| Prompt | `/student_snapshot <student_id>` | 60-second briefing (e.g. for a sub) |

## Approach & key decisions

- **Hand-authored structured JSON over PDF parsers.** The IEP and lesson are one-shot demo data; brittle parsing of two specific PDFs would burn time and produce worse data than carefully transcribing what matters into Pydantic-validated JSON. Adding a real PDF ingestion path is a separate, larger problem.
- **Filesystem-based multi-student/multi-lesson scaling.** Adding a student = drop a JSON file in `data/students/`. No code changes, no DB, no vector index. The schema enforces shape; loaders auto-discover.
- **Lesson text is paragraph-keyed** (`full_text_by_paragraph`), so Claude can cite specific paragraphs in modifications instead of saying "scaffold the reading."
- **Both whole-document and section-level access.** Claude can pull `iep://jasmine_bailey/accommodations` for a narrow question, or call `differentiate_lesson` to get everything at once for the full plan. Keeping the surface this way means Claude doesn't burn context when it doesn't need to.
- **Prompt engineering is the highest-leverage piece.** The differentiation system prompt has 6 explicit rules forcing modifications to (1) cite a specific accommodation/goal/present-level finding, (2) reference specific lesson paragraphs/questions, (3) walk the lesson in pacing order, (4) bridge the access gap concretely, (5) anticipate Jasmine's avoidance/shutdown pattern with proactive 1:1 check-ins, and (6) output in a teacher-actionable format ending with a Materials checklist.
- **No fine-tuning, no vector RAG.** Both fail the cost/benefit test for a corpus this small (one IEP, one lesson). The whole problem fits in Claude's context window. Structured retrieval via MCP tools beats both for grounding.
- **Claude Desktop as the UI.** The README brief asks for an MCP server; Claude Desktop is the canonical client. Building a separate Streamlit app would be lower fidelity than the chat surface teachers will actually use.

## How to run & test

### 1. Install

```bash
pip install -r requirements.txt
```

This installs `mcp[cli]` and `pydantic`. No API key needed.

### 2. Configure Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "waypoint": {
      "command": "<absolute path to python.exe in your env>",
      "args": ["<absolute path>/server.py"]
    }
  }
}
```

Use the absolute path to the `python` where you ran `pip install` — easiest is the venv's `python.exe`.

**Fully quit Claude Desktop** (tray icon → Quit, not just close window) and reopen. The tools menu in the chat composer should now show **waypoint** with 5 tools.

### 3. Try these prompts

| Prompt | What to expect |
|---|---|
| `What students and lessons are available?` | Claude calls `list_students` / `list_lessons` |
| `What are Jasmine Bailey's accommodations?` | Claude calls `get_iep_section` and lists presentation/response/timing/setting accommodations |
| `Differentiate the lesson "What is 'Community' and Why is it Important?" for Jasmine Bailey.` | Part-by-part modification plan, paragraph-grounded, with a Materials checklist |
| `/student_snapshot jasmine_bailey` | <200-word briefing leading with top accommodations + her shutdown pattern |

### 4. What "good output" looks like

For the differentiation prompt, a high-quality answer:

- Walks the lesson **in pacing order** (intro → during reading → independent practice → discussion).
- References **specific paragraphs / question labels** (e.g., "before paragraph 3, pre-teach *narrative* on a vocabulary card") rather than "scaffold the reading."
- Ties each modification back to a **specific IEP element** — accommodation name, goal benchmark, or present-level finding.
- Adds **proactive 1:1 check-ins** at the moments Jasmine is most likely to disengage (independent practice is the obvious risk).
- Ends with a printable **Materials to Prepare** checklist.

Generic UDL platitudes ("provide multiple means of representation") = the system prompt isn't reaching Claude — verify by calling `differentiate_lesson` directly.

### 5. Adding a new student or lesson

Drop a JSON file matching the Pydantic schemas in `core/schemas.py` into `data/students/` or `data/lessons/`. No code, no restart of anything other than Claude Desktop's connection to the server. `list_students` / `list_lessons` will pick it up.

### 6. Troubleshooting

| Symptom | Fix |
|---|---|
| Server doesn't appear in Claude Desktop | Fully quit Claude Desktop (tray → Quit) and reopen. Validate JSON syntax. |
| `ModuleNotFoundError: mcp` in `mcp-server-waypoint.log` | The `command` is using a python without `mcp` installed. Point it at the venv's `python.exe`. |
| `FileNotFoundError: No IEP found...` | The `student_id` must match a JSON filename in `data/students/` (without `.json`). Use `list_students` to discover IDs. |
| Output is generic | Make sure you're invoking `differentiate_lesson` (or `/differentiate`). Free-form questions may not pull the system prompt rules. |
