export function speakJapanese(text: string) {
  const cleanText = text.trim();

  if (!cleanText || typeof window === "undefined" || !("speechSynthesis" in window)) return;

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = "ja-JP";
  utterance.rate = 0.88;
  utterance.pitch = 1;

  const voice = window.speechSynthesis
    .getVoices()
    .find((item) => item.lang.toLowerCase().startsWith("ja"));

  if (voice) utterance.voice = voice;

  window.speechSynthesis.speak(utterance);
}
