# Design Write-Up: Daily Reflection Tree

**DT Fellowship — Knowledge Engineering Rationale**

---

## Why These Questions

The hardest constraint in this assignment is the one that looks easy: fixed options only. No free text. This forces a decision that most survey designers avoid — you have to commit to the actual shape of human experience in advance. If your options don't capture the real spectrum, the employee will click through to the nearest approximation and leave with a reflection that doesn't fit.

I made three decisions that shaped every question in the tree:

**1. The opening question sets the emotional frame without naming it.** The first question is: *"When you think about today as a whole, which of these comes closest to how it felt?"* The options use a structural metaphor — "I moved through it" vs "it moved through me" — rather than asking directly about agency or control. This matters because asking "did you feel in control today?" primes the employee to perform the right answer. The metaphor asks them to locate themselves honestly. The diagnostic work happens through how they interpret the language, not through their awareness of being diagnosed.

**2. Follow-up questions must be worth asking.** The first question per axis sorts employees into a branch. The second question, within that branch, is where the real reflection happens. For the internal-locus branch: *"Think of one moment today where something went the way you wanted it to. What was your actual role in that?"* This question is doing three things simultaneously — anchoring the employee to a specific memory (not a general self-assessment), asking about role rather than outcome, and offering "I'm not sure — it might have just worked out" as a legitimate option. That fourth option is intentional. It's the growth-mindset diagnostic: someone with a strong internal locus will usually resist attributing their success to luck.

**3. The options must be genuinely distinguishable under fatigue.** I tested every option set by asking: would a tired, slightly frustrated person at 7pm choose differently between B and C? If the answer was no, I rewrote them. The Axis 2 contribution question — *"When you gave today — what was underneath it?"* — went through six drafts before the options ("person needed it," "right thing to do even though it cost me," "wanted to be seen," "it was automatic") felt like genuinely different things a real person might recognize in themselves.

---

## How I Designed the Branching

The tree uses a two-depth structure per axis: one sorting question routes to two branches, then a second question within each branch produces the specific reflection. This gives 4 reflection nodes per axis and 16 possible complete paths.

**The opening question is the key structural choice.** Rather than routing on a single word (the sample TSV uses "Tough|Productive|Mixed|Frustrating"), I route on a structural description of the employee's relationship to their day. This produces cleaner branch semantics — the internal branch question can assume the employee already sees themselves as having had some agency, and probe specifically into *how* they exercised it.

**Trade-off: binary routing vs. per-option routing.** Each of my 4-option questions collapses into 2 branches. A tree with per-option routing would produce 256 distinct paths instead of 16, but would require 3x the nodes and 3x the reflection writing. More importantly, the marginal gain in precision decreases fast — the difference between "I noticed something shifting" and "I kept energy up when others were losing it" is real but small. Both indicate an internal orientation. The reflection they deserve is the same.

**Trade-off: axis-linked vs. independent questions.** The assignment specifies that axes must flow as a sequence, not three independent quizzes. I implemented this through the bridge nodes, which explicitly name the transition ("from how you moved through the day — to what you gave while you were in it"), and through the Axis 2 opening, which assumes the Axis 1 frame is now in the employee's mind. The Axis 2 question asks about "one interaction" — a more grounded anchor than "how was your day" — because by Axis 2, the employee has already been thinking about specific moments for 2-3 minutes.

**Signal accumulation is simple on purpose.** Each question and reflection node carries a signal tag (e.g., `axis1:internal`). The summary node reads the dominant pole per axis and selects the appropriate template. There's no weighting, no scoring model, no sentiment analysis. The intelligence is in the question design, not the scoring system.

---

## Psychological Sources

**Axis 1 — Locus of Control (Rotter, 1954):** I operationalised the internal/external distinction through attribution — where the employee's mind goes when something goes wrong. Rotter's original scale asks participants to choose between paired statements ("When I make plans, I am almost certain I can make them work" vs "It is not always wise to plan too far ahead because many things turn out to be a matter of luck"). I adapted this structure: offer options that attribute causation to self vs. circumstances, and let the employee choose.

**Growth Mindset (Dweck, 2006):** The "I'm not sure — it might have just worked out" option on the internal-branch question is specifically designed to catch fixed-mindset attribution of success to luck. Dweck's research shows that people with fixed mindsets often avoid claiming credit for success (it might reveal that they're not as capable as they appear) while people with growth mindsets are more likely to connect outcomes to their own process. The reflection for this option explicitly names the pattern: "Luck doesn't explain patterns."

**Axis 2 — Organizational Citizenship Behavior (Organ, 1988):** OCB is discretionary effort beyond formal requirements — altruistic helping, conscientiousness, civic virtue. My Axis 2 contribution question probes for this through the motivation question ("what was underneath it?"), which distinguishes genuine OCB from impression management. The options "wanted to be seen as someone who helps" and "it was automatic" are both contribution-coded but get different reflections, acknowledging the psychological difference.

**Psychological Entitlement (Campbell et al., 2004):** Campbell's work identifies entitlement as a stable belief in deserving more than others, independent of contribution. My entitlement questions probe not the belief directly but the behavioral signal — pulling back effort when recognition isn't received. The reflection for this path ("the withdrawal usually costs you more than it costs the person who didn't give you what you needed") names the dynamic without shaming.

**Axis 3 — Self-Transcendence (Maslow, 1969):** Maslow's 1969 paper argued that the healthiest humans operate from a frame beyond self-actualization — oriented toward something larger than personal fulfillment. My Axis 3 questions operationalise this as "who was in your mind" during difficulty. The options progress from self-referential ("my deadline, my reputation") to collective ("the bigger picture — what we're all actually trying to do"), capturing the continuum Maslow described.

**Perspective-Taking (Batson, 2011):** Batson's distinction between imagining another's perspective and feeling what they feel is encoded in the Axis 3 follow-up: *"Did that awareness change anything about how you acted — or did it mostly change how you felt?"* Batson's research shows that perspective-taking without behavioral change is common — you can feel for someone and still act entirely in your own interest. The tree treats awareness-that-changed-behavior as a distinct and rarer thing from awareness-that-didn't.

---

## What I'd Improve With More Time

**1. Per-option routing at Axis 2.** The contribution axis is the most psychologically nuanced, and collapsing 4 options into 2 branches loses the most resolution there. "Wanted to be seen" and "it was automatic" are meaningfully different motivations — the first is impression management, the second is genuine OCB that's become habitual. They deserve different reflections.

**2. Cross-axis interpolation in the summary.** The current summary uses separate sentences per axis. A richer version would look for patterns across axes: "You said you moved through the day — and then described giving something without making it a transaction. Those are the same impulse." The data is there in the answer state. The templates just need more conditionals.

**3. Longitudinal tracking.** A single session gives one reading. Meaningful reflection happens over time — when the tool can say "this is the third time this week your attention went outward in a hard moment" or "you've been in the external locus branch every day this week." The data model supports this; the storage layer doesn't exist yet.

**4. The Axis 3 self branch.** The "I kept it entirely to myself" option currently collapses into the same A3_R_SELF reflection as "people probably noticed, but I said nothing." These are meaningfully different — one is deliberate concealment, one is uncertainty. A third branch for the protective option already exists (A3_R_PROTECTIVE), but the other two could be split further.
