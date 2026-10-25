# ReferralFlow AI

Dental Demand Labs - Duke MENG 570. Three working interactive alternatives around specialist correspondence, now including voice capture and AI report preparation in Prototype A.

[Open the live voice app](https://referralflow-ai-voice-and-three-prototypes-zstv8f.v2.appdeploy.ai/) · [Hosted frontend and backend source](appdeploy/)

## Open the demos

| Demo | Persona and hypothesis | Published link |
| --- | --- | --- |
| A - Letter Studio | Owner-specialist: recorded visit → transcript and quoted fields → reviewed letter | [Live AI voice](https://referralflow-ai-voice-and-three-prototypes-zstv8f.v2.appdeploy.ai/) · [Pages example](https://aaryadeshpande.github.io/referralflow-ai/A.html) |
| B - Referral Brief | Referring general dentist: understand actions, ownership and open items | [Open B](https://aaryadeshpande.github.io/referralflow-ai/B.html) |
| C - Practice Relay | Coordinator: prepare, route, approve and complete a handoff | [Open C](https://aaryadeshpande.github.io/referralflow-ai/C.html) |

[Demo hub](https://aaryadeshpande.github.io/referralflow-ai/) · [Presentation guide](https://aaryadeshpande.github.io/referralflow-ai/guide.html) · [Evidence](https://aaryadeshpande.github.io/referralflow-ai/evidence.html)

## Run locally

Install Node.js 20 or later. No npm packages need installation.

```sh
npm start
```

Open http://127.0.0.1:3000/. The preview also accepts /A, /B and /C. Stop it with Ctrl+C.

Use the local HTTP preview for the voice example; loading sample audio requires HTTP or HTTPS. Live AI processing runs in the linked AppDeploy workspace.

## Edit and verify

| File | Purpose |
| --- | --- |
| `appdeploy/` | Complete recovered hosted voice frontend, backend and assets |
| `scripts/sync-appdeploy.mjs` | Rebuild the static Pages preview from hosted source |
| `dist/A.html` | Letter Studio with the prepared voice example and live AI link |
| `dist/B.html` | Referral Brief interface and inline JavaScript |
| `dist/C.html` | Practice Relay interface and inline JavaScript |
| `dist/site.css` | Shared visual styling; changes can affect every page |
| `dist/nav.css` | Shared left icon rail and footer link styling used by every page |
| `dist/index.html` | Navigation hub |
| `dist/guide.html`, `dist/evidence.html` | Assignment, scope, demonstration and evidence material |
| `dist/evaluate.html` | Blank observation record |
| `logs/` | Attributed AI development exchanges |
| `qa/verify.mjs` | Portable state, script and link verification |

After editing `appdeploy/`, regenerate the Pages preview and verify:

```sh
npm run sync:pages
npm test
```

The checks use Node VM and DOM stubs. They do not verify real browser rendering, customer usability, clinical accuracy or real delivery. `qa/result.json` and `qa/rehearsal.json` are generated records. The scripted walkthroughs do not count as actual team presentation rehearsals.

GitHub Actions checks pushes and pull requests. Updates to `main` also run verification and automatically publish `dist/` to GitHub Pages after checks pass. Each teammate can work on a branch and open a pull request; the intended collaborator role is **Write**, which permits pushes. Aarya owns the repository and manages access.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the collaboration workflow and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for publishing.

## Product boundary

Permission → fictional visit recording → AI transcript and quoted report fields → editable draft → specialist reviews, corrects, confirms recipient and approves → approved export through the practice's existing authorized channel. Existing labelled notes remain another input. Voice is implemented in A; B and C focus on recipient understanding and coordinator handoff.

All cases are fictional. The hosted app includes real AI audio transcription and transcript extraction. GitHub Pages provides a clearly labelled fixed voice example and local notes drafting; its main A link opens the hosted AI workspace. Editing, approval gates, snapshots, revisions and downloads work locally. Roles, identity and delivery remain simulated. No production authentication, clinical validation, real patient records or external sending is provided. Customer value and willingness to pay remain unvalidated.

## Course records

The retained earlier notes-based presentation PDF is `dist/ReferralFlow_Presentation_Guide.pdf`; its generator is `docs/build_presentation_pdf.py` (Python, ReportLab, DejaVu fonts). The voice source includes the preserved development-log HTML/JSON. `python3 build-log.py` rebuilds the earlier log view from `logs/`; preserve current voice navigation when changing the log. Preserve attribution: these logs include AI-assistant-to-coding-agent exchanges, not claims of student-typed prompts or customer observations.

The assignment deadline recorded in the supplied materials is October 25, 2026, at 10:59 p.m. Chicago. Confirm current instructions in Canvas. Team review, two actual rehearsals, submission and the class vote are team actions.
