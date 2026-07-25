import fs from "node:fs";

const importPath = "database/import/jlpt_n5_vocabulary_by_chapter_topic.json";
const data = JSON.parse(fs.readFileSync(importPath, "utf8"));

const keepAsKana = new Set([
  "です",
  "さん",
  "ちゃん",
  "はい",
  "ええ",
  "いいえ",
  "そうです",
  "ちがいます。",
  "おはよう。",
  "おはようございます。",
  "こんにちは.",
  "こんばんは。",
  "さようなら。",
  "じゃ、また。",
  "おやすみなさい。",
  "ありがとう.",
  "どういたしまして。",
  "ありがとうございます。",
  "どうぞ。",
  "どうも。",
  "はじめまして。",
  "どうぞよろしく。",
  "こちらこそ。"
]);

const manual = new Map([
  ["こんにちは.", { word: "こんにちは", reading: "こんにちは", pos: "cụm từ giao tiếp" }],
  ["ありがとう.", { word: "ありがとう", reading: "ありがとう", pos: "cụm từ giao tiếp" }],
  ["ちがいます。", { word: "ちがいます", reading: "ちがいます", pos: "mẫu câu/cụm từ" }],
  ["お父さん", { word: "お父さん", reading: "おとうさん", pos: "danh từ/cụm danh từ" }],
  ["ふくお力", { word: "福岡", reading: "ふくおか", pos: "danh từ riêng" }],
  ["オートラリア", { word: "オーストラリア", reading: "オーストラリア", pos: "danh từ riêng" }],
  ["べんきょう（する）", { word: "勉強（する）", reading: "べんきょう（する）", pos: "danh từ/động từ suru" }],
  ["れんしゅう（する）", { word: "練習（する）", reading: "れんしゅう（する）", pos: "danh từ/động từ suru" }],
  ["しつもん（する）", { word: "質問（する）", reading: "しつもん（する）", pos: "danh từ/động từ suru" }],
  ["ざんぎょう（する）", { word: "残業（する）", reading: "ざんぎょう（する）", pos: "danh từ/động từ suru" }],
  ["しゅっちょう（する）", { word: "出張（する）", reading: "しゅっちょう（する）", pos: "danh từ/động từ suru" }],
  ["じゅんび（する）", { word: "準備（する）", reading: "じゅんび（する）", pos: "danh từ/động từ suru" }],
  ["しょくじ（する）", { word: "食事（する）", reading: "しょくじ（する）", pos: "danh từ/động từ suru" }],
  ["さんぽ（する）", { word: "散歩（する）", reading: "さんぽ（する）", pos: "danh từ/động từ suru" }],
  ["うんてん（する）", { word: "運転（する）", reading: "うんてん（する）", pos: "danh từ/động từ suru" }],
  ["せんたく（する）", { word: "洗濯（する）", reading: "せんたく（する）", pos: "danh từ/động từ suru" }],
  ["そうじ（する）", { word: "掃除（する）", reading: "そうじ（する）", pos: "danh từ/động từ suru" }],
  ["しょうかい（する）", { word: "紹介（する）", reading: "しょうかい（する）", pos: "danh từ/động từ suru" }],
  ["けっこん（する）", { word: "結婚（する）", reading: "けっこん（する）", pos: "danh từ/động từ suru" }],
  ["こしょう（する）", { word: "故障（する）", reading: "こしょう（する）", pos: "danh từ/động từ suru" }],
  ["しゅうり（する）", { word: "修理（する）", reading: "しゅうり（する）", pos: "danh từ/động từ suru" }],
  ["しんぱい（する）", { word: "心配（する）", reading: "しんぱい（する）", pos: "danh từ/động từ suru" }]
]);

function normalizeWord(value) {
  return String(value)
    .replace(/~/g, "〜")
    .replace(/～/g, "〜")
    .replace(/くする>$/g, "（する）")
    .replace(/＜する＞/g, "（する）")
    .replace(/<する>/g, "（する）")
    .trim();
}

function stripPunctuation(value) {
  return String(value || "").replace(/[。.!！？?]+$/g, "").trim();
}

function lookupKey(vocabulary) {
  return stripPunctuation(String(vocabulary.reading || vocabulary.word))
    .replace(/[「」『』（）()]/g, "")
    .replace(/〜/g, "")
    .trim();
}

function hasKanji(value) {
  return /[一-龯]/.test(value);
}

function hasKana(value) {
  return /[ぁ-んァ-ヶ]/.test(value);
}

function hasPattern(value) {
  return /[〜「」『』\[\]\/]|など|\.{3,}/.test(value);
}

function shouldLookup(vocabulary) {
  const word = vocabulary.word;

  if (keepAsKana.has(word) || hasKanji(word) || hasPattern(word) || word.length < 2) {
    return false;
  }

  if (/^[A-Z]+$/.test(word)) {
    return false;
  }

  if (/^[ァ-ヶー]+$/.test(word)) {
    return false;
  }

  return hasKana(word);
}

