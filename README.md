# ReferralFlow AI

Dental Demand Labs - Duke MENG 570. Three working interactive alternatives around specialist correspondence.

## Open the demos

| Demo | Persona and hypothesis | Published link |
| --- | --- | --- |
| A - Letter Studio | Owner-specialist: source-visible document review | [Open A](https://aaryadeshpande.github.io/referralflow-ai/A.html) |
| B - Referral Brief | Referring general dentist: understand actions, ownership and open items | [Open B](https://aaryadeshpande.github.io/referralflow-ai/B.html) |
| C - Practice Relay | Coordinator: prepare, route, approve and complete a handoff | [Open C](https://aaryadeshpande.github.io/referralflow-ai/C.html) |

[Demo hub](https://aaryadeshpande.github.io/referralflow-ai/) · [Presentation guide](https://aaryadeshpande.github.io/referralflow-ai/guide.html) · [Evidence](https://aaryadeshpande.github.io/referralflow-ai/evidence.html)

## Run locally

Install Node.js 20 or later. No npm packages need installation.

```sh
npm start
```

Open http://127.0.0.1:3000/. The preview also accepts /A, /B and /C. Stop it with Ctrl+C.

You can also open `dist/index.html` directly after downloading and extracting the repository.

## Edit and verify

| File | Purpose |
| --- | --- |
| `dist/A.html` | Letter Studio interface and inline JavaScript |
| `dist/B.html` | Referral Brief interface and inline JavaScript |
| `dist/C.html` | Practice Relay interface and inline JavaScript |
| `dist/site.css` | Shared visual styling; changes can affect every page |
| `dist/index.html` | Navigation hub |
| `dist/guide.html`, `dist/evidence.html` | Assignment, scope, demonstration and evidence material |
| `dist/evaluate.html` | Blank observation record |
| `logs/` | Attributed AI development exchanges |
| `qa/verify.mjs` | Portable state, script and link verification |

Run:

```sh
npm test
```

The checks use Node VM and DOM stubs. They do not verify real browser rendering, customer usability, clinical accuracy or real delivery. `qa/result.json` and `qa/rehearsal.json` are generated records. The scripted walkthroughs do not count as actual team presentation rehearsals.

GitHub Actions checks pushes and pull requests. Updates to `main` also run verification and automatically publish `dist/` to GitHub Pages after checks pass. Each teammate can work on a branch and open a pull request; the intended collaborator role is **Write**, which permits pushes. Aarya owns the repository and manages access.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the collaboration workflow and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for publishing.

## Product boundary

Existing specialist notes → editable draft → specialist reviews, corrects, confirms recipient and approves → approved export through the practice's existing authorized channel.

All cases are fictional. Editing, approval gates, snapshots, revisions and downloads work locally. Draft generation uses deterministic local templates. Roles, identity and delivery are simulated. No live AI, authentication, external sending, patient records or backend is included. Customer value and willingness to pay remain unvalidated.

## Course records

The presentation PDF is `dist/ReferralFlow_Presentation_Guide.pdf`; its generator is `docs/build_presentation_pdf.py` (Python, ReportLab, DejaVu fonts). `python3 build-log.py` rebuilds the development-log HTML/JSON. Preserve attribution: these logs include AI-assistant-to-coding-agent exchanges, not claims of student-typed prompts or customer observations.

The assignment deadline recorded in the supplied materials is October 25, 2026, at 10:59 p.m. Chicago. Confirm current instructions in Canvas. Team review, two actual rehearsals, submission and the class vote are team actions.
