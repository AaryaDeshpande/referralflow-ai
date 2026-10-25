# Website publishing

The team website is https://aaryadeshpande.github.io/referralflow-ai/.

## Update the website

1. Edit the source in `appdeploy/` or the Pages adaptation in `scripts/sync-appdeploy.mjs`, then run `npm run sync:pages`.
2. Run `npm test` and try the affected flow locally with `npm start`.
3. Push the changes to `main`, or merge a reviewed pull request into `main`.
4. GitHub Actions runs verification, then publishes `dist/` through the **Check prototypes** (verify, then deploy) workflow. The public link stays the same.

A failed verification prevents that workflow from publishing. Check the Actions tab for the outcome. Branches and open pull requests do not publish changes to the public site. You can also start the publishing workflow manually from Actions.

Only `dist/` is published. The repository stays private; the website is public. The complete voice app source lives in `appdeploy/`. Its AI backend runs on AppDeploy, where the platform supplies the SDK and AI service. Pushing this repository does not redeploy that backend. The Pages hub links to the live AI workspace, and `A.html` offers the prepared fictional example and local notes flow. No API keys are embedded in the site.

Live voice: https://referralflow-ai-voice-and-three-prototypes-zstv8f.v2.appdeploy.ai/. Open this workspace before recording a visit for AI processing; recordings made on the Pages preview are not transferred between sites.

## Presentation PDF

If editing the presentation source, regenerate `dist/ReferralFlow_Presentation_Guide.pdf` using `python3 docs/build_presentation_pdf.py`, then commit the generated PDF. The deployment workflow publishes committed static files without regenerating the PDF.

## Before class

Open the published hub, all three prototypes, the guide and downloads on desktop and a phone. Complete the two team rehearsals and submit the materials required by Canvas.
