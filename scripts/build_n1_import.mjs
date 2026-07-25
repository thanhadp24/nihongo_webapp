import fs from "node:fs";

const sourceBase = "https://jtest.net";
const level = {
  code: "N1",
  slug: "tu-vung-n1",
  jlptLevelId: 5,
  topicStartId: 207,
  sourceUrl: "https://jtest.net/tu-vung-n1"
};

const outputPath = "database/import/jlpt_n1_vocabulary_by_chapter_topic.json";

function decodeHtml(value) {
  return String(value)
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#039;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)));
}

function cleanText(html) {
  return decodeHtml(html)
    .replace(/<rt[\s\S]*?<\/rt>/g, "")
    .replace(/<rp[\s\S]*?<\/rp>/g, "")
    .replace(/<br\s*\/?\s*>/gi, " ")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

async function fetchHtml(url) {
  const response = await fetch(url, {
    headers: { "user-agent": "nihongo-webapp-data-import/1.0" }
  });

  if (!response.ok) {
    throw new Error(`Fetch failed ${response.status}: ${url}`);
  }

  return response.text();
}

function parseCatalog(html) {
  const chapters = [];
  let currentChapter = null;
  const tokenPattern =
    /<a href="\/tu-vung-n1\/chapter-(\d+)"[\s\S]*?<code[^>]*>Chapter\s+\d+<\/code><span[^>]*>([\s\S]*?)<\/span>[\s\S]*?<p class="font-weight-light">([\s\S]*?)<\/p>|<a href="\/tu-vung-n1\/chapter-(\d+)\/section-(\d+)"[\s\S]*?<span class="font-weight-bold">([\s\S]*?)<\/span>[\s\S]*?<small class="font-weight-light">([\s\S]*?)<\/small>/g;

  for (const match of html.matchAll(tokenPattern)) {
    if (match[1]) {
      currentChapter = {
        number: Number(match[1]),
        name: cleanText(match[2]),
        reading: cleanText(match[3]).replace(/\s*\/\s*$/, "") || null,
        sections: []
      };
      chapters.push(currentChapter);
      continue;
    }

    if (match[4] && currentChapter) {
      currentChapter.sections.push({
        chapter_number: Number(match[4]),
        section_number: Number(match[5]),
        name: cleanText(match[6]),
        label: cleanText(match[7]),
        source_url: `${sourceBase}/tu-vung-n1/chapter-${match[4]}/section-${match[5]}`
      });
    }
  }

  return chapters.filter((chapter) => chapter.sections.length > 0);
}

function stripPunctuation(value) {
  return String(value || "").replace(/[。.!！？?]+$/g, "").trim();
}

function normalizeWord(value) {
  return stripPunctuation(value)
    .replace(/~/g, "〜")
    .replace(/～/g, "〜")
    .replace(/くする>$/g, "（する）")
    .replace(/＜する＞/g, "（する）")
    .replace(/<する>/g, "（する）")
    .trim();
}

function normalizeReading(word, reading) {
  if (reading) return stripPunctuation(reading);

  const candidate = normalizeWord(word)
    .replace(/[「」『』（）()\[\]]/g, "")
    .replace(/〜/g, "")
    .trim();

  return candidate || normalizeWord(word);
}

const greetingWords = new Set([
  "おはよう",
  "こんにちは",
  "こんばんは",
  "さようなら",
  "ありがとう",
  "ありがとうございます",
  "ありがとうございました",
  "どうぞ",
  "どうも",
  "はじめまして"
]);

const verbMeaningPrefixes = [
  "ăn",
  "uống",
  "đi",
  "đến",
  "về",
  "làm",
  "học",
  "đọc",
  "viết",
  "nghe",
  "nói",
  "xem",
  "nhìn",
  "chơi",
  "mặc",
  "cởi",
  "đội",
  "đeo",
  "cầm",
  "giữ",
  "sống",
  "mua",
  "bán",
  "gửi",
  "ngủ",
  "dậy",
  "mở",
  "đóng",
  "đợi",
  "gặp",
  "nhớ",
  "biết",
  "hiểu",
  "quên",
  "mượn",
  "cho",
  "nhận",
  "trả",
  "tắm",
  "rửa",
  "đứng",
  "ngồi",
  "chạy",
  "bơi",
  "hát",
  "dạy",
  "nấu",
  "dùng",
  "sử dụng",
  "bắt đầu",
  "kết thúc",
  "trở",
  "thay",
  "giúp",
  "chuẩn bị",
  "kiểm tra",
  "giải thích",
  "sửa",
  "đổi",
  "mất",
  "tốn",
  "cần"
];

const adjectiveHints = [
  "mới",
  "cũ",
  "lớn",
  "nhỏ",
  "tốt",
  "xấu",
  "nóng",
  "lạnh",
  "ấm",
  "mát",
  "vui",
  "buồn",
  "đẹp",
  "tiện",
  "quan trọng",
  "ngon",
  "đắt",
  "rẻ",
  "cao",
  "thấp",
  "dài",
  "ngắn",
  "rộng",
  "hẹp",
  "nhanh",
  "chậm",
  "khó",
  "dễ",
  "bận",
  "khỏe",
  "nguy hiểm",
  "an toàn",
  "cần thiết",
  "đặc biệt"
];

const adverbHints = [
  "vừa",
  "ngay",
  "thường",
  "luôn",
  "thỉnh thoảng",
  "đôi khi",
  "chắc",
  "nhất định",
  "đặc biệt",
  "dần dần",
  "từ từ",
  "trước hết",
  "cuối cùng"
];

const questionHints = ["?", "bao nhiêu", "mấy", "ở đâu", "khi nào", "như thế nào", "tại sao"];

function includesAny(value, terms) {
  return terms.some((term) => value.includes(term));
}

function isQuestionMeaning(value) {
  return (
    includesAny(value, questionHints) ||
    value.startsWith("ai ") ||
    value === "ai" ||
    value.startsWith("gì ") ||
    value === "gì" ||
    value.startsWith("nào ") ||
    value === "nào"
  );
}

function startsWithAny(value, prefixes) {
  return prefixes.some((prefix) => value.startsWith(prefix));
}

function hasPattern(value) {
  return /[〜「」『』\[\]\/]|など|\.{3,}/.test(value);
}

function isSuru(word) {
  return word.includes("（する）") || word.endsWith("する");
}

function inferPartOfSpeech(word, reading, meaningVi) {
  const cleanWord = stripPunctuation(word);
  const meaning = stripPunctuation(meaningVi).toLowerCase();

  if (greetingWords.has(cleanWord)) return "cụm từ giao tiếp";
  if (cleanWord === "さん" || cleanWord === "ちゃん") return "hậu tố xưng hô";
  if (hasPattern(cleanWord)) return isSuru(cleanWord) ? "danh từ/động từ suru" : "mẫu câu/cụm từ";
  if (isSuru(cleanWord)) return "danh từ/động từ suru";
  if (isQuestionMeaning(meaning)) return "từ nghi vấn";
  if (includesAny(meaning, adverbHints)) return "trạng từ";
  if (startsWithAny(meaning, verbMeaningPrefixes)) return "động từ";
  if (includesAny(meaning, adjectiveHints)) return "tính từ";
  if (includesAny(meaning, adverbHints)) return "trạng từ";
  if (/^[ァ-ヶーA-Z]+$/.test(cleanWord)) return "danh từ ngoại lai";
  if (/^[一二三四五六七八九十百千万億兆\d]/.test(cleanWord) || meaning.includes("người") && reading.endsWith("にん")) {
    return "số từ/lượng từ";
  }

  return "danh từ/cụm danh từ";
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

function baseSuruWord(word) {
  return word.replace(/（する）$/, "");
}

function baseSuruReading(reading) {
  return reading.replace(/（する）$/, "").replace(/する$/, "");
}

function makeExample(word, reading, meaningVi, partOfSpeech) {
  const meaning = stripPunctuation(meaningVi);

  if (partOfSpeech === "cụm từ giao tiếp") {
    return [
      `${stripPunctuation(word)}。`,
      `${stripPunctuation(reading)}。`,
      `Câu này dùng khi nói: ${meaning}.`
    ];
  }

  if (hasPattern(word) && partOfSpeech !== "danh từ/động từ suru") {
    return [
      `「${word}」を使います。`,
      `「${reading}」をつかいます。`,
      `Tôi dùng mẫu/từ "${word}" với nghĩa: ${meaning}.`
    ];
  }

  if (partOfSpeech === "danh từ/động từ suru") {
    return [
      `毎日${baseSuruWord(word)}します。`,
      `まいにち${baseSuruReading(reading)}します。`,
      `Hằng ngày tôi ${meaning.toLowerCase()}.`
    ];
  }

  if (partOfSpeech === "động từ") {
    return [
      `毎日${masuFromWord(word)}。`,
      `まいにち${masuFromReading(reading)}。`,
      `Hằng ngày tôi ${meaning.toLowerCase()}.`
    ];
  }

  if (partOfSpeech === "tính từ") {
    return [
      `${stripPunctuation(word)}です。`,
      `${stripPunctuation(reading)}です。`,
      `Nó ${meaning.toLowerCase()}.`
    ];
  }

  if (partOfSpeech === "trạng từ") {
    return [
      `${stripPunctuation(word)}確認します。`,
      `${stripPunctuation(reading)}かくにんします。`,
      `Tôi xác nhận với sắc thái/mức độ: ${meaning}.`
    ];
  }

  if (partOfSpeech === "từ nghi vấn") {
    return [
      `${stripPunctuation(word)}ですか。`,
      `${stripPunctuation(reading)}ですか。`,
      `Câu hỏi với nghĩa: ${meaning}.`
    ];
  }

  return [
    `これは${stripPunctuation(word)}です。`,
    `これは${stripPunctuation(reading)}です。`,
    `Đây là ${meaning}.`
  ];
}

function parseSection(html) {
  const audioMatch = html.match(/<source\s+src="([^"]*\/tango\/sound\/n1\/section\/[^"]+)"/);
  const tbodyMatch = html.match(/<tbody>[\s\S]*?<\/tbody>/);
  const rows = tbodyMatch ? [...tbodyMatch[0].matchAll(/<tr>[\s\S]*?<\/tr>/g)].map((match) => match[0]) : [];

  const vocabularies = rows
    .map((row, index) => {
      const wordMatch = row.match(/<small\s+id="word\d+"[^>]*>([\s\S]*?)<\/small>/);
      const furiganaMatch = row.match(/<small\s+id="furigana\d+"[^>]*>([\s\S]*?)<\/small>/);
      const meaningMatch = row.match(/<span\s+id="meaning\d+"[^>]*>([\s\S]*?)<\/span>/);
      const word = normalizeWord(wordMatch ? cleanText(wordMatch[1]) : "");
      const reading = normalizeReading(word, furiganaMatch ? cleanText(furiganaMatch[1]) : null);
      const meaningVi = meaningMatch ? cleanText(meaningMatch[1]) : "";
      const partOfSpeech = inferPartOfSpeech(word, reading, meaningVi);
      const [exampleSentence, exampleReading, exampleMeaningVi] = makeExample(
        word,
        reading,
        meaningVi,
        partOfSpeech
      );

      return {
        word,
        reading,
        meaning_vi: meaningVi,
        part_of_speech: partOfSpeech,
        jlpt_level_id: level.jlptLevelId,
        example_sentence: exampleSentence,
        example_reading: exampleReading,
        example_meaning_vi: exampleMeaningVi,
        display_order: index + 1,
        is_published: true,
        version: 1
      };
    })
    .filter((item) => item.word && item.meaning_vi);

  return {
    topic_audio_url: audioMatch ? audioMatch[1] : null,
    vocabularies
  };
}

const catalogHtml = await fetchHtml(level.sourceUrl);
const chapters = parseCatalog(catalogHtml);
if (!chapters.length) throw new Error("No N1 chapters parsed");

const topics = [];
const vocabularies = [];
let topicId = level.topicStartId;

for (const chapter of chapters) {
  for (const sectionMeta of chapter.sections) {
    const sectionHtml = await fetchHtml(sectionMeta.source_url);
    const section = parseSection(sectionHtml);

    topics.push({
      id: topicId,
      chapter_number: chapter.number,
      chapter_name: chapter.name,
      chapter_reading: chapter.reading,
      section_number: sectionMeta.section_number,
      name: sectionMeta.name,
      description: `${level.code} - Chapter ${chapter.number}: ${chapter.name} - Section ${sectionMeta.section_number}: ${sectionMeta.name}`,
      topic_audio_url: section.topic_audio_url,
      display_order: topicId,
      is_published: true,
      version: 1,
      source_url: sectionMeta.source_url
    });

    for (const vocabulary of section.vocabularies) {
      vocabularies.push({ topic_id: topicId, ...vocabulary });
    }

    console.log(
      `chapter ${chapter.number}, section ${sectionMeta.section_number}: ${section.vocabularies.length} words`
    );
    topicId += 1;
  }
}

const output = {
  metadata: {
    name: "JLPT N1 vocabulary import data",
    jlpt_level_code: level.code,
    jlpt_level_id_assumption: level.jlptLevelId,
    source_url: level.sourceUrl,
    generated_at: new Date().toISOString(),
    notes: [
      "Import topics first, then vocabularies using topic_id.",
      "chapter_* fields are metadata because the provided topics table does not include chapter_id.",
      "word keeps kanji from the source when available; reading stores furigana/kana.",
      "example_sentence/example_reading are generated for the app and are not copied from source example rows.",
      "No helper columns are included in vocabulary rows."
    ]
  },
  chapters: chapters.map((chapter) => ({
    number: chapter.number,
    name: chapter.name,
    reading: chapter.reading,
    display_order: chapter.number
  })),
  topics,
  vocabularies
};

fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf8");
console.log(`created ${outputPath}`);
console.log(`${topics.length} topics, ${vocabularies.length} vocabularies`);

