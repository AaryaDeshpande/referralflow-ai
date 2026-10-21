from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'/'ReferralFlow_Presentation_Guide.pdf'
BASE='https://aaryadeshpande.github.io/referralflow-ai'
FONT='/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DejaVu',FONT+'/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold',FONT+'/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold')
INK=colors.HexColor('#15243d'); BLUE=colors.HexColor('#345cda'); MUTED=colors.HexColor('#5d6b80'); LINE=colors.HexColor('#dce3ee'); PALE=colors.HexColor('#edf2ff')
S={
 'title':ParagraphStyle('title',fontName='DejaVuBold',fontSize=28,leading=33,textColor=INK,spaceAfter=16),
 'h1':ParagraphStyle('h1',fontName='DejaVuBold',fontSize=23,leading=28,textColor=INK,spaceAfter=13),
 'h2':ParagraphStyle('h2',fontName='DejaVuBold',fontSize=12,leading=16,textColor=INK,spaceBefore=13,spaceAfter=7),
 'p':ParagraphStyle('p',fontName='DejaVu',fontSize=9.5,leading=14.3,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8,leading=11.8,textColor=MUTED,spaceAfter=7),
 'eyebrow':ParagraphStyle('eyebrow',fontName='DejaVuBold',fontSize=8,leading=12,textColor=BLUE,spaceAfter=11),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=8.5,leading=12.5,textColor=INK,spaceAfter=0),
 'head':ParagraphStyle('head',fontName='DejaVuBold',fontSize=8,leading=12,textColor=INK,spaceAfter=0),
 'callout':ParagraphStyle('callout',fontName='DejaVu',fontSize=10,leading=15.4,textColor=INK,spaceAfter=0),
}

def P(t,style='p'):
 t=re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)','&amp;',t)
 return Paragraph(t,S[style])
def link(label,path):
 u=path if path.startswith('https://') else BASE+'/'+path
 return f'<link href="{u}" color="#345cda"><u>{label}</u></link>'
def tab(headers,rows,widths):
 t=Table([[P(c,'head') for c in headers]]+[[P(c,'cell') for c in row] for row in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,0),.7,LINE),('LINEBELOW',(0,1),(-1,-1),.45,LINE)]))
 return t

def box(t):
 b=Table([[P(t,'callout')]],colWidths=[524],hAlign='LEFT');b.spaceAfter=10;b.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]));return b

def page(kicker,title):
 if story:story.append(PageBreak())
 story.extend([P(kicker.upper(),'eyebrow'),P(title,'h1')])
def paras(*texts):story.extend(P(x) for x in texts)
def steps(items):
 for i,t in enumerate(items,1):story.append(P(f'<b>{i}.</b> {t}'))

story=[]
page('Dental Demand Labs · MENG 570 · 20 October 2026','ReferralFlow<br/>Three hypotheses. One direction.')
story.append(P('Presentation document · Working prototypes · Evidence and test plan','small'))
story.append(box('<b>Decision:</b> continue the committed notes → editable report → specialist approval → approved handoff direction. Use the three versions to choose how this workflow should work. Commercial profitability remains unverified.'))
story.append(Spacer(1,18))
story.append(tab(['VERSION / PERSONA','HYPOTHESIS','OPEN'],[
 ('<b>A · Letter Studio</b><br/>Specialist','Source beside the letter supports effective review and completion.',link('Prototype A','A.html')),
 ('<b>B · Referral Brief</b><br/>Referring dentist','An action-focused approved brief supports correct recipient understanding.',link('Prototype B','B.html')),
 ('<b>C · Practice Relay</b><br/>Coordinator','Visible states and ownership support reliable completion of a team handoff.',link('Prototype C','C.html')),
], [148,288,88]))
story.append(P('Ready-to-share materials','h2'))
paras(link('Prototype hub','index.html')+' · '+link('Detailed presentation guide','guide.html')+' · '+link('Evidence map','evidence.html'),link('Actual prompt history','development-log.html')+' · '+link('Download prompt JSON','development-log.json')+' · '+link('Blank observation and vote record','evaluate.html'))
story.append(P('Assignment deadline','h2'))
paras('<b>Sunday, October 25, 2026, 10:59 p.m. Chicago time</b>, as shown in the supplied screenshot. Submit the three links and presentation document to Canvas before presenting. No submission has been made by the assistant.')
story.append(P('Working scope','h2'))
paras('All three use fictional Alex Morgan / RF-1042 case data. They are functioning interface experiments with editable state and real exports. Drafting, roles and delivery are locally simulated. No real patient records, live AI model, real messages or payments are involved.')
story.append(P('Human review still required: confirm the earlier persona mapping, open the public links on a separate device, and complete two actual team rehearsals. Scripted technical walkthroughs do not satisfy the team rehearsal requirement.','small'))