function jishoPosToVi(parts) {
  const joined = (parts || []).join(" | ").toLowerCase();

  if (joined.includes("pronoun")) return "đại từ";
  if (joined.includes("suru")) return "danh từ/động từ suru";
  if (joined.includes("verb")) return "động từ";
  if (joined.includes("adjective")) return "tính từ";
  if (joined.includes("adverb")) return "trạng từ";
  if (joined.includes("particle")) return "trợ từ";
  if (joined.includes("counter")) return "số từ/lượng từ";
  if (joined.includes("expression")) return "mẫu câu/cụm từ";
  if (joined.includes("proper noun") || joined.includes("place")) return "danh từ riêng";
  if (joined.includes("noun")) return "danh từ/cụm danh từ";

  return null;
}

async function fetchJisho(key) {
  const url = `https://jisho.org/api/v1/search/words?keyword=${encodeURIComponent(key)}`;
  const response = await fetch(url, {
    headers: { "user-agent": "nihongo-webapp-import/1.0" }
  });

  if (!response.ok) {
    return null;
  }

  return response.json();
}

function chooseCandidate(result, key) {
  if (!result?.data?.length) {
    return null;
  }

  const candidates = [];

  for (const entry of result.data) {
    for (const japanese of entry.japanese || []) {
      if (!japanese.word || !japanese.reading) continue;
      if (japanese.reading !== key) continue;
      if (!hasKanji(japanese.word)) continue;
      if (japanese.word.length > Math.max(8, key.length + 4)) continue;

      candidates.push({
        word: japanese.word,
        reading: japanese.reading,
        common: Boolean(entry.is_common),
        pos: jishoPosToVi(entry.senses?.[0]?.parts_of_speech)
      });
    }
  }

  candidates.sort(
    (a, b) => Number(b.common) - Number(a.common) || a.word.length - b.word.length
  );

  return candidates[0] || null;
}

function cleanMeaning(value) {
  return stripPunctuation(value).replace(/\)+$/g, ")");
}

function isSuru(vocabulary) {
  return (
    vocabulary.word.includes("（する）") ||
    vocabulary.part_of_speech === "danh từ/động từ suru"
  );
}

function baseSuruWord(vocabulary) {
  return vocabulary.word.replace(/（する）$/, "");
}

function baseSuruReading(vocabulary) {
  return String(vocabulary.reading || "")
    .replace(/（する）$/, "")
    .replace(/する$/, "");
}

function masuFromReading(reading) {
  const clean = stripPunctuation(reading);
  if (clean === "する") return "します";
  if (clean === "くる") return "きます";
  if (clean === "いる") return "います";
  if (clean === "ある") return "あります";

  const map = {
    う: "います",
    く: "きます",
    ぐ: "ぎます",
    す: "します",
    つ: "ちます",
    ぬ: "にます",
    ぶ: "びます",
    む: "みます"
  };
  const last = clean.at(-1);

  if (last === "る") return `${clean.slice(0, -1)}ます`;
  if (map[last]) return `${clean.slice(0, -1)}${map[last]}`;

  return `${clean}します`;
}

function masuFromWord(word) {
  const clean = stripPunctuation(word);

  if (clean === "する") return "します";
  if (clean === "来る") return "来ます";
  if (clean === "いる") return "います";
  if (clean === "ある") return "あります";

  const map = {
    う: "います",
    く: "きます",
    ぐ: "ぎます",
    す: "します",
    つ: "ちます",
    ぬ: "にます",
    ぶ: "びます",
    む: "みます"
  };
  const last = clean.at(-1);

  if (last === "る") return `${clean.slice(0, -1)}ます`;
  if (map[last]) return `${clean.slice(0, -1)}${map[last]}`;

  return clean;
}

function isVerb(vocabulary) {
  return vocabulary.part_of_speech === "động từ";
}

