# SDAD 4.0 execution examples

Status: W1 candidate meaning contract. These examples describe intended routing;
they are not measured model behavior or a user productivity evaluation.

| Current request or event | Authorized response | Boundary |
| --- | --- | --- |
| "Can you fix the save bug?" / "저장 버그 고쳐줄 수 있어?" | Inspect and implement the named repair, then validate | No repeated approval for the same repair |
| "Why does saving fail?" / "왜 저장이 안 돼?" | Inspect and explain the cause | Explanation alone does not authorize unrelated implementation |
| "Review whether this migration is safe" | Read-only review and concrete findings | Do not execute the migration |
| "Start the adopted development plan" | Reconcile active scope and implement its authorized work | Packaging, release and deployment remain separate actions |
| Relevant test fails during implementation | Debug and repair within scope; rerun relevant checks | Do not report software verification before the check succeeds |
| Production credentials are unavailable | Record missing production evidence and block dependent production claim/action | Continue independent local feature work |
| User corrects the intended account scope | Stop/replan affected work, persist new intent, report impact | Unaffected evidence remains valid only within its original scope |
| A correction was copied | Retain stable ID and unconfirmed delivery state | No inferred acknowledgment, application or process stop |
| A previous correction receives a late response | Link to its exact original correction ID/revision | Do not satisfy the newer correction |
| Agent reports applied changes and a new result revision | Show the report and explicit revision lineage | Report is not independent execution evidence or user acceptance |
| User does not answer an approval request | Keep that protected action pending | Silence is not authorization; unrelated authorized work can continue |
| "Good" after a feature explanation | Briefly acknowledge feedback about that feature | Do not infer unrelated work authorization, a completed test, or whole-product acceptance |
| "Good, implement that" after a concrete change proposal | Implement the named change within the existing scope | Do not request the same authorization again or infer release permission |

`evidence-ready` is narrative report language, not a state enum. Existing
`software_verified`, `owner_accepted` and `production_ready` retain different
evidence/authority requirements. No automatic conversion is introduced.

W5 should compare the old and new interfaces on discovering a scope mismatch,
correcting it, rejecting a stale response, finding the result evidence and
resuming in a new session. Record user explanations, progress questions,
misinterpretations, correction time, evidence lookup time, token/time cost and
authority failures. Current pilot observations and limits are linked from the
v4 README; examples are not evidence that a participant or model passed them.
