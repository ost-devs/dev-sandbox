"""Token usage of a Claude Code session, read from its transcripts (main + subagents).

units = input + 1.25 * cache_write + 0.1 * cache_read + 5 * output: the price ratios
of the Claude API, so units are proportional to cost for any one model.
"""
import json
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
WEIGHTS = {"input_tokens": 1.0, "cache_creation_input_tokens": 1.25,
           "cache_read_input_tokens": 0.1, "output_tokens": 5.0}


def transcripts(sid):
    files = list(PROJECTS.glob(f"*/{sid}.jsonl"))
    for main in files[:1]:
        side = main.parent / sid
        if side.is_dir():
            files += sorted(side.rglob("*.jsonl"))
    return files


def _messages(sid):
    for f in transcripts(sid):
        for line in f.read_text(errors="replace").splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if isinstance(m, dict):
                yield f, d, m


def session_usage(sid):
    seen = {}
    for f, d, m in _messages(sid):
        u = m.get("usage")
        if d.get("type") == "assistant" and u:
            key = (m.get("id") or d.get("uuid"), d.get("requestId"))
            seen[key] = (m.get("model", "?"), u)  # streamed chunks repeat the id; keep the last
    tot = {k: 0 for k in WEIGHTS}
    by_model = {}
    for model, u in seen.values():
        bm = by_model.setdefault(model, {k: 0 for k in WEIGHTS})
        for k in WEIGHTS:
            v = u.get(k) or 0
            tot[k] += v
            bm[k] += v
    units = sum(WEIGHTS[k] * tot[k] for k in WEIGHTS)
    return {"units": round(units), "tokens": sum(tot.values()), **tot,
            "by_model": by_model, "messages": len(seen)}


def skill_calls(sid):
    out = []
    for _f, d, m in _messages(sid):
        if d.get("type") != "assistant" or not isinstance(m.get("content"), list):
            continue
        for b in m["content"]:
            if b.get("type") == "tool_use" and b.get("name") == "Skill":
                out.append(b.get("input", {}).get("skill"))
            if b.get("type") == "tool_use" and b.get("name") == "Read" and "token-economy" in str(b.get("input")):
                out.append("read:" + str(b["input"].get("file_path")))
    return out


def subagent_count(sid):
    ids = set()
    for _f, d, m in _messages(sid):
        if d.get("type") == "assistant" and isinstance(m.get("content"), list):
            for b in m["content"]:
                if b.get("type") == "tool_use" and b.get("name") in ("Agent", "Task"):
                    ids.add(b.get("id"))
    return len(ids)


if __name__ == "__main__":
    import sys
    print(json.dumps(session_usage(sys.argv[1]), indent=1))
