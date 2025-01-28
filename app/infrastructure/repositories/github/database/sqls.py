from typing import Final


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

INSERT_REPOSITORY: Final[
    str
] = """
INSERT INTO repositories (name, owner, stars, watchers, forks, language)
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id;
"""

GET_REPOSITORY_WITH_DETAILS: Final[
    str
] = """
SELECT
    r.name,
    r.owner,
    p.position,
    r.stars,
    r.watchers,
    r.forks,
    r.language,
    rac.date,
    rac.author,
    rac.commits_num
FROM
    test.repositories AS r
LEFT JOIN
    test.repositories_positions AS p
    ON r.name = p.repo
LEFT JOIN
    test.repositories_authors_commits AS rac
    ON r.name = rac.repo AND rac.date = today()
WHERE
    r.name = {name: String} AND r.owner = {owner: String};
"""
