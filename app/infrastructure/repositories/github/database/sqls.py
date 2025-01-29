from typing import Final


CREATE_REPOSITORIES_DATABASE: Final[str] = "CREATE DATABASE IF NOT EXISTS {db_name}"

# TODO: Добавить форматирование для базы данных

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
INSERT INTO test.repositories (name, owner, stars, watchers, forks, language, updated)
VALUES ({name}, {owner}, {stars}, {watchers}, {forks}, {language}, now())
"""

INSERT_POSITION: Final[
    str
] = """
INSERT INTO test.repositories_positions (date, repo, position)
VALUES (now(), {repo}, {position})
"""

INSERT_AUTHORS_COMMITS: Final[
    str
] = """
INSERT INTO test.repositories_authors_commits (date, repo, author, commits_num)
VALUES (now(), {repo}, {author}, {commits_num})
"""

GET_REPOSITORY_WITH_DETAILS: Final[
    str
] = """
SELECT
    r.name name,
    r.owner owner,
    p.position position,
    r.stars stars,
    r.watchers watchers,
    r.forks forks,
    r.language language,
    rac.date date,
    rac.author author,
    rac.commits_num commits_num
FROM
    test.repositories AS r
LEFT JOIN
    test.repositories_positions AS p
    ON r.name = p.repo
LEFT JOIN
    test.repositories_authors_commits AS rac
    ON r.name = rac.repo AND rac.date = today()
WHERE
    r.name = '{name}' AND r.owner = '{owner}'
"""
