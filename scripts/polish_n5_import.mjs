import fs from "node:fs";

const importPath = "database/import/jlpt_n5_vocabulary_by_chapter_topic.json";
const data = JSON.parse(fs.readFileSync(importPath, "utf8"));

const exactByReadingMeaning = [
  { reading: "あなた", meaning: "Ông/bà", word: "あなた", pos: "đại từ" },
  { reading: "かれ", meaning: "Anh ấy", word: "彼", pos: "đại từ" },
  { reading: "かのじょ", meaning: "Cô ấy", word: "彼女", pos: "đại từ" },
  { reading: "こんにちは", meaning: "Xin chào", word: "こんにちは", pos: "cụm từ giao tiếp" },
  { reading: "ありがとう", meaning: "Cảm ơn", word: "ありがとう", pos: "cụm từ giao tiếp" },
  { reading: "ありがとうございました", meaning: "Xin cảm ơn", word: "ありがとうございました", pos: "cụm từ giao tiếp" },
  { reading: "いぬ", meaning: "Con chó", word: "犬", pos: "danh từ/cụm danh từ" },
  { reading: "ねこ", meaning: "Con mèo", word: "猫", pos: "danh từ/cụm danh từ" },
  { reading: "ある", meaning: "Có", word: "ある", pos: "động từ" },
  { reading: "さんにん", meaning: "Ba người", word: "三人", pos: "số từ/lượng từ" },
  { reading: "ごにん", meaning: "Năm người", word: "五人", pos: "số từ/lượng từ" },
  { reading: "じゅうにん", meaning: "Mười người", word: "十人", pos: "số từ/lượng từ" },
  { reading: "おとな", meaning: "Người lớn", word: "大人", pos: "danh từ/cụm danh từ" },
  { reading: "こども", meaning: "Trẻ em", word: "子供", pos: "danh từ/cụm danh từ" },
  { reading: "おとこのこ", meaning: "Cậu bé", word: "男の子", pos: "danh từ/cụm danh từ" },
  { reading: "おんなのこ", meaning: "Cô bé", word: "女の子", pos: "danh từ/cụm danh từ" },
  { reading: "かんこく", meaning: "Hàn Quốc", word: "韓国", pos: "danh từ riêng" },
  { reading: "たいわん", meaning: "Đài Loan", word: "台湾", pos: "danh từ riêng" },
  { reading: "エジプト", meaning: "Ai Cập", word: "エジプト", pos: "danh từ ngoại lai" },
  { reading: "がくせい", meaning: "Học sinh", word: "学生", pos: "danh từ/cụm danh từ" },
  { reading: "しゅうまつ", meaning: "Cuối tuần", word: "週末", pos: "danh từ/cụm danh từ" },
  { reading: "きょう", meaning: "Hôm nay", word: "今日", pos: "danh từ/cụm danh từ" },
  { reading: "かつ", meaning: "Thắng", word: "勝つ", pos: "động từ" },
  { reading: "きっと", meaning: "Chắc", word: "きっと", pos: "trạng từ" },
  { reading: "ちょっと", meaning: "Một chút", word: "ちょっと", pos: "trạng từ" },
  { reading: "わかる", meaning: "Hiểu", word: "分かる", pos: "động từ" },
  { reading: "とまる", meaning: "Nghỉ trọ", word: "泊まる", pos: "động từ" },
  { reading: "おろす", meaning: "Rút", word: "下ろす", pos: "động từ" },
  { reading: "くれる", meaning: "(Được) cho", word: "くれる", pos: "động từ" },
  { reading: "うまれる", meaning: "Chào đời", word: "生まれる", pos: "động từ" },
  { reading: "いまれる", meaning: "Chào đời", word: "生まれる", readingOverride: "うまれる", pos: "động từ" }
];

const greetings = [
  "おはよう",
  "おはようございます",
  "こんにちは",
  "こんばんは",
  "さようなら",
  "じゃ、また",
  "おやすみなさい",
  "ありがとう",
  "どういたしまして",
  "ありがとうございます",
  "どうぞ",
  "どうも",
  "はじめまして",
  "どうぞよろしく",
  "こちらこそ"
];

const verbPrefixes = [
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
  "xách",
  "sống",
  "ở",
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
  "luyện",
  "chuẩn bị",
  "giới thiệu",
  "kết hôn",
  "lái",
  "sửa",
  "lo lắng",
  "tra",
  "tìm",
  "nghỉ",
  "gọi",
  "giúp",
  "tạo",
  "có ích",
  "bắt đầu",
  "kết thúc",
  "rơi",
  "nghĩ",
  "đem",
  "mang",
  "trở nên",
  "trở thành",
  "thắng",
  "thua",
  "lên",
  "xuống",
  "đổi",
  "tiễn",
  "đưa",
  "dừng",
  "vội",
  "mất",
  "tốn",
  "băng qua",
  "rời",
  "tốt nghiệp",
  "chào đời"
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
  "thích",
  "đủ"
];

const adverbHints = [
  "hàng ngày",
  "mỗi ngày",
  "đại khái",
  "hoàn toàn",
  "ngoài ra",
  "riêng",
  "toàn bộ",
  "cùng với",
  "có lẽ",
  "chắc",
  "luôn",
  "thỉnh thoảng",
  "đôi khi",
  "thẳng",
  "gần"
];

const questionHints = ["?", "bao nhiêu", "mấy", "ở đâu", "khi nào", "ai", "gì", "nào", "như thế nào"];

