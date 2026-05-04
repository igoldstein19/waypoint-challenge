# Waypoint Challenge: The Special Education Starter Kit

Build an MCP server that helps a teacher differentiate instruction for a student with an Individualized Education Program (IEP).

**Prize:** $500 to the winner. Top 5 submissions get an immediate final-round interview for the founding engineer role at [Waypoint Learning] The challenge is designed to take no more than a few hours.

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

Feel free to research [Universal Design for Learning (UDL)] and other pedagogical frameworks. The ability to learn quickly is part of what we're evaluating.

## Getting Started

### Prerequisites

- Node.js 18+ (for TypeScript) **or** Python 3.10+ (for Python)
- An Anthropic API key or Claude Desktop installed
- Familiarity with the [Model Context Protocol]

### Setup

```bash
git clone https://github.com/waypoint-learning/waypoint-challenge.git
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

## About Waypoint Learning

Waypoint is building AI tools that help teachers serve students with disabilities — not just faster paperwork, but fundamentally better instruction. We believe the highest-leverage point in education is the teacher, and the hardest thing teachers do is differentiate instruction for students with diverse learning needs.

Founder & CEO: Isaac Goldstein studied CS at Stanford and is finishing is MBA at Harvard. He hasive years in education at EY-Parthenon, BCG, and Great Minds, where he led a 330-person curriculum implementation team - and he's looking to partner with a great engineer to build a very impactful business.
