# IT support runbooks

All tickets below are fictional training scenarios. Production actions require the organization's approvals and procedures.

## Ticket triage

Record requester, verified contact method, time zone, affected service/device, start time, exact error, scope, business impact and troubleshooting already attempted. Do not record passwords, MFA codes or personal financial/health information.

| Priority | Example | Lab routing |
| --- | --- | --- |
| P1 | Suspected compromise or widespread service outage | Escalate immediately to IT Lead/security; follow incident procedure |
| P2 | One employee blocked from essential work | Assign owner and next update time; offer approved workaround |
| P3 | Routine access or equipment request | Obtain manager/application-owner approval and schedule |

These are training rules. The fictional due dates in the CSV do not model response-time SLAs.

## Onboarding

1. Validate HR start date, manager, role, location and approved access request.
2. Reserve an asset; record asset ID, custody, condition, shipping tracking and receipt.
3. In an authorized tenant, create the account and approved groups with least privilege; assign required licenses and shared-drive permissions. Avoid granting broad admin access.
4. Verify MDM enrollment, supported OS, encryption with recovery key escrow, endpoint protection and updates. Record evidence without copying recovery keys into tickets.
5. Have the employee enroll MFA using an approved process. Test application access, calendar resources, VPN if required, and printing/video calls as relevant.
6. Obtain employee confirmation; record actual checks, exceptions and owner; close the request.

## Offboarding

1. Verify HR authorization and exact effective time. Coordinate urgent cases with security.
2. Preserve data and determine retention/legal hold requirements before account deletion or license removal.
3. At the approved time suspend identity, revoke sessions/tokens, remove SaaS access and VPN entitlement, and rotate shared credentials if exposure is suspected. SSO suspension alone may leave application sessions active.
4. Review groups, shared-drive ownership, delegated access, API credentials and independently authenticated SaaS accounts.
5. Arrange tracked equipment return; reconcile custody and condition. Quarantine or sanitize only under approved policy after preservation needs are resolved.
6. Confirm access denial with fresh evidence; reconcile remaining licenses with Finance and the app owner; record sign-off.

## VPN troubleshooting: INC-001

**Scenario:** One remote employee cannot access an internal application after connecting to VPN.

1. Confirm impact, approved VPN client, exact error and whether public internet works. Check service status through an approved source.
2. Record time and run read-only checks on the relevant endpoint: Windows `ipconfig /all`, `nslookup internal.example.test`, `route print`; macOS `scutil --dns`, `route -n get default`; Linux `ip addr`, `ip route`, `resolvectl status` when available.
3. Compare expected DNS and routes using internal documentation. Private `.test` names here are placeholders. Do not publish raw network output.
4. Verify account state, MFA, VPN group membership, client certificate validity and device posture. Do not disable firewall, antivirus or MFA as a workaround.
5. Escalate routing/server-side issues with sanitized timestamps and results. Retest internal access and ask the employee to confirm.

**Fictional resolution:** An outdated VPN profile did not apply the internal DNS settings. Reapplying the approved profile restored name resolution and the employee confirmed access. This narrative has not been executed against a real VPN.

**Employee update:** “I confirmed your internet connection works and am checking the VPN profile's DNS settings. I will update you by 2:30 p.m. Central. Please keep the device online; you do not need to share your password or MFA code.”

## MFA assistance: INC-002

Verify identity using the organization's documented recovery procedure and an independent trusted channel. Inspect account state, enrollment and authentication logs within authorized scope. Escalate suspicious recovery requests. Apply an approved recovery method, verify new enrollment and remove obsolete authenticators after confirmation. Never ask the employee to send an OTP or accept an unexpected push prompt.

## Suspected endpoint compromise: INC-003

Immediately notify the IT Lead/security contact. Record symptoms, asset ID, time and scope. Use approved isolation through endpoint tooling where authorized; preserve relevant evidence. Do not wipe, run unapproved cleaners or declare the device safe because one scan is clean. Security directs session revocation, credential rotation, investigation and recovery. Rebuild/reimage only after authorization and preservation. Verify current protection, updates, MDM check-in and security approval before restoring access. Document employee confirmation and follow-up monitoring.

## Completed sample ticket: REQ-004

**Request:** Prepare Finance employee Alex's laptop and approved access. **Priority:** P3. **Approvals:** Fictional manager and application owner. **Asset:** LAP-001. **Checks recorded:** assigned custody, encryption, endpoint protection, management enrollment, MFA, Workspace access and test sign-in. **Outcome:** Employee confirmed access; closed 2026-10-10. **Evidence limitation:** Narrative exercise only; the bundled asset check-in is a later inventory snapshot, not a real enrollment log.