function makeExample(vocabulary) {
  const meaning = cleanMeaning(vocabulary.meaning_vi);

  if (vocabulary.word === "です") {
    return ["わたしはアンです。", "わたしはアンです。", "Tôi là An."];
  }
  if (vocabulary.word === "さん") {
    return ["田中さんです。", "たなかさんです。", "Đó là anh/chị Tanaka."];
  }
  if (vocabulary.word === "ちゃん") {
    return ["ミナちゃんです。", "ミナちゃんです。", "Đó là bé Mina."];
  }
  if (vocabulary.word === "そうです") {
    return ["はい、そうです。", "はい、そうです。", "Vâng, đúng vậy."];
  }
  if (vocabulary.word === "ちがいます") {
    return ["いいえ、ちがいます。", "いいえ、ちがいます。", "Không, không phải."];
  }
  if (hasPattern(vocabulary.word) || vocabulary.part_of_speech === "trợ từ") {
    return [
      `「${vocabulary.word}」を使います。`,
      `「${vocabulary.reading || vocabulary.word}」をつかいます。`,
      `Tôi dùng mẫu/từ "${vocabulary.word}" với nghĩa: ${meaning}.`
    ];
  }
  if (isSuru(vocabulary)) {
    return [
      `毎日${baseSuruWord(vocabulary)}します。`,
      `まいにち${baseSuruReading(vocabulary)}します。`,
      `Hằng ngày tôi ${meaning.toLowerCase()}.`
    ];
  }
  if (isVerb(vocabulary)) {
    return [
      `毎日${masuFromWord(vocabulary.word)}。`,
      `まいにち${masuFromReading(vocabulary.reading)}。`,
      `Hằng ngày tôi ${meaning.toLowerCase()}.`
    ];
  }
  if (vocabulary.part_of_speech === "tính từ") {
    return [
      `${stripPunctuation(vocabulary.word)}です。`,
      `${stripPunctuation(vocabulary.reading)}です。`,
      `Nó ${meaning.toLowerCase()}.`
    ];
  }
  if (vocabulary.part_of_speech === "từ nghi vấn") {
    return [
      `${stripPunctuation(vocabulary.word)}ですか。`,
      `${stripPunctuation(vocabulary.reading)}ですか。`,
      `Câu hỏi với nghĩa: ${meaning}.`
    ];
  }

  return [
    `これは${stripPunctuation(vocabulary.word)}です。`,
    `これは${stripPunctuation(vocabulary.reading || vocabulary.word)}です。`,
    `Đây là ${meaning}.`
  ];
}

for (const vocabulary of data.vocabularies) {
  vocabulary.word = normalizeWord(vocabulary.word);
  const patch = manual.get(vocabulary.word);
  if (patch) {
    vocabulary.word = patch.word || vocabulary.word;
    vocabulary.reading = patch.reading || vocabulary.reading;
    vocabulary.part_of_speech = patch.pos || vocabulary.part_of_speech;
  }
}

const keys = [
  ...new Set(data.vocabularies.filter(shouldLookup).map((vocabulary) => lookupKey(vocabulary)))
];

console.log(`Jisho lookup keys: ${keys.length}`);

const cache = new Map();
let converted = 0;

for (let index = 0; index < keys.length; index += 1) {
  const key = keys[index];
  try {
    const result = await fetchJisho(key);
    cache.set(key, chooseCandidate(result, key));
  } catch {
    cache.set(key, null);
  }

  if ((index + 1) % 100 === 0) {
    console.log(`looked up ${index + 1}/${keys.length}`);
  }

  await new Promise((resolve) => setTimeout(resolve, 35));
}

for (const vocabulary of data.vocabularies) {
  const patch = manual.get(vocabulary.word);
  if (patch) {
    vocabulary.word = patch.word || vocabulary.word;
    vocabulary.reading = patch.reading || vocabulary.reading;
    vocabulary.part_of_speech = patch.pos || vocabulary.part_of_speech;
  }

  if (shouldLookup(vocabulary)) {
    const candidate = cache.get(lookupKey(vocabulary));
    if (candidate) {
      vocabulary.word = candidate.word;
      vocabulary.reading = candidate.reading;
      if (candidate.pos) vocabulary.part_of_speech = candidate.pos;
      converted += 1;
    }
  }

  vocabulary.reading = stripPunctuation(String(vocabulary.reading || lookupKey(vocabulary) || vocabulary.word))
    .replace(/\(する\)$/, "（する）");

  if (vocabulary.word.endsWith("（する）")) {
    vocabulary.part_of_speech = "danh từ/động từ suru";
  }

  if (!vocabulary.part_of_speech) {
    vocabulary.part_of_speech = "danh từ/cụm danh từ";
  }

  const [exampleSentence, exampleReading, exampleMeaningVi] = makeExample(vocabulary);
  vocabulary.example_sentence = exampleSentence;
  vocabulary.example_reading = exampleReading;
  vocabulary.example_meaning_vi = exampleMeaningVi;

  delete vocabulary.word_with_furigana;
  delete vocabulary.example_with_furigana;
}

data.metadata.generated_at = new Date().toISOString();
data.metadata.enrichment_sources = [
  "https://jtest.net/tu-vung-n5",
  "https://jisho.org/api/v1/search/words"
];
data.metadata.notes = [
  "Import topics first, then vocabularies using topic_id.",
  "chapter_* fields are metadata because the provided topics table does not include chapter_id.",
  "word is converted to kanji when a dictionary candidate matches the kana reading; reading stores furigana/kana.",
  "example_sentence uses kanji where available; example_reading stores the kana reading.",
  "No helper columns are included in vocabulary rows."
];
data.metadata.kanji_converted_count = converted;

fs.writeFileSync(importPath, JSON.stringify(data, null, 2), "utf8");
console.log(`converted ${converted} vocabulary rows to kanji candidates`);
