# Review checklist and evidence map

This is an audit-support practice exercise, not a certification or comprehensive mapping to any compliance framework.

| Review area | Sample evidence | Reviewer question | Limitation |
| --- | --- | --- | --- |
| Access lifecycle | users.csv + findings | Are departed accounts disabled and app sessions revoked? | CSV cannot prove live revocation |
| MFA | users.csv | Are required accounts enrolled and policy enforced? | Enrollment does not prove effective policy |
| Least privilege | Admin review findings | Has the owner approved each privileged assignment? | IT department is only a lab heuristic |
| Endpoint posture | assets.csv | Are encryption, protection and MDM verified with fresh telemetry? | Reported flags may be stale or incorrect |
| Asset custody | Owner/status records | Is equipment assigned, returned and sanitized correctly? | Shipping and sanitization evidence not modeled |
| License governance | licenses.csv | Can seats be removed without breaking retention or contracts? | Potential savings are not realized savings |
| Ticket management | tickets.csv + runbooks | Are priorities, owners and follow-ups documented? | Date policy is simpler than a real SLA |
| Evidence integrity | manifest.json | Have exported files changed since hashing? | Manifest is unsigned and can be replaced |

For a real review, record source system, collector, scope, collection time, report date, approver, exceptions, evidence location and retention period. Restrict access and redact sensitive records. Have the security/compliance owner determine applicable controls for SOC 2, HIPAA or PCI DSS.

## Closing a finding

Record finding ID/subject, validated issue, approving owner, authorized action, actual completion timestamp, fresh verification, employee impact and reviewer sign-off. Do not close a finding merely because a row disappeared from an export.
