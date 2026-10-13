---
title: "Confidence labels A–D (canonical definition)"
canonical: true
---

# Confidence labels A–D: the one definition

**This is the only definition of A/B/C/D.** Every other page (takeoff rules, three-stage method, payment structure, order of operations, steps, briefs) points here. In Reader v4 the code (`bpr-v4/bpr4/quantity.py`) computes these labels from the ledgers. The Reader's own label is a ceiling, never a floor.

Every quantity carries **two labels**:
- **Drawing confidence**: how well the physical count or length is known.
- **Payment confidence**: how well we know which pay item it goes to.

The headline label on a pay item is the lower of the two. Payment doubt never lowers drawing confidence, and drawing doubt never lowers payment confidence.

## Checks
A check counts only if it is **recorded** in the ledger: `{kind, result: agree|disagree, detail}` with a detail saying what was compared, or a sheet or evidence ref. Flags like `checked: true`, `verified`, or a bare `split_checked: true` never count.

An **independent check** compares the value with a *different* source:
- another view or sheet (plan vs profile, plan vs detail);
- an actual symbol count on the tiles (Rule 31);
- a measurement against a printed label (vector or station geometry vs the profile band);
- a blind Checker "yes" on a verifier task;
- a schedule or table against a count.

Checks that are **not independent** are **consistency checks**. They can support B but never A. All of them together count as **one** check, however many times the label is re-read. For a **counted fitting** (bend, valve, tee, hydrant, reducer, cap, service) they never give B on their own; see Rule 31:
- re-reading the same label (text layer vs image, OCR vs text, the same callout found again, the same label repeated at a match line on the next sheet);
- station arithmetic on the same labels;
- adding up your own numbers twice.

## Drawing confidence
| Label | Needs all of |
|---|---|
| **A** | A printed value (figured dimension, label, schedule row), **and** at least one recorded **independent** check that agrees, **and** none of the C caps below. |
| **B** | One unambiguous source, a complete count or sum (every summand present), and at least one recorded second check that agrees (independent or consistency). No C cap applies. |
| **C** | Any of these caps: an open conflict touching it; a ranked-precedence reading (Rule 34, shown as *provisional*); a length that disagrees between two methods (with an engineer question, never "X or Y"); a shared leader or unclear note scope; incomplete coverage of its sheets or categories; an open network flag (Rule 23); a quantity resting on scaling when the set says DO NOT SCALE (Rule 37); a split between two pay items not checked instance by instance; a `partial` quantity; a visible number committed under Rule 33; an inferred value; no recorded second check. |
| **D** | An assumption: length × typical width (`lxw`), an area with no piece list, or a value with no drawing basis. |

## Payment confidence
| Label | Needs |
|---|---|
| **A** | A cited clause that explicitly names this component (or its pay line) and how it is paid, with the clause wording quoted. |
| **B** | A cited clause that clearly covers it by category or location (e.g. a tie-in named by location, Rule 14), with no payment question open. |
| **C** | Allocation inferred from general wording, or any payment or scope question raised about the item (Rule 3), or "included" without the quoted clause (Rule 21), or a ranked reading of a payment conflict. |
| **D** | No basis found, or clauses that conflict and can't be ranked: allocation `unresolved`. |

## Never
- Never write "X or Y" as a quantity. Commit the ranked reading (Rule 34) at C, show the alternative in Notes, and ask.
- Never leave a number blank because it is uncertain. Give the number with its label. Unknown is `unresolved, not zero`.
- Never raise a label because a reading was copied twice or a flag says "checked".
- An A means "read correctly from the documents", not "correct for construction".

## Where enforced
`quantity.component_confidence` (drawing), `quantity.payment_confidence` (payment) and `gates.py`. Calibration targets (grading-method-v2): A at least 98% correct, B at least 90%.
