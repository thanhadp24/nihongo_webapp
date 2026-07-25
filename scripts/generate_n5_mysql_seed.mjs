import fs from "node:fs";

const sourcePath = "database/import/jlpt_n5_vocabulary_by_chapter_topic.json";
const strictJsonPath = "database/import/jlpt_n5_vocabulary_db_import.json";
const sqlPath = "database/seed/002_jlpt_n5_vocabulary.sql";

const data = JSON.parse(fs.readFileSync(sourcePath, "utf8"));

function strictTopic(topic) {
  return {
    id: topic.id,
    name: `N5-C${String(topic.chapter_number).padStart(2, "0")}S${String(topic.section_number).padStart(2, "0")} - ${topic.name}`,
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

function sqlValue(value) {
  if (value === null || value === undefined) return "NULL";
  if (typeof value === "boolean") return value ? "TRUE" : "FALSE";
  if (typeof value === "number") return String(value);

  return `'${String(value).replace(/\\/g, "\\\\").replace(/'/g, "''")}'`;
}

function insertRows(table, columns, rows, updateColumns) {
  if (!rows.length) return "";

  const values = rows
    .map((row) => `(${columns.map((column) => sqlValue(row[column])).join(", ")})`)
    .join(",\n");
  const updates = updateColumns
    .map((column) => `${column} = VALUES(${column})`)
    .join(",\n    ");

  return `INSERT INTO ${table} (${columns.join(", ")}) VALUES\n${values}\nON DUPLICATE KEY UPDATE\n    ${updates};`;
}

const strict = {
  metadata: {
    name: "JLPT N5 strict database import data",
    source_file: sourcePath,
    jlpt_level_id_assumption: data.metadata.jlpt_level_id_assumption,
    generated_at: new Date().toISOString(),
    import_order: ["topics", "vocabularies"],
    notes: [
      "This file keeps only columns available in the provided topics and vocabularies schema.",
      "Import topics first with id values, then import vocabularies with topic_id references.",
      "created_at and updated_at are omitted so MySQL can use default timestamps."
    ]
  },
  topics: data.topics.map(strictTopic),
  vocabularies: data.vocabularies.map(strictVocabulary)
};

fs.writeFileSync(strictJsonPath, JSON.stringify(strict, null, 2), "utf8");

const topicColumns = [
  "id",
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
  "SET FOREIGN_KEY_CHECKS = 0;",
  "TRUNCATE TABLE vocabularies;",
  "TRUNCATE TABLE topics;",
  "SET FOREIGN_KEY_CHECKS = 1;",
  insertRows("topics", topicColumns, strict.topics, [
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

console.log(`created ${strictJsonPath}`);
console.log(`created ${sqlPath}`);
console.log(`${strict.topics.length} topics, ${strict.vocabularies.length} vocabularies`);
