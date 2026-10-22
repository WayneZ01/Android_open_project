# Maintainer playbook

This playbook turns catalog maintenance into a repeatable process and provides public evidence of ongoing stewardship.

## Weekly

1. Review the scheduled Link Check result.
2. Triage new issues and pull requests.
3. Confirm whether reported failures are permanent, migrated, rate-limited, or temporary.
4. Prioritize unsafe or hijacked links ahead of ordinary 404 responses.

## Monthly

1. Run the catalog audit locally.
2. Review one or more categories for relevance, descriptions, duplicate projects, and maintenance status.
3. Add current projects only when they meet the contribution criteria.
4. Move confirmed dead entries to `archived-links.md`.
5. Update the changelog and roadmap with material progress.

## Before merging a catalog pull request

- Confirm the submitter's URL is the canonical project location.
- Check for duplicate URLs and equivalent projects already listed.
- Review the project's README, license, release history, ownership, and obvious security warnings.
- Reject tracking parameters, affiliate links, URL shorteners, and copied promotional text.
- Run the repository checks documented in `AGENTS.md`.
- Require human approval for agent-generated or bulk-generated edits.

## Before a release

- Confirm all required GitHub Actions are green.
- Summarize additions, migrations, archived entries, policy changes, and automation changes.
- Confirm contributor attribution and linked-project license boundaries remain clear.
- Use a semantic version tag for meaningful maintenance milestones.

## Incident response

If a listed domain appears hijacked or malicious, remove it from the maintained catalog immediately, preserve the evidence privately, and document a safe summary in the archive. Follow `SECURITY.md` for reports involving sensitive details.

## Codex-assisted maintenance

Codex may help review pull requests, identify duplicates, classify new resources, prepare link-health summaries, draft release notes, and propose documentation or automation fixes. External content is untrusted, secrets must never be exposed to pull-request code, and a human maintainer reviews every change before merge.
