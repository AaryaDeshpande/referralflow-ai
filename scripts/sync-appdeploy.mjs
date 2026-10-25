import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'appdeploy');
const dist = path.join(root, 'dist');
const live = 'https://referralflow-ai-voice-and-three-prototypes-zstv8f.v2.appdeploy.ai/';

// GitHub Pages serves static files. Keep the hosted source intact and produce
// an explicit local example plus a link to the live AI service.
fs.cpSync(path.join(source, 'public'), dist, { recursive: true });
let letter = fs.readFileSync(path.join(source, 'index.html'), 'utf8');
letter = letter.replace('    <script type="module" src="./src/main.ts"></script>\n', '');
letter = letter.replace(
  '<section class="visit-voice" aria-labelledby="voice-heading">',
  `<section class="visit-voice" aria-labelledby="voice-heading">
          <div class="pages-voice-notice" role="note">
            <strong>Try the live AI voice workflow</strong>
            <p>Open the hosted workspace to turn a new recording or edited transcript into a report.
            This preview lets you play the fictional visit and review its prepared example letter.
            New recordings stay on this page and are not transferred when you open the hosted workspace.</p>
            <a href="${live}">Open live AI voice workspace →</a>
          </div>`
);
letter = letter.replace('id="voice-process" disabled', 'id="voice-process" hidden disabled');
letter = letter.replace('id="voice-extract" disabled', 'id="voice-extract" hidden disabled');
letter = letter.replace('Fictional demo · AI voice + local notes', 'Fictional demo · prepared voice example + local notes');
letter = letter.replace(
  'Voice capture uses AI transcription and field extraction.',
  'The hosted workspace uses AI transcription and field extraction. This static preview uses the prepared fictional example.'
);
fs.writeFileSync(path.join(dist, 'A.html'), letter);
fs.appendFileSync(path.join(dist, 'voice.css'), `
/* Pages preview: AI processing runs in the linked hosted workspace. */
#voice-process[hidden], #voice-extract[hidden] { display: none !important; }
.pages-voice-notice { padding: 16px; margin-bottom: 20px; border: 1px solid #b9c9ed; border-radius: 8px; background: #edf3ff; }
.pages-voice-notice p { margin: 8px 0; }
.pages-voice-notice a { font-weight: 650; }
`);

let overview = fs.readFileSync(path.join(source, 'public/overview.html'), 'utf8');
overview = overview.replace(
  '<a class="open" href="A.html">Open Letter Studio →</a>',
  `<a class="open" href="${live}">Open Letter Studio + live voice →</a>
            <a href="A.html" style="margin-top:12px">Try the prepared voice example here →</a>`
);
overview = overview.replace(
  'Record a fictional visit, prepare draft fields with AI, and review',
  'Open the hosted voice workspace, record a fictional visit, prepare draft fields with AI, and review'
);
fs.writeFileSync(path.join(dist, 'overview.html'), overview);
fs.writeFileSync(path.join(dist, 'index.html'), overview);

const guidePath = path.join(dist, 'guide.html');
let guide = fs.readFileSync(guidePath, 'utf8');
guide = guide.replace(
  '<h1>',
  `<div class="notice"><strong>Live AI voice:</strong> <a href="${live}">Open the hosted Letter Studio</a> for recording transcription and edited-transcript processing.
  The GitHub Pages A preview uses the labelled prepared example. B and C remain local interaction prototypes.</div><h1>`
);
fs.writeFileSync(guidePath, guide);
console.log('Updated Pages preview from appdeploy/; live AI remains on AppDeploy.');
