# Database Design

The main database design is drafted in:

```text
plan/thiet-ke-du-lieu-pwa-hoc-tieng-nhat.md
```

The base schema starts with a normalized `jlpt_levels` table. Content tables should use `jlpt_level_id` as a foreign key instead of free-form level strings.

