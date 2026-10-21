"""Render preserved source logs. Normalize display wrappers, never source records."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parent
NAMES = {'A': 'Letter Studio', 'B': 'Referral Brief', 'C': 'Practice Relay'}
TIME_KEYS = ('timestamp_utc', 'received_at_utc', 'time', 'source_review_recorded_at_utc', 'completed_at_utc', 'date')


def first_value(*objects, keys):
    for obj in objects:
        for key in keys:
            if obj.get(key) is not None:
                return obj[key], key
    return None, None


def load_record(key, phase):
    filename = f'{key}.json' if phase == 'initial_build' else f'update-{key}.json'
    source = ROOT / 'logs' / filename
    raw_bytes = source.read_bytes()
    raw_text = raw_bytes.decode('utf-8')
    raw = json.loads(raw_text)
    entries = raw.get('exchanges')
    if entries is None:
        entries = [raw] if raw.get('prompt') else []
    if phase == 'initial_build' and len(entries) != 5:
        raise SystemExit(f'{filename}: expected the five historical exchanges')
    if not entries:
        raise SystemExit(f'{filename}: no actual prompts found')
    display = []
    for index, entry in enumerate(entries, 1):
        prompt = entry.get('prompt')
        outcome, outcome_key = first_value(entry, keys=('result', 'outcome'))
        if not isinstance(prompt, str) or not prompt or outcome is None:
            raise SystemExit(f'{filename}: incomplete prompt/outcome record {index}')
        identifier, id_key = first_value(entry, keys=('id', 'exchange'))
        timestamp, time_key = first_value(entry, raw, keys=TIME_KEYS)
        purpose, _ = first_value(entry, raw, keys=('purpose',))
        validation, _ = first_value(entry, raw, keys=('validation', 'verification'))
        provenance, _ = first_value(entry, raw, keys=('attribution', 'authorship', 'author'))
        display.append({
            'display_label': identifier or f'{key} current update {index}',
            'display_label_basis': id_key or 'generated display label, not a historical prompt ID',
            'source_entry': index,
            'timestamp': timestamp,
            'timestamp_source_field': time_key,
            'time_basis': entry.get('time_basis', raw.get('time_basis')),
            'from': entry.get('from', raw.get('from', 'AI assistant')),
            'to': entry.get('to', raw.get('to', 'coding agent')),
            'provenance': provenance or 'AI assistant → coding agent',
            'purpose': purpose,
            'exact_prompt': prompt,
            'recorded_outcome': outcome,
            'outcome_source_field': outcome_key,
            'recorded_validation': validation,
        })
    return {
        'prototype_key': key,
        'prototype_name': NAMES[key],
        'phase': phase,
        'source_file': f'logs/{filename}',
        'source_sha256': hashlib.sha256(raw_bytes).hexdigest(),
        'source_bytes': len(raw_bytes),
        'exchange_count': len(display),
        'display_exchanges': display,
        'raw_record': raw,
        'raw_json': raw_text,
    }


initial = [load_record(key, 'initial_build') for key in NAMES]
updates = [load_record(key, 'current_revision') for key in NAMES]
initial_count = sum(item['exchange_count'] for item in initial)
update_count = sum(item['exchange_count'] for item in updates)
record = {
    'schema_version': '2.0',
    'title': 'ReferralFlow AI — development prompt history and current revisions',
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'provenance': 'Actual AI-assistant-to-coding-agent development exchanges. No student authorship is claimed. The initial build records and the later revision records remain separate.',
    'historical_context': 'Earlier prompt constraints and validation results describe the initial build. They are historical records, not instructions governing the current revision or evidence that the current files passed those earlier checks.',
    'preservation': 'Source files were read without modification. Display wrappers normalize differing schemas; raw_record preserves all parsed values and raw_json preserves the original UTF-8 text. Source hashes refer to those unmodified log files.',
    'evidence_limits': 'These records document requests, purposes, outcomes and builder-reported technical checks. They do not establish browser visual QA, real customer use, clinical validity, student/team rehearsals, class votes, payments or willingness to pay.',
    'counts': {'prototypes': len(NAMES), 'initial_build_exchanges': initial_count, 'current_revision_exchanges': update_count, 'total_recorded_exchanges': initial_count + update_count},
    'initial_build': initial,
    'current_revisions': updates,
}


def fmt(value):
    text = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    return html.escape(text, quote=True)


def content(value):
    if value is None:
        return '<p class="small">Not separately recorded; see the exact request.</p>'
    if isinstance(value, list):
        return '<ul class="outcomes">' + ''.join(f'<li>{fmt(item)}</li>' for item in value) + '</ul>'
    if isinstance(value, dict):
        return f'<pre class="record-text">{fmt(value)}</pre>'
    return f'<p class="record-text">{fmt(value)}</p>'


def exchange_markup(entry, phase):
    timestamp = entry['timestamp'] or 'Timestamp not recorded'
    meta = f'{fmt(entry["from"])} → {fmt(entry["to"])} · {fmt(timestamp)}'
    parts = [f'<article class="exchange"><h3>{fmt(entry["display_label"])}</h3><p class="small metadata">{meta}</p>']
    if entry.get('time_basis'):
        parts.append(f'<p class="small">Time basis: {fmt(entry["time_basis"])}</p>')
    parts.extend(['<h4>Recorded purpose</h4>', content(entry['purpose']), '<h4>Recorded outcome</h4>', content(entry['recorded_outcome'])])
    parts.append(f'<details class="prompt"><summary>Read the exact prompt</summary><pre class="prompt-text">{fmt(entry["exact_prompt"])}</pre></details>')
    if entry['recorded_validation'] is not None:
        label = 'Historical builder checks — earlier version' if phase == 'initial_build' else 'Builder-reported checks for this revision'
        parts.append(f'<details class="checks"><summary>{label}</summary>{content(entry["recorded_validation"])}</details>')
    return ''.join(parts) + '</article>'


def prototype_markup(item):
    key = item['prototype_key']
    heading = f'{key} · {item["prototype_name"]}'
    plural = 's' if item['exchange_count'] != 1 else ''
    source = f'<p class="small source-record">Source: <code>{fmt(item["source_file"])}</code> · {item["exchange_count"]} actual exchange{plural}. Original source record is preserved in the JSON download.</p>'
    exchanges = ''.join(exchange_markup(entry, item['phase']) for entry in item['display_exchanges'])
    if item['phase'] == 'initial_build':
        return f'<details class="card history-group" id="history-{key}"><summary><span>{heading}</span><span class="pill">5 historical exchanges</span></summary>{source}{exchanges}</details>'
    return f'<section class="card revision-group" id="revision-{key}"><div class="revision-heading"><h3>{heading}</h3><span class="pill">Current revision</span></div>{source}{exchanges}</section>'


css = '''
.log-counts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:26px 0}.log-counts .card{margin:0;padding:20px}.count-number{font-size:32px;font-weight:750;letter-spacing:-1px;line-height:1.1}.count-label{font-size:13px;color:var(--muted);margin-top:8px}.jump-links{display:flex;gap:10px 20px;flex-wrap:wrap;margin:20px 0 30px;font-size:13px}.section-intro{max-width:900px;color:var(--muted)}.revision-heading{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap}.revision-heading h3{margin:0}.source-record{margin:10px 0 19px;line-height:1.8}.exchange{padding-top:22px;margin-top:22px;border-top:1px solid var(--line)}.exchange h3{font-size:16px;margin-bottom:6px}.metadata{margin:0 0 12px;overflow-wrap:anywhere}.exchange h4{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#52647e;margin:20px 0 8px}.record-text{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.75 system-ui,sans-serif;margin:0 0 14px;color:#344b66}.outcomes{font-size:14px;line-height:1.75;color:#344b66;margin:0;padding-left:20px}.prompt,.checks{border:1px solid var(--line);border-radius:8px;background:#fafcff;padding:0 14px;margin:17px 0 0}.prompt summary,.checks summary{font-size:13px;min-height:44px;display:list-item;align-content:center}.prompt[open] summary,.checks[open] summary{margin-bottom:8px}.prompt-text{padding:12px 0 15px;border-top:1px solid #e4eaf3;margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.8 system-ui,sans-serif;color:#334d6e}.checks .record-text{font-size:12px;line-height:1.8}.checks{padding-bottom:4px}.history-group>summary{display:flex;align-items:center;justify-content:space-between;gap:14px;list-style:none}.history-group>summary::before{content:'+';font-size:21px;font-weight:500;color:var(--blue)}.history-group[open]>summary::before{content:'−'}.history-group>summary>span:first-child{margin-right:auto}.history-group .exchange:first-of-type{margin-top:15px}.limit-note{font-size:13px;line-height:1.8;color:var(--muted);max-width:930px}.label-current{font-weight:750;text-decoration:underline;text-underline-offset:5px}.section-divider{border:0;border-top:1px solid var(--line);margin:45px 0 0}
@media(max-width:700px){.log-counts{gap:9px}.log-counts .card{padding:16px 12px}.count-number{font-size:27px}.count-label{font-size:12px}.history-group>summary{flex-wrap:wrap;gap:8px}.history-group>summary .pill{margin-left:24px}.record-text,.outcomes{font-size:14px}.prompt-text{font-size:13px}.revision-group,.history-group{padding:18px}.jump-links{gap:14px 20px}}
@media print{.jump-links,.download-link{display:none}.prompt-text,.record-text,.outcomes{font-size:10px}.exchange{break-inside:avoid}.card{break-inside:auto}.log-counts{grid-template-columns:repeat(3,1fr)}}
'''
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prompt history & revisions | ReferralFlow</title><link rel="stylesheet" href="site.css"><style>''' + css + '''</style></head><body>
<a class="skip" href="#main">Skip to content</a><header><a class="brand" href="index.html"><span class="mark">RF</span>ReferralFlow</a><nav aria-label="Main"><a href="index.html">Prototypes</a><a href="guide.html">Presentation guide</a><a href="evaluate.html">Test record</a><a href="evidence.html">Evidence</a><a class="label-current" href="development-log.html" aria-current="page">Prompt log</a></nav></header>
<main id="main"><div class="eyebrow">Development record · 20 October 2026</div><h1>Initial prompts.<br>Current revisions.</h1><p class="lede">The actual requests, purposes and recorded outcomes behind Letter Studio, Referral Brief and Practice Relay.</p>
<div class="notice"><strong>Authorship: AI assistant → coding agent.</strong> These are real development exchanges recorded during the user-authorized work. They are not attributed to students. Initial build history and later revisions are shown separately; timestamps and exact prompt wording remain as recorded.</div>
<div class="log-counts" aria-label="Recorded exchange counts"><div class="card"><div class="count-number">''' + str(initial_count) + '''</div><div class="count-label">Initial exchanges<br>5 per prototype</div></div><div class="card"><div class="count-number">''' + str(update_count) + '''</div><div class="count-label">Current revision exchanges<br>Recorded separately</div></div><div class="card"><div class="count-number">''' + str(initial_count + update_count) + '''</div><div class="count-label">Total actual exchanges<br>Across 3 prototypes</div></div></div>
<div class="row download-link"><a class="button" href="development-log.json" download>Download complete JSON record</a><span class="small">Includes the original source text and hashes.</span></div>
<nav class="jump-links" aria-label="Prompt log sections"><a href="#current-revisions">Current revisions</a><a href="#initial-history">Initial history</a><a href="#revision-A">A update</a><a href="#revision-B">B update</a><a href="#revision-C">C update</a></nav>
<section id="current-revisions"><h2>Current revisions</h2><p class="section-intro">These follow-up records describe the latest bounded updates to the three prototype pages. The purpose and outcome below come from each builder’s source record. Differing source schemas are normalized only for display; the complete raw records are preserved in the download.</p>''' + ''.join(prototype_markup(item) for item in updates) + '''</section>
<hr class="section-divider"><section id="initial-history"><h2>Initial build history</h2><p class="section-intro">Five original exchanges are retained for each prototype. Expand a prototype, then an exact prompt, to inspect the request and recorded result.</p><div class="notice"><strong>Historical context, not current instructions.</strong> Requirements in these earlier prompts—including instructions to build from a blank file—describe the initial build. They do not govern the present revision. Earlier “frozen” hashes and checks apply to that earlier version, not automatically to the current files.</div>''' + ''.join(prototype_markup(item) for item in initial) + '''</section>
<h2>What this log establishes</h2><p class="limit-note">It records development instructions and builder-reported outcomes. Technical assertions and DOM-stub checks are distinct from browser visual QA. The prompt records do not establish real customer use, clinical validity, student or team rehearsals, a class vote, payments or willingness to pay. Private source documents and attachments are not included here.</p><p class="limit-note">The source log files remain unchanged. No additional prompts, participant identities or observations have been invented. The exact source text in the JSON download allows each original record to be recovered without relying on the display summary.</p>
</main><footer>Dental Demand Labs · ReferralFlow · <a href="guide.html">Presentation & testing guide</a> · <a href="evidence.html">Evidence & limits</a></footer></body></html>
'''

# Fail before writing if a colleague has changed an input or raw content diverges.
for item in initial + updates:
    source = ROOT / item['source_file']
    if source.read_bytes() != item['raw_json'].encode('utf-8'):
        raise SystemExit(f'Source changed while building: {item["source_file"]}')
    if json.loads(item['raw_json']) != item['raw_record']:
        raise SystemExit(f'Raw source mismatch: {item["source_file"]}')

(ROOT / 'dist' / 'development-log.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
(ROOT / 'dist' / 'development-log.html').write_text(page, encoding='utf-8')
print(f'Development record built: {initial_count} historical + {update_count} current = {initial_count + update_count} actual exchanges; 6 source logs unchanged.')