page('Opening · up to 2 minutes','The problem stays fixed.')
story.append(box('Specialists need to return an accurate, useful report to the dentist who referred the patient. ReferralFlow starts with notes the specialist already has and supports the work needed to produce a reviewed, approved copy.'))
story.append(P('What we knew, and what we know now','h2'))
paras('The uploaded prototype describes an earlier specialist interview about correspondence effort and fragmented information. The original transcript and original persona sheets were unavailable in this audit. Its task description is the starting point, with limited independent verification.','Current vendor evidence shows that notes-to-letter drafting and report queues already exist. The product question is whether a specific review, comprehension or coordination approach improves the practice’s actual workflow.','No measured report volume, total time saved, buyer price acceptance, customer retention or profit is established by these prototypes.')
story.append(tab(['WORKING PERSONA','JOB / EVIDENCE LIMIT'],[
 ('<b>Dr. Arjun Patel</b><br/>Owner-periodontist','Prepare and approve correspondence. Fictional name retained from the backup; task linked to its account of specialist discovery.'),
 ('<b>Dr. Elena Ruiz</b><br/>Referring general dentist','Understand the update and next action. Fictional working persona; specific needs require recipient testing.'),
 ('<b>Maya Chen</b><br/>Coordinator / clinical assistant','Prepare, route and complete work. Fictional working persona; actual ownership needs observation.'),
],[165,359]))
story.append(P('Persona and comparison integrity','h2'))
paras('Confirm these roles against the team’s earlier persona submission. If those sheets differ, update the presentation explanation. The assignment allows variants by functionality. Do not claim that fictional names or assumed responsibilities came from verified interviews.','All versions share Alex Morgan’s case, recipient and source statements. This reduces content differences. Repeating the case creates learning effects, so rotate test order and record it.')

page('Evidence → design choices','Four books, with clear limits.')
story.append(tab(['SOURCE / EXACT LOCATION','APPLICATION IN THIS BUILD'],[
 ('<b>Running Lean, 3rd ed.</b><br/>Printed pp. 145–147, 203–204, 231, 236.<br/>PDF pp. 191–193, 249–250, 277, 282.','Define observable tasks and disconfirming results in advance. Compare with the existing process. Deliver a small useful solution and test a stated price with the buyer. Practitioner guidance; no guaranteed conversion rate.'),
 ('<b>$100M Offers</b><br/>PDF pp. 52, 81.','Qualify pain, purchasing power and access. Measure total customer effort, including review, reformatting and handoff. Keep an existing-channel export path. The value framework is conceptual.'),
 ('<b>The Everywhere Millionaire</b><br/>PDF pp. 108, 125.','Separate revenue, profit and founder income. Count setup and support labor and examine dependence on the founder. Population evidence does not predict this venture’s outcome.'),
 ('<b>Think and Grow Rich</b><br/>PDF p. 125.','Turn plans into working experiments, seek relevant expertise, rehearse and revise after observation. Motivational guidance does not establish product demand.'),
],[190,334]))
story.append(P('Current primary market evidence','h2'))
paras('<b>ToothNote</b> describes notes-to-referral-letter drafting and publishes a named periodontics testimonial. Its listed Solo price is <b>US$79/doctor/month, billed annually</b>, including referral letters. Listed price and vendor testimonials do not establish actual revenue, profit or broad adoption. [S1–S2]','<b>DentalEMR and TDO</b> document related letter and report-management functionality. Test against what a practice already owns and uses. A queue or generated letter alone is insufficient evidence of differentiation. [S3–S4]','<b>AAE’s 2026 endodontic referral survey</b> supports testing timely, useful return communication. Its 919 responses and 7.7% / 8.1% group response rates limit generalization. It does not establish willingness to buy ReferralFlow. [S5]')
story.append(P('Book references use the supplied editions. Primary-source links and survey locations appear on page 10 and the online evidence page.','small'))

