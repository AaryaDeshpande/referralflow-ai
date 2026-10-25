(function () {
  'use strict';
  const get = id => document.getElementById(id);
  const keys = [
    'patient',
    'dob',
    'case',
    'date',
    'specialist',
    'clinician',
    'practice',
    'destination',
  ];
  const sampleMeta = {
    patient: 'Alex Morgan',
    dob: '12 March 1984',
    case: 'RF-1042',
    date: '20 October 2026',
    specialist: 'Dr. Arjun Patel',
    clinician: 'Dr. Elena Ruiz',
    practice: 'Cedar Grove Dental',
    destination: 'referrals@cedargrove.example',
  };
  const sampleTranscript = [
    'Specialist: Alex, we have completed your periodontal assessment. The findings were discussed with you today.',
    'Patient: What did you find?',
    'Specialist: Localized gum inflammation was recorded around tooth nineteen.',
    'Patient: When should I come back?',
    'Specialist: Specialist review in six weeks. The earlier radiograph was not included.',
    'Patient: My referring dentist is Doctor Elena Ruiz at Cedar Grove Dental.',
    'Specialist: Please share the prior radiograph before the follow-up visit.',
  ].join('\n');
  const prepared = {
    transcript: sampleTranscript,
    assessment:
      'Localized gum inflammation was recorded around tooth nineteen.',
    treatment:
      'We have completed your periodontal assessment. The findings were discussed with you today.',
    followUp: 'Specialist review in six weeks.',
    requestedAction:
      'Please share the prior radiograph before the follow-up visit.',
    unresolved: 'The earlier radiograph was not included.',
    uncertainties: [],
  };
  let blob = null;
  let objectUrl = '';
  let recorder = null;
  let stream = null;
  let chunks = [];
  let timer = null;
  let startedAt = 0;
  let busy = false;
  let revision = 0;
  let fields = null;
  let applied = false;
  let sample = false;

  function status(message, isError = false) {
    get('voice-status').textContent = message;
    get('voice-status').dataset.error = String(isError);
  }
  function metadata() {
    return Object.fromEntries(
      keys.map(key => [key, get('voice-' + key).value.trim()])
    );
  }
  function setMetadata(value) {
    keys.forEach(key => {
      get('voice-' + key).value = value[key] || '';
    });
  }
  function recording() {
    return recorder && recorder.state === 'recording';
  }
  function refresh() {
    const consent = get('voice-consent').checked;
    get('voice-record').disabled = !consent || busy || !!recording();
    get('voice-stop').disabled = !recording();
    get('voice-process').disabled = !consent || !blob || busy || !!recording();
    get('voice-fixture').disabled =
      !consent || !sample || busy || !!recording();
    get('voice-extract').disabled =
      !consent ||
      !get('voice-transcript').value.trim() ||
      busy ||
      !!recording();
    get('voice-example').disabled = busy || !!recording();
    const locked = busy || !!recording();
    keys.forEach(key => { get('voice-' + key).disabled = locked; });
    get('voice-transcript').disabled = locked;
    get('voice-stage').textContent = recording()
      ? 'Recording'
      : busy
        ? 'Preparing report'
        : fields
          ? 'Ready for specialist review'
          : 'Ready to capture';
  }
  function releaseStream() {
    if (stream) stream.getTracks().forEach(track => track.stop());
    stream = null;
    clearInterval(timer);
    timer = null;
  }
  function setAudio(value) {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    blob = value;
    objectUrl = value ? URL.createObjectURL(value) : '';
    get('voice-audio').src = objectUrl;
    get('voice-audio').hidden = !value;
    refresh();
  }
  function sourceNote(result, meta) {
    const lines = [
      ['Patient', meta.patient],
      ['DOB', meta.dob],
      ['Case', meta.case],
      ['Date', meta.date],
      ['Specialist', meta.specialist],
      ['Referring clinician', meta.clinician],
      ['Practice', meta.practice],
      ['Recipient', meta.destination],
      ['Assessment', result.assessment],
      ['Treatment', result.treatment],
      ['Follow-up', result.followUp],
      ['Requested action', result.requestedAction],
      [
        'Unresolved',
        [result.unresolved, ...(result.uncertainties || [])]
          .filter(Boolean)
          .join(' '),
      ],
    ];
    return lines
      .filter(([, value]) => value)
      .map(([key, value]) => key + ': ' + value)
      .join('\n');
  }
  function invalidateVoice() {
    revision += 1;
    fields = null;
    get('voice-summary').hidden = true;
    if (applied && window.demo) {
      const current = window.demo.getState();
      window.demo.setSource(
        current.source.replace(/\nVoice review:.*/g, '') +
          '\nVoice review: Transcript or case details changed. Prepare a new voice report.'
      );
    }
    applied = false;
    refresh();
  }
  function showFields(result) {
    const names = {
      assessment: 'Assessment',
      treatment: 'Treatment',
      followUp: 'Follow-up',
      requestedAction: 'Requested action',
      unresolved: 'Unresolved',
    };
    get('voice-summary-fields').replaceChildren();
    Object.entries(names).forEach(([key, label]) => {
      const dt = document.createElement('dt');
      dt.textContent = label;
      const dd = document.createElement('dd');
      dd.textContent = result[key] || 'Not stated in the recording';
      get('voice-summary-fields').append(dt, dd);
    });
    get('voice-uncertainties').textContent = (result.uncertainties || []).join(
      ' '
    );
    get('voice-summary').hidden = false;
  }
  function applyResult(result, mode) {
    if (!result || typeof result.transcript !== 'string')
      throw new Error('The service returned an incomplete transcript.');
    fields = result;
    get('voice-transcript').value = result.transcript;
    showFields(result);
    window.demo.setSource(sourceNote(result, metadata()));
    window.demo.generateDraft();
    applied = true;
    status(
      mode +
        '. The letter is ready below. Compare it with the recording and transcript, then complete specialist review and recipient confirmation.'
    );
    refresh();
  }
  async function loadExample() {
    clear(false);
    const expected = revision;
    busy = true;
    refresh();
    try {
      const response = await fetch('./resources/fictional-visit.mp3');
      if (!response.ok)
        throw new Error('The sample recording could not be loaded.');
      const audio = await response.blob();
      if (expected !== revision) return;
      window.demo.loadSample();
      setMetadata(sampleMeta);
      sample = true;
      setAudio(audio);
      status(
        'Fictional visit loaded. Play it, confirm permission, then prepare the report from the recording. The prepared transcript is an explicitly labelled demonstration fallback.'
      );
    } catch (err) {
      if (expected === revision)
        status(
          err.message || 'The sample recording could not be loaded.',
          true
        );
    } finally {
      if (expected === revision) {
        busy = false;
        refresh();
      }
    }
  }
  async function startRecording() {
    if (!get('voice-consent').checked) {
      status('Confirm permission from both speakers first.', true);
      return;
    }
    if (
      !navigator.mediaDevices ||
      !navigator.mediaDevices.getUserMedia ||
      !window.MediaRecorder
    ) {
      status(
        'This browser cannot record audio here. Use a current browser on the published HTTPS page, or load the fictional visit.',
        true
      );
      return;
    }
    invalidateVoice();
    const expected = revision;
    sample = false;
    setAudio(null);
    get('voice-transcript').value = '';
    try {
      const acquired = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      if (expected !== revision || !get('voice-consent').checked) {
        acquired.getTracks().forEach(t => t.stop());
        return;
      }
      stream = acquired;
      chunks = [];
      const mime = ['audio/webm;codecs=opus', 'audio/mp4', 'audio/webm'].find(
        type => MediaRecorder.isTypeSupported(type)
      );
      recorder = new MediaRecorder(
        stream,
        mime
          ? { mimeType: mime, audioBitsPerSecond: 48000 }
          : { audioBitsPerSecond: 48000 }
      );
      recorder.ondataavailable = event => {
        if (event.data.size) chunks.push(event.data);
      };
      recorder.onstop = () => {
        const audio = new Blob(chunks, {
          type: recorder.mimeType || 'audio/webm',
        });
        releaseStream();
        if (expected !== revision) return;
        setAudio(audio);
        status(
          audio.size > 2097152
            ? "This recording exceeds the class prototype's 2 MB limit. Record a shorter clip or use the sample."
            : 'Recording saved on this page. Prepare the report when you are ready.',
          audio.size > 2097152
        );
        refresh();
      };
      recorder.onerror = () => {
        releaseStream();
        status(
          'Recording stopped because the browser reported an audio error. Retry or use the sample.',
          true
        );
        refresh();
      };
      recorder.start(500);
      startedAt = Date.now();
      timer = setInterval(() => {
        const seconds = Math.floor((Date.now() - startedAt) / 1000);
        get('voice-timer').textContent =
          Math.floor(seconds / 60) +
          ':' +
          String(seconds % 60).padStart(2, '0');
        if (seconds >= 180 && recording()) recorder.stop();
      }, 500);
      status(
        'Recording the fictional visit. Stop when the conversation is complete.'
      );
      refresh();
    } catch {
      releaseStream();
      status(
        'Microphone access was unavailable. You can retry recording or load the fictional visit.',
        true
      );
      refresh();
    }
  }
  function encodeAudio(value) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(',')[1]);
      reader.onerror = () =>
        reject(new Error('The recording could not be read.'));
      reader.readAsDataURL(value);
    });
  }
  async function process(kind) {
    if (!get('voice-consent').checked) {
      status('Confirm permission before AI processing.', true);
      return;
    }
    const meta = metadata();
    if (!meta.patient || !meta.case) {
      status(
        'Enter the fictional patient and case ID before preparing the report.',
        true
      );
      return;
    }
    if (!window.referralVoiceTransport) {
      status(
        'The AI connection is unavailable on this page. Open the published Letter Studio page or use the prepared example.',
        true
      );
      return;
    }
    if (kind === 'audio' && (!blob || blob.size > 2097152)) {
      status('Use a recording under 2 MB.', true);
      return;
    }
    const transcript = get('voice-transcript').value.trim();
    if (kind === 'text' && transcript.length < 12) {
      status(
        'Enter a complete fictional transcript before preparing a report.',
        true
      );
      return;
    }
    const expected = revision;
    busy = true;
    refresh();
    status(
      'Preparing the transcript and draft fields. Your recording remains available here.'
    );
    try {
      const response =
        kind === 'audio'
          ? await window.referralVoiceTransport.analyze({
              consent: true,
              audio: await encodeAudio(blob),
              mimeType: blob.type || 'audio/mpeg',
            })
          : await window.referralVoiceTransport.extract({
              consent: true,
              transcript,
            });
      if (expected !== revision) return;
      applyResult(
        response.result,
        response.mode || 'AI report preparation complete'
      );
    } catch {
      if (expected === revision)
        status(
          'AI processing is unavailable. Your recording and transcript are still here. Retry or choose Use prepared example transcript.',
          true
        );
    } finally {
      if (expected === revision) {
        busy = false;
        refresh();
      }
    }
  }
  function clear(resetCase = true, clearCore = true) {
    if (clearCore && applied && window.demo) {
      window.demo.setSource(
        'Voice review: Recording cleared. Prepare and review a new report.'
      );
    }
    revision += 1;
    if (recording()) recorder.stop();
    releaseStream();
    busy = false;
    sample = false;
    fields = null;
    applied = false;
    setAudio(null);
    get('voice-transcript').value = '';
    get('voice-summary').hidden = true;
    get('voice-timer').textContent = '0:00';
    if (resetCase) setMetadata({});
    status(
      'Recording cleared. Load the fictional visit or start a new test recording.'
    );
    refresh();
  }
  get('voice-example').addEventListener('click', loadExample);
  get('voice-record').addEventListener('click', startRecording);
  get('voice-stop').addEventListener('click', () => {
    if (recording()) recorder.stop();
  });
  get('voice-process').addEventListener('click', () => process('audio'));
  get('voice-extract').addEventListener('click', () => process('text'));
  get('voice-fixture').addEventListener('click', () => {
    if (!get('voice-consent').checked || !sample) return;
    applyResult(
      JSON.parse(JSON.stringify(prepared)),
      'Prepared fictional example used. This path uses a fixed transcript and fixed fields'
    );
  });
  get('voice-clear').addEventListener('click', () => clear());
  get('voice-consent').addEventListener('change', () => {
    if (!get('voice-consent').checked) {
      revision += 1;
      busy = false;
      if (recording()) recorder.stop();
      releaseStream();
      status('Permission is off. Recording and AI processing are disabled.');
    }
    refresh();
  });
  get('voice-transcript').addEventListener('input', () => {
    invalidateVoice();
    status(
      'Transcript changed. Prepare a new report from this transcript before approving it.'
    );
  });
  keys.forEach(key =>
    get('voice-' + key).addEventListener('input', invalidateVoice)
  );
  get('reset-demo').addEventListener('click', () => clear(true, false));
  get('scenario-select').addEventListener('change', () => clear(true, false));
  ['sample-note', 'start-demo', 'clear-note'].forEach(id => {
    get(id).addEventListener('click', () => clear(true, false));
  });
  window.addEventListener('pagehide', releaseStream);
  window.voiceDemo = Object.freeze({
    getSampleTranscript: () => sampleTranscript,
    getPreparedFields: () => JSON.parse(JSON.stringify(prepared)),
    getMetadata: metadata,
    sourceNote,
    clear,
    process,
    applyResult,
  });
  refresh();
})();
