"""Run queries with the real skill installed; record every tool call up to --max-turns.
Usage: trigger_seq.py eval.json idx,idx,... out.json"""
import json, subprocess, sys, os, concurrent.futures as cf
evals = json.load(open(sys.argv[1])); idx = [int(i) for i in sys.argv[2].split(',')]
env = {k: v for k, v in os.environ.items() if k != 'CLAUDECODE'}
def run(i):
    q = evals[i]['query']
    p = subprocess.run(['claude', '-p', q, '--output-format', 'stream-json', '--verbose',
                        '--max-turns', '2', '--model', 'claude-opus-5-5'],
                       capture_output=True, text=True, cwd='/dev-sandbox', env=env, timeout=600)
    tools, cost = [], None
    for line in p.stdout.splitlines():
        try: e = json.loads(line)
        except ValueError: continue
        if e.get('type') == 'assistant':
            for c in e['message'].get('content', []):
                if c.get('type') == 'tool_use':
                    tools.append(c['name'] + (':' + c['input'].get('skill', '') if c['name'] == 'Skill' else ''))
        if e.get('type') == 'result': cost = e.get('total_cost_usd')
    return {'i': i, 'should': evals[i]['should_trigger'], 'tools': tools, 'cost': cost, 'q': q[:60]}
with cf.ThreadPoolExecutor(5) as ex: res = list(ex.map(run, idx))
json.dump(res, open(sys.argv[3], 'w'), indent=1, ensure_ascii=False)
for r in res: print(r['i'], r['should'], r['cost'], r['tools'])
