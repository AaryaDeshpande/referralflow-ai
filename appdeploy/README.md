# Hosted voice application

This directory preserves the source of the deployed ReferralFlow voice app,
recovered from `ReferralFlow_Source_Backup.zip` in the supplied submission package.
AppDeploy app: `referralflow-ai-voice-and-three-prototypes-zstv8f`.
Deployed source version: `1792969136135`.

[Open the live app](https://referralflow-ai-voice-and-three-prototypes-zstv8f.v2.appdeploy.ai/).
The backend, voice script and Letter Studio HTML were also compared with that
stored AppDeploy version during this import. `source-manifest.json` records
SHA-256 hashes of all 25 recovered application files. `RECOVERY_NOTE.txt` retains
the original recovery note; its statement that GitHub was not updated is historical.

## Runtime

- `index.html` is Prototype A, including the original approval/export controls.
- `public/voice.js` handles permission, browser recording, playback, sample loading,
  corrected transcripts and applying fields to the letter.
- `src/main.ts` connects the page to `/api/voice/analyze` and `/api/voice/extract`.
- `backend/index.ts` transcribes audio and extracts quoted fields using AI. It
  rejects requests without permission and leaves unmatched facts for review.
- `public/B.html` and `public/C.html` retain the recipient and coordinator workflows.
- `public/resources/fictional-visit.mp3` is the supplied synthetic fictional visit.

AppDeploy injects `@appdeploy/client` and `@appdeploy/sdk` into its runtime. The
recovered package manifest relies on that host behavior; `npm install` alone is
not a standalone backend setup. GitHub Pages cannot run these TypeScript API
handlers. No secret keys are included or required in the static preview.

## Pages preview

From the repository root, run `npm run sync:pages` after editing this source,
then `npm test`. The sync copies public assets, maps the hosted root to `dist/A.html`,
and keeps the Pages root as the overview. It replaces the host SDK entry point
with a visible link to the hosted AI workspace. Live-AI controls are hidden on
Pages; the labelled prepared example, microphone capture, notes, review and
approved exports remain available locally. A new recording is not transferred
when opening the hosted workspace.

Edit the hosted source here; edit Pages-specific adaptation in
`scripts/sync-appdeploy.mjs`. Pushing to GitHub updates Pages but does not deploy
the backend to AppDeploy. Deploying future backend changes is a separate action.

`tests/tests.json` contains recovered manual test descriptions. The root
`npm test` runs executable VM/DOM-stub checks, including voice integration,
approval invalidation, error recovery and local links. Neither is a hardware
microphone check, clinical validation or team rehearsal. Use fictional data only.
