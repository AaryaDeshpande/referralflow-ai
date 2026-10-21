# Source collaboration and deployment

The current public site is https://referralflow-class-lab.ad277.chatgpt.site/.

This team copy is based on published Site version 2, source commit `87f840f87e4ee2e68db165d2552479d4b32be142`, retrieved on October 20, 2026 (Chicago). App source and supporting course files are copied without changing the published application. The repository adds team instructions, a local development server and GitHub Actions checks.

## What a GitHub push does

A push saves the source for the team and triggers the included verification workflow. It does **not** automatically update the current hosted Site. There is no GitHub-to-Sites deployment automation in this repository.

## Publish an update

For the existing Site, Aarya can request publication of the selected GitHub commit through ChatGPT Sites. The publishing workflow must fetch that commit, validate the static `dist/` output, and publish through the original Site project. Keep the same live Site when continuing this project.

Alternatively, the team can later choose another static host and deploy the `dist/` directory. The app needs static-file hosting only. It currently has no server, database or cloud credentials to provision.

The Site-specific hosting manifest is intentionally excluded from this portable team copy. No credential, token or account session is included. The original source checkout keeps its Site identity separately.

## Checks before class

1. Open the actual published links without signing in and verify A/B/C load.
2. Run the intended demo paths on desktop and a phone.
3. Test approval, revision, missing information and downloads.
4. Complete two actual team presentation rehearsals.
5. Submit the verified links, presentation and prompt record required by Canvas.
