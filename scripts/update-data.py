#!/usr/bin/env python3
"""Validate a complete export and atomically replace the Jekyll data file."""
import json
import sys
from datetime import datetime
from pathlib import Path

source = Path(sys.argv[1])
data = json.loads(source.read_text())
if data.get('schema_version') != '1.0' or data.get('status') != 'complete':
    raise SystemExit('Expected a complete schema 1.0 export.')
coverage = data.get('coverage', [])
scopes = {(c['date'], c['direction']) for c in coverage}
dates = {c['date'] for c in coverage}
expected_scopes = {(date, direction) for date in dates
                   for direction in ('paris-marseille', 'marseille-paris')}
if (not dates or scopes != expected_scopes or len(scopes) != len(coverage)
        or not all(c.get('complete') for c in coverage)):
    raise SystemExit('Expected unique, complete searches in both directions for every date.')
ids = set()
for j in data['journeys']:
    if j['id'] in ids or (j['date'], j['direction']) not in scopes:
        raise SystemExit('Duplicate journey or missing search coverage.')
    ids.add(j['id'])
    if not j['autonomous_wheelchair_access'] or data['criterion'] not in j['amenities']:
        raise SystemExit('Journey does not match the accessibility criterion.')
    departure, arrival = map(datetime.fromisoformat, (j['departure'], j['arrival']))
    if departure.tzinfo is None or arrival.tzinfo is None or arrival <= departure:
        raise SystemExit('Expected chronological timestamps with UTC offsets.')
target = Path(__file__).resolve().parents[1] / '_data' / 'journeys.json'
target.parent.mkdir(exist_ok=True)
temporary = target.with_suffix('.json.tmp')
temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
temporary.replace(target)
print(f'Updated {target}: {len(ids)} matching departures.')
