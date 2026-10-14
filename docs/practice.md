# Make this project your own

Complete these exercises before claiming the project on your resume. Keep your explanation in your own words.

## Session 1: Run and understand

Run `python lab.py`, open the HTML report and identify the critical finding. Explain why a departed employee with an active account is higher priority than an unused license. Read each CSV and trace three findings back to their exact input fields. Run the tests.

## Session 2: Resolve simulated findings

Copy `data/` to `work/remediated/`. Modify only the copy: mark Casey's account suspended, mark Casey's three licenses unassigned, change LAP-003 to returned, enable Blair's MFA and LAP-002 encryption, and change Ellis's role to user. Mark INC-001 and INC-003 closed. These edits represent hypothetical approved remediations; they do not administer actual services.

```sh
python lab.py --data work/remediated --out work/after --as-of 2026-10-14
```

Expected result: zero findings and $0 potential reclaimable seats. Explain that $0 here means no remaining seat candidates; actual savings would require billing confirmation. Compare before/after reports. Document which authorizations and evidence real remediation would require.

## Session 3: Troubleshoot and write

Follow the VPN runbook on a device you own using only applicable read-only commands. Private internal hostnames will not resolve without a real lab network. Capture sanitized observations locally. Write one ticket with symptoms, hypothesis, tests, results, escalation criteria and employee update. Do not invent a successful VPN repair if you did not perform one.

## Session 4: Close the real-platform gap

If you have an authorized Workspace or MDM training tenant, practice with dedicated test accounts and devices: approved account provisioning, group assignment, MFA enrollment and revocation; endpoint enrollment and policy verification. Record sanitized screenshots with dates and notes. Tenant availability and cost vary; verify before purchasing. Without a tenant, describe these as documented workflows, not hands-on administration. No paid tenant is required to run this repository.

## Five-minute interview demonstration

1. Explain the fictional business and why IT needs one accurate access/asset review.
2. Run the analyzer and show Casey's active account plus three SaaS seats.
3. Explain the sequence: HR authorization, preservation, suspension/session revocation, independent app access, asset return and license review.
4. Show endpoint gaps and distinguish missing inventory evidence from verified insecure configuration.
5. Show the before/after exercise, test results and a ticket update. State the simulation boundary clearly.

Questions to prepare: Why not delete the account immediately? Why does MFA not solve excessive privilege? Why might SSO revocation leave app sessions? What does a SHA-256 manifest prove? When should you escalate rather than continue troubleshooting?
