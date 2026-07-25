import fs from "node:fs";
import { fileURLToPath } from "node:url";

const levels = [
  { code: "N5", slug: "n5", jlptLevelId: 1, sourceSeedNumber: "002", chapterStartId: 1 },
  { code: "N4", slug: "n4", jlptLevelId: 2, sourceSeedNumber: "003", chapterStartId: 11 },
  { code: "N3", slug: "n3", jlptLevelId: 3, sourceSeedNumber: "004", chapterStartId: 18 },
  { code: "N2", slug: "n2", jlptLevelId: 4, sourceSeedNumber: "005", chapterStartId: 30 },
  { code: "N1", slug: "n1", jlptLevelId: 5, sourceSeedNumber: "006", chapterStartId: 42 }
];

function sqlValue(value) {
  if (value === null || value === undefined) return "NULL";
  if (typeof value === "boolean") return value ? "TRUE" : "FALSE";
  if (typeof value === "number") return String(value);
  return `'${String(value).replace(/\\/g, "\\\\").replace(/'/g, "''")}'`;
}

function insertRows(table, columns, rows, updateColumns) {
  const values = rows
    .map((row) => `(${columns.map((column) => sqlValue(row[column])).join(", ")})`)
    .join(",\n");
  const updates = updateColumns
    .map((column) => `${column} = VALUES(${column})`)
    .join(",\n    ");

  return `INSERT INTO ${table} (${columns.join(", ")}) VALUES\n${values}\nON DUPLICATE KEY UPDATE\n    ${updates};`;
}

function strictChapter(chapter, level) {
  return {
    id: level.chapterStartId + chapter.number - 1,
    jlpt_level_id: level.jlptLevelId,
    chapter_number: chapter.number,
    name: chapter.name,
    reading: chapter.reading,
    description: `${level.code} - Chapter ${chapter.number}: ${chapter.name}`,
    display_order: chapter.display_order,
    is_published: true,
    version: 1
  };
}

function strictTopic(topic, level, chapterByNumber) {
  const chapter = chapterByNumber.get(topic.chapter_number);
  if (!chapter) {
    throw new Error(`${level.code} topic ${topic.id} references missing chapter ${topic.chapter_number}`);
  }

  return {
    id: topic.id,
    chapter_id: chapter.id,
    section_number: topic.section_number,
    name: `${level.code}-C${String(topic.chapter_number).padStart(2, "0")}S${String(topic.section_number).padStart(2, "0")} - ${topic.name}`,
    description: topic.description,
    topic_audio_url: topic.topic_audio_url,
    display_order: topic.display_order,
    is_published: topic.is_published,
    version: topic.version
  };
}

function strictVocabulary(vocabulary) {
  return {
    topic_id: vocabulary.topic_id,
    word: vocabulary.word,
    reading: vocabulary.reading,
    meaning_vi: vocabulary.meaning_vi,
    part_of_speech: vocabulary.part_of_speech,
    jlpt_level_id: vocabulary.jlpt_level_id,
    example_sentence: vocabulary.example_sentence,
    example_reading: vocabulary.example_reading,
    example_meaning_vi: vocabulary.example_meaning_vi,
    display_order: vocabulary.display_order,
    is_published: vocabulary.is_published,
    version: vocabulary.version
  };
}

function generateLevel(level) {
  const sourcePath = `database/import/jlpt_${level.slug}_vocabulary_by_chapter_topic.json`;
  const strictJsonPath = `database/import/jlpt_${level.slug}_vocabulary_db_import.json`;
  const sqlPath = `database/seed/${level.sourceSeedNumber}_jlpt_${level.slug}_vocabulary.sql`;
  const data = JSON.parse(fs.readFileSync(sourcePath, "utf8"));

  const chapters = data.chapters.map((chapter) => strictChapter(chapter, level));
  const chapterByNumber = new Map(chapters.map((chapter) => [chapter.chapter_number, chapter]));
  const topics = data.topics.map((topic) => strictTopic(topic, level, chapterByNumber));
  const vocabularies = data.vocabularies.map(strictVocabulary);

  const strict = {
    metadata: {
      name: `JLPT ${level.code} strict database import data`,
      source_file: sourcePath,
      jlpt_level_id_assumption: level.jlptLevelId,
      generated_at: new Date().toISOString(),
      import_order: ["chapters", "topics", "vocabularies"],
      notes: [
        "This file keeps only columns available in the chapters, topics, and vocabularies schema.",
        "Import chapters first, then topics with chapter_id references, then vocabularies with topic_id references.",
        "created_at and updated_at are omitted so MySQL can use default timestamps."
      ]
    },
    chapters,
    topics,
    vocabularies
  };

  fs.writeFileSync(strictJsonPath, JSON.stringify(strict, null, 2), "utf8");

  const chapterColumns = [
    "id",
    "jlpt_level_id",
    "chapter_number",
    "name",
    "reading",
    "description",
    "display_order",
    "is_published",
    "version"
  ];
  const topicColumns = [
    "id",
    "chapter_id",
    "section_number",
    "name",
    "description",
    "topic_audio_url",
    "display_order",
    "is_published",
    "version"
  ];
  const vocabularyColumns = [
    "topic_id",
    "word",
    "reading",
    "meaning_vi",
    "part_of_speech",
    "jlpt_level_id",
    "example_sentence",
    "example_reading",
    "example_meaning_vi",
    "display_order",
    "is_published",
    "version"
  ];

  const sql = [
    "SET NAMES utf8mb4;",
    insertRows("chapters", chapterColumns, strict.chapters, [
      "jlpt_level_id",
      "chapter_number",
      "name",
      "reading",
      "description",
      "display_order",
      "is_published",
      "version"
    ]),
    insertRows("topics", topicColumns, strict.topics, [
      "chapter_id",
      "section_number",
      "name",
      "description",
      "topic_audio_url",
      "display_order",
      "is_published",
      "version"
    ]),
    insertRows("vocabularies", vocabularyColumns, strict.vocabularies, [
      "word",
      "reading",
      "meaning_vi",
      "part_of_speech",
      "jlpt_level_id",
      "example_sentence",
      "example_reading",
      "example_meaning_vi",
      "display_order",
      "is_published",
      "version"
    ])
  ].join("\n\n");

  fs.writeFileSync(sqlPath, `${sql}\n`, "utf8");

  console.log(
    `${level.code}: ${strict.chapters.length} chapters, ${strict.topics.length} topics, ${strict.vocabularies.length} vocabularies`
  );
}

export function generateLevelByCode(code) {
  const level = levels.find((item) => item.code === code.toUpperCase());
  if (!level) {
    throw new Error(`Unknown JLPT level: ${code}`);
  }

  generateLevel(level);
}

export function generateAllLevels() {
  for (const level of levels) {
    generateLevel(level);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const requestedLevels = process.argv.slice(2);

  if (requestedLevels.length) {
    for (const code of requestedLevels) {
      generateLevelByCode(code);
    }
  } else {
    generateAllLevels();
  }
}