page('Version A · specialist · about 2 minutes','Letter Studio')
story.append(P('Hypothesis','h2'))
story.append(box('Keeping the source near an editable letter lets a specialist find, correct and approve the report without a guided tour.'))
story.append(tab(['FEATURE SCOPE CARD','DECISION'],[
 ('Value','Finish the specialist’s actual correspondence task.'),
 ('Included','Source note, editable draft, source-selection buttons, recipient/review checks, explicit unresolved information, approved TXT and HTML export.'),
 ('Effort / complexity','Medium prototype effort. Production complexity depends on notes, review burden and integration. These are design estimates.'),
 ('Success signal','Independent task completion; missing facts preserved; correct recipient and approved version exported.'),
 ('Disconfirming observation','Lost source context, unsupported content, repeated help, or more total effort than the current template.'),
], [145,379]))
story.append(P('Live demo · about 2 minutes','h2'))
steps(['Load Alex Morgan and generate the local draft.','Use an Assessment, Treatment or Follow-up source button. Compare the statement and make a wording edit.','Confirm clinical review, recipient and the recorded missing radiograph.','Approve and download the HTML or TXT report.','Edit again to show that approval is cleared and a new review is required.'])
paras('<b>Optional exception:</b> load Sofia Bennett’s incomplete note. The missing follow-up remains explicit and must be acknowledged.','<b>Tradeoff:</b> flexible document editing still requires whole-report review. It offers little help when the main bottleneck occurs after approval.')
story.append(P(link('Open Letter Studio','A.html')+' · Observe source checks, corrections, help requests and active time.','small'))

page('Version B · referring dentist · about 2 minutes','Referral Brief')
story.append(P('Hypothesis','h2'))
story.append(box('A concise approved brief, with the full report available, helps the referring dentist correctly identify the action, its owner and remaining uncertainty.'))
story.append(tab(['FEATURE SCOPE CARD','DECISION'],[
 ('Value','Make the returned report useful at the receiving practice.'),
 ('Included','Structured review, approved action cards, full report, seeded approved sample, local comprehension record and approved TXT export.'),
 ('Effort / complexity','Medium prototype effort. The brief must remain consistent with the approved full report.'),
 ('Success signal','Recipient identifies the requested action, responsible office and timing without coaching.'),
 ('Disconfirming observation','Missing context, unsupported action, wrong owner, or no comprehension benefit over the existing letter.'),
], [145,379]))
story.append(P('Live demo · about 2 minutes','h2'))
steps(['Choose Open approved sample. Its approval and handoff are explicitly fictional.','As Dr. Ruiz, identify the next action and responsible office.','State the timing and what is still missing. Open the full report.','Download the approved report.','If time permits: Specialist review → Create a revision → edit → confirm both checks → Approve this version → Simulate practice handoff.'])
paras('<b>Expected understanding:</b> Cedar Grove Dental supplies the prior radiograph before the follow-up; specialist review is in six weeks; no calendar appointment was supplied.','<b>Tradeoff:</b> structured review can add preparation work. The previous delivered version remains visible during revision; only an explicit new approved handoff replaces it.')
story.append(P(link('Open Referral Brief','B.html')+' · Capture the recipient’s answer in their own words.','small'))

page('Version C · coordinator · about 2 minutes','Practice Relay')
story.append(P('Hypothesis','h2'))
story.append(box('Visible work states and a named next owner help staff complete a case through specialist review while keeping missing-source work blocked.'))
story.append(tab(['FEATURE SCOPE CARD','DECISION'],[
 ('Value','Make preparation, review and completion ownership visible.'),
 ('Included','Work queue, preparation checks, saved edits, specialist approval, current recipient confirmation, frozen export, local completion and separate completed section.'),
 ('Effort / complexity','Higher coordination complexity. Production permissions and delivery are future work; current role selection is simulated.'),
 ('Success signal','Ready case completes correctly; specialist retains approval; missing-note case stays blocked.'),
 ('Disconfirming observation','Misrouting, lost work, confusion between export and delivery, or excessive handoff overhead.'),
], [145,379]))
story.append(P('Live demo · about 2 minutes','h2'))
steps(['As coordinator, select Alex Morgan and check the source and recipient.','Prepare a draft for specialist review.','Switch to specialist, inspect/edit, confirm clinical review and recipient, then approve.','Switch to coordinator. Export the approved version, then Mark return complete locally.','Show the completed section and inspect a missing-note case that cannot advance.'])
paras('<b>Tradeoff:</b> explicit workflow can help shared work and add overhead for a solo specialist. Compare with the practice’s configured system, including any existing unfinished-report queue. [S4]','<b>Boundary:</b> export, local completion, actual delivery and recipient acknowledgement are different events. This prototype demonstrates the first two.')
story.append(P(link('Open Practice Relay','C.html')+' · Observe ownership, routing, saved edits and handling of incomplete work.','small'))