function stripPunctuation(value) {
  return String(value || "").replace(/[。.!！？?]+$/g, "").trim();
}

function hasPattern(value) {
  return /[〜「」『』\[\]\/]|など|\.{3,}/.test(value);
}

function cleanMeaning(value) {
  return stripPunctuation(value).replace(/\)+$/g, ")");
}

function isSuru(vocabulary) {
  return vocabulary.word.includes("（する）") || vocabulary.part_of_speech === "danh từ/động từ suru";
}

function baseSuruWord(vocabulary) {
  return vocabulary.word.replace(/（する）$/, "");
}

function baseSuruReading(vocabulary) {
  return String(vocabulary.reading || "").replace(/（する）$/, "").replace(/する$/, "");
}

function startsWithAny(value, prefixes) {
  return prefixes.some((prefix) => value.startsWith(prefix));
}

function includesAny(value, terms) {
  return terms.some((term) => value.includes(term));
}

function inferPartOfSpeech(vocabulary) {
  const word = stripPunctuation(vocabulary.word);
  const reading = stripPunctuation(vocabulary.reading);
  const meaning = cleanMeaning(vocabulary.meaning_vi).toLowerCase();

  if (["私", "あなた", "彼", "彼女"].includes(word)) return "đại từ";
  if (word === "です" || word === "そうです" || word === "ちがいます") return "mẫu câu/cụm từ";
  if (word === "さん" || word === "ちゃん") return "hậu tố xưng hô";
  if (greetings.includes(word)) return "cụm từ giao tiếp";
  if (hasPattern(word)) return isSuru(vocabulary) ? "danh từ/động từ suru" : "mẫu câu/cụm từ";
  if (isSuru(vocabulary)) return "danh từ/động từ suru";
  if (questionHints.some((hint) => meaning.includes(hint))) return "từ nghi vấn";
  if (startsWithAny(meaning, verbPrefixes)) return "động từ";
  if (includesAny(meaning, adjectiveHints)) return "tính từ";
  if (includesAny(meaning, adverbHints)) return "trạng từ";
  if (/^[ァ-ヶーA-Z]+$/.test(word)) return "danh từ ngoại lai";
  if (vocabulary.part_of_speech === "danh từ riêng") return "danh từ riêng";
  if (["アメリカ", "日本", "中国", "韓国", "台湾", "福岡"].includes(word)) return "danh từ riêng";
  if (reading.endsWith("にん") || meaning.includes("người") && /^[一二三四五六七八九十]/.test(word)) {
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

function makeExample(vocabulary) {
  const meaning = cleanMeaning(vocabulary.meaning_vi);

  if (vocabulary.word === "です") return ["わたしはアンです。", "わたしはアンです。", "Tôi là An."];
  if (vocabulary.word === "さん") return ["田中さんです。", "たなかさんです。", "Đó là anh/chị Tanaka."];
  if (vocabulary.word === "ちゃん") return ["ミナちゃんです。", "ミナちゃんです。", "Đó là bé Mina."];
  if (vocabulary.word === "そうです") return ["はい、そうです。", "はい、そうです。", "Vâng, đúng vậy."];
  if (vocabulary.word === "ちがいます") return ["いいえ、ちがいます。", "いいえ、ちがいます。", "Không, không phải."];
  if (vocabulary.part_of_speech === "cụm từ giao tiếp") {
    const sentence = `${stripPunctuation(vocabulary.word)}。`;
    const reading = `${stripPunctuation(vocabulary.reading)}。`;
    return [sentence, reading, `Câu này dùng khi nói: ${meaning}.`];
  }
  if (vocabulary.word === "（ゆびわを）する") {
    return ["毎日指輪をします。", "まいにちゆびわをします。", "Hằng ngày tôi đeo nhẫn."];
  }
  if (hasPattern(vocabulary.word) && !isSuru(vocabulary)) {
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
  if (vocabulary.part_of_speech === "động từ") {
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
  const normalizedReading = stripPunctuation(vocabulary.reading);
  const normalizedMeaning = cleanMeaning(vocabulary.meaning_vi);
  const override = exactByReadingMeaning.find(
    (item) =>
      item.reading === normalizedReading &&
      normalizedMeaning.toLowerCase().startsWith(item.meaning.toLowerCase())
  );

  if (override) {
    vocabulary.word = override.word;
    vocabulary.reading = override.readingOverride || override.reading;
  }

  vocabulary.part_of_speech = override?.pos || inferPartOfSpeech(vocabulary);

  const [exampleSentence, exampleReading, exampleMeaningVi] = makeExample(vocabulary);
  vocabulary.example_sentence = exampleSentence;
  vocabulary.example_reading = exampleReading;
  vocabulary.example_meaning_vi = exampleMeaningVi;

  delete vocabulary.word_with_furigana;
  delete vocabulary.example_with_furigana;
}

data.metadata.generated_at = new Date().toISOString();
data.metadata.notes = [
  "Import topics first, then vocabularies using topic_id.",
  "chapter_* fields are metadata because the provided topics table does not include chapter_id.",
  "word is converted to kanji when a dictionary/manual candidate matches the kana reading; reading stores furigana/kana.",
  "example_sentence uses kanji where available; example_reading stores the kana reading.",
  "No helper columns are included in vocabulary rows."
];

fs.writeFileSync(importPath, JSON.stringify(data, null, 2), "utf8");
console.log(`polished ${data.vocabularies.length} vocabulary rows`);
