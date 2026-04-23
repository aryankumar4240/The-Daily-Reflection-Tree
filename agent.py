#!/usr/bin/env python3
"""
Daily Reflection Tree — CLI Agent
Loads reflection-tree.json and walks deterministically through the tree.
No LLM calls. No third-party dependencies. Python 3.8+.

Usage:
  python3 agent.py                          # uses ../tree/reflection-tree.json
  python3 agent.py path/to/tree.json        # custom tree path
  python3 agent.py tree.json transcript.md  # save session transcript
"""

import json, os, re, sys, time
from pathlib import Path

# ── Colours ──────────────────────────────────────────────────────────────────
R = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
CY = "\033[96m"; YL = "\033[93m"; GR = "\033[92m"; MG = "\033[95m"; GY = "\033[90m"

def p(text, c="", bold=False, end="\n"):
    print(f"{BOLD if bold else ''}{c}{text}{R}", end=end, flush=True)

def slow(text, c="", delay=0.014):
    for ch in text:
        print(f"{c}{ch}{R}", end="", flush=True)
        time.sleep(delay)
    print()

def hr(): p("─"*58, GY)
def blank(): print()

# ── Tree loading ──────────────────────────────────────────────────────────────
def load(path):
    with open(path) as f:
        data = json.load(f)
    return data, {n["id"]: n for n in data["nodes"]}

# ── State helpers ─────────────────────────────────────────────────────────────
def tally(state, signal):
    if not signal: return
    axis, pole = signal.split(":")
    state["signals"].setdefault(axis, {})
    state["signals"][axis][pole] = state["signals"][axis].get(pole, 0) + 1

def dominant(state, axis):
    poles = state["signals"].get(axis, {})
    return max(poles, key=poles.get) if poles else None

def interpolate(text, state, tree_data):
    def sub(m):
        ref = m.group(1)
        if ".answer" in ref:
            return state["answers"].get(ref.replace(".answer",""), ref)
        if ".summary" in ref:
            axis = ref.replace(".summary","")
            pole = dominant(state, axis)
            s = next((n for n in tree_data["nodes"] if n["type"]=="summary"), None)
            return s["summaryTemplates"].get(axis,{}).get(pole,"") if s else ""
        return ref
    return re.sub(r"\{([^}]+)\}", sub, text) if text else text

# ── Routing ───────────────────────────────────────────────────────────────────
def route(node, state):
    for rule in node.get("options", []):
        if rule.startswith("answer="):
            values_part, target = rule[7:].rsplit(":", 1)
            values = [v.strip() for v in values_part.split("|")]
            if any(a in values for a in state["answers"].values()):
                return target.strip()
    return None

def child(parent_id, idx):
    return idx.get(next((n["id"] for n in idx.values()
                         if n.get("parentId") == parent_id), None))

# ── Renderers ─────────────────────────────────────────────────────────────────
def render_start(node, log):
    blank(); hr()
    p("  🌙  DAILY REFLECTION", CY, bold=True); hr(); blank()
    slow(f"  {node['text']}", "")
    blank(); input(f"  {DIM}[Press Enter to begin]{R}")
    log.append(f"\n[START]\n  {node['text']}")

def render_bridge(node, log):
    blank(); p(f"  — {node['text']} —", MG)
    blank(); time.sleep(1.0)
    log.append(f"\n[BRIDGE] {node['text']}")

def render_question(node, state, tree_data, log):
    blank()
    text = interpolate(node["text"], state, tree_data)
    p(f"  {text}", "", bold=True); blank()
    for i, opt in enumerate(node["options"], 1):
        p(f"    {GY}{i}.{R}  {opt}")
    blank()
    while True:
        try:
            raw = input(f"  {CY}Your answer (1-{len(node['options'])}): {R}").strip()
            idx = int(raw) - 1
            if 0 <= idx < len(node["options"]):
                chosen = node["options"][idx]
                state["answers"][node["id"]] = chosen
                log.append(f"\n[QUESTION] {text}\n  → {chosen}")
                return chosen
        except (ValueError, KeyboardInterrupt):
            pass
        p(f"  Please enter a number 1-{len(node['options'])}", GY)

def render_reflection(node, state, tree_data, log):
    blank(); hr()
    text = interpolate(node["text"], state, tree_data)
    slow(f"  {text}", YL, delay=0.011)
    hr(); blank()
    input(f"  {DIM}[Press Enter to continue]{R}")
    log.append(f"\n[REFLECTION]\n  {text}")

def render_summary(node, state, tree_data, log):
    blank(); hr()
    p("  TODAY'S READING", GR, bold=True); hr(); blank()
    state["_summary_templates"] = node.get("summaryTemplates", {})
    text = interpolate(node["text"], state, tree_data)
    for line in text.split("\n"):
        slow(f"  {line}", GR, delay=0.009)
    blank(); hr()
    input(f"  {DIM}[Press Enter to finish]{R}")
    log.append(f"\n[SUMMARY]\n{text}")

def render_end(node, log):
    blank(); slow(f"  {node['text']}", CY); blank()
    log.append(f"\n[END] {node['text']}")

# ── Walker ────────────────────────────────────────────────────────────────────
def walk(tree_data, idx, transcript_path=None):
    state = {"answers": {}, "signals": {}}
    log = []
    cur = "START"

    while cur:
        node = idx.get(cur)
        if not node:
            p(f"\n  [ERROR] Node '{cur}' not found", GY); break

        nt = node["type"]
        tally(state, node.get("signal"))

        if nt == "start":
            render_start(node, log)
            cur = node.get("target") or next(
                (n["id"] for n in tree_data["nodes"] if n.get("parentId") == cur), None)

        elif nt == "question":
            render_question(node, state, tree_data, log)
            cur = next((n["id"] for n in tree_data["nodes"] if n.get("parentId") == cur), None)

        elif nt == "decision":
            cur = route(node, state)

        elif nt == "reflection":
            tally(state, node.get("signal"))
            render_reflection(node, state, tree_data, log)
            cur = node.get("target") or next(
                (n["id"] for n in tree_data["nodes"] if n.get("parentId") == cur), None)

        elif nt == "bridge":
            render_bridge(node, log)
            cur = node.get("target") or next(
                (n["id"] for n in tree_data["nodes"] if n.get("parentId") == cur), None)

        elif nt == "summary":
            render_summary(node, state, tree_data, log)
            cur = node.get("target")

        elif nt == "end":
            render_end(node, log); break

        else:
            p(f"  [Unknown type: {nt}]", GY); break

    if transcript_path and log:
        Path(transcript_path).write_text("\n".join(log))
        p(f"\n  Transcript saved → {transcript_path}", GY)

# ── Entry ─────────────────────────────────────────────────────────────────────
def main():
    tree_path = Path(sys.argv[1]) if len(sys.argv) > 1 else \
                Path(__file__).parent.parent / "tree" / "reflection-tree.json"
    transcript = sys.argv[2] if len(sys.argv) > 2 else None

    if not tree_path.exists():
        p(f"Tree not found: {tree_path}", GY); sys.exit(1)

    tree_data, idx = load(str(tree_path))
    os.system("clear" if os.name != "nt" else "cls")
    walk(tree_data, idx, transcript)

if __name__ == "__main__":
    main()
