# Daily Reflection Tree

**DT Fellowship Assignment — Knowledge Engineering Submission**

A deterministic end-of-day reflection tool. The employee answers fixed-choice questions; the tree branches based on their answers; they leave with a reflection on how they showed up. No LLM at runtime. Same answers always produce the same path.

---

## Repository Structure

```
/tree/
  reflection-tree.json     ← Part A: full tree (35 nodes, JSON)
  reflection-tree.tsv      ← Part A: same tree in TSV format (for readability)
  tree-diagram.md          ← Part A: Mermaid branching diagram

/agent/
  index.html               ← Part B: web UI (open in browser via local server)
  agent.py                 ← Part B: CLI agent (Python, no dependencies)

/transcripts/
  persona-1-transcript.md  ← victim / entitled / self-centric path
  persona-2-transcript.md  ← victor / contribution / altrocentric path

write-up.md                ← Part A: design rationale (2 pages)
README.md                  ← this file
```

---

## Running the Web UI (Recommended)

```bash
cd agent/
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

The web UI loads `../tree/reflection-tree.json` at runtime. Dark-themed, mobile-friendly, no dependencies.

## Running the CLI Agent

```bash
python3 agent/agent.py
# or with a custom tree path:
python3 agent/agent.py tree/reflection-tree.json
# or with transcript output:
python3 agent/agent.py tree/reflection-tree.json my-session.md
```

Python 3.8+. No pip installs required.

---

## Reading the Tree

Open `tree/reflection-tree.json`. Each node has:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `parentId` | Parent in the tree hierarchy |
| `type` | `start` `question` `decision` `reflection` `bridge` `summary` `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` is replaced with their earlier answer. |
| `options` | For questions: selectable choices. For decisions: routing rules. |
| `target` | Explicit jump (bridges, reflections). Null = follow first child. |
| `signal` | State tally: `axis1:internal`, `axis2:entitlement`, etc. |

### Tracing a path without running code

1. Start at `START`
2. Follow `target` (or first child by `parentId`) to the next node
3. At `question` nodes: employee picks an option, it's stored as `answers[nodeId]`
4. At `decision` nodes: match stored answers to routing rules → jump to target
5. At `reflection`/`bridge` nodes: follow `target`
6. `SUMMARY` interpolates `{axis1.summary}` etc. from the accumulated signals
7. End at `END`

### Decision routing format

```
answer=Option A|Option B:TARGET_NODE
answer=Option C:OTHER_TARGET
```

Rules are semicolon-separated in the TSV, array items in JSON.

---

## The Three Axes

| Axis | Spectrum | Sources |
|------|----------|---------|
| Locus | Internal ↔ External | Rotter (1954), Dweck (2006) |
| Orientation | Contribution ↔ Entitlement | Organ (1988), Campbell et al. (2004) |
| Radius | Altrocentric ↔ Self-centric | Maslow (1969), Batson (2011) |

The axes are sequenced intentionally. Axis 1 (agency) sets the frame; Axis 2 (contribution) asks how that agency was directed; Axis 3 (radius) asks whose world you were living in while doing it.

---

## Key Design Constraints Observed

- **No LLM at runtime** — tree loads from JSON, branches on string matching, interpolates templates
- **Fixed options only** — no free text input anywhere
- **Deterministic** — same answers → same path → same reflection, every session
- **No moralizing** — every path produces a useful, non-shaming reflection
