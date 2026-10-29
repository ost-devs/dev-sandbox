---
name: token-economy
description: Same result with fewer tokens. Use when planning work whose token cost is large or repeated - several subagents or parallel agents, big reads or outputs, many similar items, long sessions - or when the user asks to cut cost or a run hit a usage limit.
---

# Token economy

The result is fixed: what the user asked for, at the quality they expect. Tokens are the variable. Look for the path that reaches the same result with fewer tokens; take it when it does, not when it doesn't.

Both directions fail:
- Saving by cutting the result: skipping a step that produces evidence, reading less than the task needs, a model or context too small for the job. The rework costs more than the saving.
- Spending as insurance: checks that keep finding nothing, reading everything "to be safe", more agents than the work splits into. Cost with no result.

Where the same result usually costs less:
- Work done twice. Agents each building the same helper, reading the same long instructions, rediscovering the same fact: do it once, write it to a file, share it.
- Output nobody reads. Tool output, logs and long reports go to files; a conversation gets what its next decision needs.
- Size from measurement. Run one unit (a chunk, one subagent) first, see what it cost, then size the rest. Too small pays the fixed cost many times; too large fills a context.
- Work a failure would lose. Agents write results as they go, so a usage limit or crash costs the item in progress, not the run. Agents in parallel hit a usage limit together.
- Checks by their yield. When a measured run shows a check finds little for its cost, tell the user and propose narrowing or dropping it; don't drop it silently.

A small context is not a goal in itself: one that misses what the task needs is the expensive kind.

A choice that trades result for tokens is the user's: say what each path costs and what it gives up.