page('Experiment and class vote','Declare the test before the result.')
story.append(tab(['ID','TASK / OBSERVATIONS','CRITICAL ERRORS'],[
 ('A','Create, inspect, edit, approve and export. Record help, source checks, corrections and active time.','Wrong patient/recipient; unsupported statement; ignored missing fact; unapproved export.'),
 ('B','Use the approved sample to name the action, office and timing. Record the answer, full-report use and comprehension time.','Wrong action/owner; invented appointment date; missing context.'),
 ('C','Complete the report through both roles; inspect a blocked case. Record routing and ownership errors, saved edits and active time.','Staff approval; wrong version/recipient; export treated as confirmed delivery; missing-note case advanced.'),
],[45,252,227]))
story.append(P('Comparison rules','h2'))
steps(['Record participant role, current software, task baseline and test order. Rotate A–B–C, B–C–A and C–A–B.','Give a task without a guided tour. Record actual help, errors and completion. Leave unknown measurements blank.','Compare the same role and task with its existing process. Different A/B/C task times do not form a valid speed ranking.','Use completion, critical errors and friction to explain the preference. A small error-free sample does not establish clinical safety.'])
story.append(P('Class vote response','h2'))
paras('Record A ___ / B ___ / C ___ / abstentions ___ / selected version ___.','Explain reasons ___ / observed issues ___ / changes ___ / next test ___.','Advance the class-selected version for the semester. If the team disagrees, take a reasoned, documented case to the teaching team under the assignment’s process. A class preference does not establish buying intent.')
story.append(P('Blank record','h2'))
paras(link('Open the observation, vote and later buyer-evidence form','evaluate.html')+'. The form exports JSON, preserves blank values as unknown, and records no result until entered. Download before reloading; no data is sent.')

page('Prioritization and commercial next steps','Build what the evidence can test.')
story.append(tab(['PRIORITIZED','DEFERRED'],[
 ('Source comparison; editable output; explicit unknowns; correct recipient; revision-specific approval; real export; next owner; blank test record.','Ambient recording; diagnosis; image interpretation; scheduling; claims; marketing; broad chart exchange; new referral network.'),
 ('A functioning experiment around the existing correspondence task.','Live model, production accounts, patient processing, live delivery, payments and PMS integration. Integration may prove necessary if copy/export adds too much effort.'),
],[262,262]))
story.append(P('Commercial path after the assignment','h2'))
steps(['Observe an accessible specialist practice’s current report workflow. Record monthly volume, total staff/clinician effort, corrections, delays, software and buyer authority. This is a learning sample, not proof of market size.','Test the relevant version against that baseline. A is the provisional first interaction because it most closely matches the reported specialist task. It has not won a customer test.','Agree a bounded pilot: deliverable, duration, recurring price, support and decision criteria. Record accepted price, payment, repeated use and renewal as separate events.','Measure earned subscription revenue, direct delivery/support cost, onboarding effort and acquisition expense. Include founder support time. Continue investment only when observed value and buyer behavior support it.'])
story.append(P('Profit discipline','h2'))
paras('Allocate annual prepayments across their service months. Earned monthly revenue minus variable model, hosting, delivery, payment and support costs gives contribution. Deduct each expense once; remaining sales and fixed operating costs determine operating profit. Show unpaid founder labor at a stated replacement cost as a separate analytical adjustment.','Cash receipts, recurring revenue, contribution, operating profit and founder income are different measures. Competitor prices, funding or selected testimonials cannot fill these fields for ReferralFlow.')
story.append(box('<b>Decision trigger:</b> if the existing tool is adequate, the task is infrequent, review/support consumes the benefit, or buyers decline a worthwhile price, revise the workflow or offer before expanding scope.'))

page('Presentation and delivery','Make the demo dependable.')
story.append(tab(['SECTION','TIME / PURPOSE'],[
 ('Problem and approach','Up to 2 minutes. State the correspondence task, limited discovery, unchanged direction and what current evidence adds.'),
 ('Three hypotheses','About 2 minutes each. Explain role, distinct interaction, scope, success signal and disconfirming observation.'),
 ('Live demos','About 2 minutes each. Run the clean paths on pages 4–6; let the product communicate.'),
 ('Justification and strategy','Explain cuts, tradeoffs, comparison limits, class-vote response and next commercial test.'),
],[155,369]))
story.append(P('Two actual team rehearsals','h2'))
steps(['Run 1: each presenter completes the clickable path, downloads the output, resets and handles the exception case. Record date, issue and fix.','Run 2: run the presentation in speaking order, time it, and check all URLs from a separate signed-out browser or device. Record actual results.'])
paras('<b>Technical verification:</b> state-transition and DOM-stub checks exercise approval, revision, recipient, export and navigation behavior. Two scripted walkthroughs exercise all three full paths. These do not establish browser rendering, customer usability or the team’s rehearsal completion.')
story.append(P('Submit / retain','h2'))
steps(['Three direct shared URLs: '+link('A','A.html')+', '+link('B','B.html')+', '+link('C','C.html')+'.','This PDF or the '+link('online presentation document','guide.html')+'.','The '+link('attributed prompt history','development-log.html')+' or '+link('JSON log','development-log.json')+'. Five real initial exchanges per prototype are preserved; current revisions are separate. Historical instructions are records of the initial build.','After the vote, save the outcome, rationale and next changes. Continue the selected version toward the Week 11 investor pitch.'])
story.append(P('The assistant has not submitted to Canvas, contacted practices, taken payments, conducted customer sessions or recorded a class vote. Fictional examples are the only data in the public prototypes.','small'))

