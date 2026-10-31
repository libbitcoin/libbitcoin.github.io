# Security

## 1. Reporting

Report a vulnerability privately on GitHub. Open the Security tab of the
affected repository and select **Report a vulnerability**:

- [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server/security/advisories/new)
- [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer/security/advisories/new)
- [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node/security/advisories/new)
- [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network/security/advisories/new)
- [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database/security/advisories/new)
- [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system/security/advisories/new)
- [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build/security/advisories/new)

If you are not sure which library is affected, report it to
libbitcoin-build. The report is visible only to you and the
maintainers.

Follow responsible (coordinated) disclosure, as described in the
[OWASP Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html):
do not disclose a vulnerability in a public issue, pull request, chat or
mailing list before its advisory is published.

## 2. What to include

- The affected component, and its version or commit.
- The platform and build options.
- Steps to reproduce, or a proof of concept.
- The impact as you understand it.
- Any date by which you intend to disclose.

## 3. Email option

If you cannot use GitHub, email `mienkphi@gmail.com`. Encrypt the report
to every key listed in this section, so that each maintainer can read it.

<div class="banner"><strong>Maintainer GPG keys will be published before the first version 4 release.</strong> Until then, use email only to arrange contact, and send no details of the vulnerability by email.</div>

## 4. Handling

A maintainer acknowledges the report, confirms the issue and its
severity, and works with you on a fix in a private advisory. The
advisory is published once a release containing the fix is available,
on a date agreed with you. Reporters are credited in the advisory unless
they ask not to be.

## 5. Versions

Fixes are made to version 4 and its successors. Earlier versions are no
longer maintained.

## 6. Not security

Bugs without a security impact, build problems and support questions
belong in the public issues of the affected repository.
If you are not certain that a bug has no security impact, report it
privately as a vulnerability.
