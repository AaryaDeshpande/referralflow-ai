import { api } from '@appdeploy/client';

declare global {
  interface Window {
    referralVoiceTransport: {
      analyze: (input: Record<string, unknown>) => Promise<unknown>;
      extract: (input: Record<string, unknown>) => Promise<unknown>;
    };
  }
}

window.referralVoiceTransport = {
  analyze: async input => (await api.post('/api/voice/analyze', input)).data,
  extract: async input => (await api.post('/api/voice/extract', input)).data,
};