page('Sources and provenance','Trace every decision.')
story.append(P('Primary online sources · checked 20 October 2026','h2'))
refs=[
 ('S1 · ToothNote',link('Product and named testimonial','https://toothnote.ai/')+'; '+link('Referral-letter workflow','https://toothnote.ai/referral-letters/')+'. Vendor claims and an early-access offering. No audited revenue or profit inferred.'),
 ('S2 · ToothNote pricing',link('Official pricing','https://toothnote.ai/pricing/')+'. Solo US$79/doctor/month billed annually, including referral letters. Published price; actual receipts and adoption unknown.'),
 ('S3 · DentalEMR',link('AI Referral Letter Writing for Endodontists','https://www.dentalemr.com/resources/ai-referral-letter-writing-endodontists')+', 30 June 2026. Vendor description of notes-to-reviewable-letter workflow.'),
 ('S4 · TDO',link('Referral Reports Overview','https://kb.tdo4endo.com/article.php?id=64')+', updated 24 February 2026. Official documentation of templates, unfinished reports, saving and sending.'),
 ('S5 · American Association of Endodontists',link('2026 Referral Patterns Survey','https://www.aae.org/specialty/wp-content/uploads/sites/2/2026/04/FINAL-aae-referral-pattern-survey-report-80pp-20260412.pdf')+'. Summary: printed p. 4 / PDF p. 6. Methods: printed pp. 7–8 / PDF pp. 9–10. Endodontic sample; limited response rates. No ReferralFlow willingness-to-pay evidence.'),
]
for h,t in refs:story.append(P(h,'h2'));story.append(P(t,'small'))
story.append(P('Four supplied books','h2'))
paras('Ash Maurya, <b>Running Lean</b>, 3rd edition: printed pp. 145–147, 203–204, 231, 236; physical PDF pp. 191–193, 249–250, 277, 282.','Alex Hormozi, <b>$100M Offers</b>: physical PDF pp. 52, 81.','Owen Zidar & Eric Zwick, <b>The Everywhere Millionaire</b>: physical PDF pp. 108, 125.','Napoleon Hill, <b>Think and Grow Rich</b>: physical PDF p. 125.')
story.append(P('User-provided material','h2'))
paras('Assignment text and screenshot; ReferralFlow site backup dated 20 October 2026; four PDF books. The role mapping and limited discovery account are attributed to the backup. Private chats and the book files are excluded from the public site.')
story.append(P(link('Full decision record and evidence limits','evidence.html')+' · '+link('Public prototype hub','index.html'),'small'))

def decorate(c,doc):
 c.saveState();c.setFillColor(INK);c.roundRect(44,754,25,25,6,fill=1,stroke=0);c.setFont('DejaVuBold',8);c.setFillColor(colors.white);c.drawCentredString(56.5,763,'RF');c.setFillColor(INK);c.setFont('DejaVuBold',8);c.drawString(78,763,'ReferralFlow');c.setFont('DejaVu',7);c.setFillColor(MUTED);c.drawRightString(568,763,'THREE-PROTOTYPE FIELD GUIDE');c.setStrokeColor(LINE);c.line(44,42,568,42);c.setFont('DejaVu',7);c.drawString(44,28,'Dental Demand Labs  ·  20 October 2026  ·  Fictional prototype cases');c.drawRightString(568,28,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=38,leftMargin=38,topMargin=60,bottomMargin=56,title='ReferralFlow — Three Prototypes, Evidence and Presentation Guide',author='Dental Demand Labs · AI-assisted preparation',subject='MENG 570 prototype hypotheses, evidence, demonstrations and testing plan')
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(OUT)
