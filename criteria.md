# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Across three evaluation trials, no more than 1 of 10 separate pieces of my own writing may receive the high-confidence AI label in any trial.

**Why this target:**

I allow at most one false positive because a mistaken accusation can harm a real writer. Requiring the target in every trial keeps a favorable run from hiding an inconsistent result.

---

## 2.

Across three evaluation trials, the mean combined score for five texts I judge clearly AI-generated must be at least 0.20 higher than the mean combined score for five pieces of my own writing in each trial.

**Why this target:**

The scores need to separate the two groups by a visible margin, not merely rank one example above another. A 0.20 gap is a meaningful target on a 0–1 scale while recognizing that neither signal can prove authorship.

---

## 3.

In each of three evaluation trials, at least one test submission must receive each of the three labels: high-confidence human, unsure, and high-confidence AI.

**Why this target:**

Every label needs to be reachable or it cannot serve its intended purpose. Checking all three in every trial also tests whether the label boundaries behave consistently.

---

## 4.

For a valid appeal against an existing `content_id`, the response must confirm `under_review` and the audit log must contain exactly one appeal record for that content; an appeal using an unknown ID must return `404` and create no appeal record.

**Why this target:**

An appeal is meaningful only if it is acknowledged and leaves a reviewable record. Checking the unknown-ID case guards against telling a writer an appeal succeeded when their submission was not found. I will check this criterion by submitting and appealing a real `content_id`, then inspecting the response and log.

---

## 5.

Requests with missing, null, empty, whitespace-only, or over-20,000-character `text` must not be scored: the first four must return `400`, the oversized request must return `413`, and none may create a decision entry in the audit log.

**Why this target:**

Rejecting malformed and oversized input before scoring gives callers a clear result and avoids spending model work on requests the service cannot use. Checking the audit log makes sure rejected requests are not mistaken for completed decisions.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
