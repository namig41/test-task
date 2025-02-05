from typing import Final


CREATE_REPOSITORIES_DATABASE: Final[str] = "CREATE DATABASE IF NOT EXISTS {db_name}"

CREATE_REPOSITORIES_TABLES_SQL_QUERIES: Final[list[str]] = [
    """
    CREATE TABLE IF NOT EXISTS test.repositories
    (
        name     String,
        owner    String,
        stars    Int32,
        watchers Int32,
        forks    Int32,
        language String,
        updated  DateTime
    ) ENGINE = ReplacingMergeTree(updated)
      ORDER BY name;
    """,
    """
    CREATE TABLE IF NOT EXISTS test.repositories_authors_commits
    (
        date        Date,
        repo        String,
        author      String,
        commits_num Int32
    ) ENGINE = ReplacingMergeTree
      ORDER BY (date, repo, author);
    """,
    """
    CREATE TABLE IF NOT EXISTS test.repositories_positions
    (
        date     Date,
        repo     String,
        position UInt32
    ) ENGINE = ReplacingMergeTree
      ORDER BY (date, repo);
    """,
]

DROP_REPOSITORIES_DROP_TABLES: Final[list[str]] = [
    "TRUNCATE TABLE test.repositories",
    "TRUNCATE TABLE test.repositories_positions",
    "TRUNCATE TABLE test.repositories_authors_commits",
]
