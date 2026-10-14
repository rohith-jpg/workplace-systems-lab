"""Offline workplace systems evidence lab. Python standard library only."""
import argparse
import csv
import hashlib
import html
import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(folder, name):
    with (folder / (name + '.csv')).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def analyze(folder, as_of):
    users = load(folder, 'users')
    assets = load(folder, 'assets')
    seats = load(folder, 'licenses')
    tickets = load(folder, 'tickets')
    identities = {u['email']: u for u in users}
    findings = []

    def flag(severity, control, subject, detail, action):
        findings.append(dict(severity=severity, control=control, subject=subject,
                             detail=detail, action=action))

    for u in users:
        if u['employment_status'] == 'departed' and u['account_status'] == 'active':
            flag('critical', 'Access review', u['email'], 'Departed employee has active account',
                 'Verify HR authorization; suspend account, revoke sessions and SaaS access; preserve data per policy.')
        if u['account_status'] == 'active' and u['mfa'] != 'enabled':
            flag('high', 'MFA', u['email'], 'Active account lacks MFA',
                 'Verify identity and enroll MFA; never request passwords or verification codes.')
        if u['role'] == 'admin' and u['department'] != 'IT':
            flag('high', 'Least privilege', u['email'], 'Non-IT administrator requires review',
                 'Ask application owner to confirm documented business need; remove only after approval.')
    for a in assets:
        if a['status'] != 'assigned':
            continue
        owner = identities.get(a['owner'])
        if owner is None or owner['employment_status'] != 'active':
            flag('high', 'Asset lifecycle', a['asset_id'], 'Assigned to unknown or departed employee',
                 'Confirm custody and arrange tracked return; record receipt and approved sanitization.')
        for field, label in [('encrypted', 'Disk encryption'), ('antivirus', 'Antivirus'), ('mdm', 'MDM enrollment')]:
            if a[field] != 'yes':
                flag('high', 'Endpoint posture', a['asset_id'], label + ' missing or unverified',
                     'Validate in endpoint console; remediate through approved policy and collect fresh evidence.')
        age = (as_of - date.fromisoformat(a['last_checkin'])).days
        if age > 14:
            flag('medium', 'Endpoint visibility', a['asset_id'], f'Last check-in {age} days ago',
                 'Contact owner; confirm connectivity and management agent health.')
        elif age < 0:
            flag('medium', 'Data quality', a['asset_id'], 'Check-in is after report date',
                 'Correct export timestamp before relying on endpoint evidence.')
    reclaimable = 0
    for seat in seats:
        owner = identities.get(seat['email'])
        if seat['assigned'] == 'yes' and (owner is None or owner['employment_status'] != 'active'):
            cents = round(float(seat['monthly_cost_usd']) * 100)
            reclaimable += cents
            flag('medium', 'SaaS license review', seat['email'] + ' / ' + seat['app'],
                 f'Potential reclaimable seat: ${cents / 100:.2f}/month',
                 'Confirm retention, ownership transfer and contract terms before removing seat.')
    for ticket in tickets:
        if ticket['status'] != 'closed' and date.fromisoformat(ticket['due_date']) < as_of:
            flag('high' if ticket['priority'] == 'P1' else 'medium', 'Ticket queue', ticket['ticket_id'],
                 'Open ticket past due date', 'Update employee, document next action and escalate to IT Lead.')
    findings.sort(key=lambda f: {'critical': 0, 'high': 1, 'medium': 2}[f['severity']])
    return dict(as_of=as_of.isoformat(), simulated=True, users=len(users), assets=len(assets),
                tickets=len(tickets), potential_monthly_savings_usd=reclaimable / 100,
                findings=findings)


def export(result, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'report.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    fields = ['severity', 'control', 'subject', 'detail', 'action']
    with (folder / 'findings.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for finding in result['findings']:
            # Protect spreadsheet consumers from formula interpretation.
            writer.writerow({k: "'" + v if v.startswith(('=', '+', '-', '@', '\t', '\r', '\n')) else v
                             for k, v in finding.items()})
    rows = ''.join('<tr data-severity="' + html.escape(f['severity'], quote=True) + '">' + ''.join('<td>' + html.escape(str(f[k])) + '</td>' for k in fields) + '</tr>'
                   for f in result['findings'])
    page = (ROOT / 'report-template.html').read_text(encoding='utf-8')
    counts = {level: sum(f['severity'] == level for f in result['findings'])
              for level in ('critical', 'high', 'medium')}
    replacements = {'ASOF': result['as_of'], 'USERS': result['users'], 'ASSETS': result['assets'],
                    'COUNT': len(result['findings']), 'SAVINGS': f"{result['potential_monthly_savings_usd']:.2f}"}
    for level, count in counts.items():
        replacements[level.upper() + '_WIDTH'] = f"{100 * count / max(1, len(result['findings'])):.3f}"
        replacements[level.upper()] = count
    for key in sorted(replacements, key=len, reverse=True):
        page = page.replace(key, html.escape(str(replacements[key])))
    page = page.replace('ROWS', rows)
    (folder / 'report.html').write_text(page, encoding='utf-8', newline='\n')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(folder.iterdir()) if p.name in ('report.json', 'findings.csv', 'report.html')}
    (folder / 'manifest.json').write_text(json.dumps({'generated_at': datetime.now(timezone.utc).isoformat(),
                                                   'sha256': manifest}, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'data')
    parser.add_argument('--out', type=Path, default=ROOT / 'evidence')
    parser.add_argument('--as-of', type=date.fromisoformat, default=date(2026, 10, 14))
    args = parser.parse_args()
    try:
        result = analyze(args.data, args.as_of)
        export(result, args.out)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'Input/report error: {exc}\n')
    print(f"{len(result['findings'])} findings; ${result['potential_monthly_savings_usd']:.2f}/month potential savings")
    print(args.out / 'report.html')


if __name__ == '__main__':
    main()
