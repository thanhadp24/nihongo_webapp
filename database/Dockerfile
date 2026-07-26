FROM mysql:8.4

COPY schema/001_initial_schema.sql /docker-entrypoint-initdb.d/001_initial_schema.sql
COPY seed/001_jlpt_levels.sql /docker-entrypoint-initdb.d/002_jlpt_levels.sql
COPY seed/002_jlpt_n5_vocabulary.sql /docker-entrypoint-initdb.d/003_jlpt_n5_vocabulary.sql
COPY seed/003_jlpt_n4_vocabulary.sql /docker-entrypoint-initdb.d/004_jlpt_n4_vocabulary.sql
COPY seed/004_jlpt_n3_vocabulary.sql /docker-entrypoint-initdb.d/005_jlpt_n3_vocabulary.sql
COPY seed/005_jlpt_n2_vocabulary.sql /docker-entrypoint-initdb.d/006_jlpt_n2_vocabulary.sql
COPY seed/006_jlpt_n1_vocabulary.sql /docker-entrypoint-initdb.d/007_jlpt_n1_vocabulary.sql
COPY seed/007_jlpt_n5_grammar.sql /docker-entrypoint-initdb.d/008_jlpt_n5_grammar.sql
COPY seed/008_jlpt_n4_grammar.sql /docker-entrypoint-initdb.d/009_jlpt_n4_grammar.sql
COPY seed/009_jlpt_n3_grammar.sql /docker-entrypoint-initdb.d/010_jlpt_n3_grammar.sql
COPY seed/010_jlpt_n2_grammar.sql /docker-entrypoint-initdb.d/011_jlpt_n2_grammar.sql
COPY seed/011_jlpt_n1_grammar.sql /docker-entrypoint-initdb.d/012_jlpt_n1_grammar.sql
