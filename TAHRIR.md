# Tahrir Database

## Database name

The database is known as `tahrir`.

## Users availables

1. Role `tahrir` with CRUD access
2. Role `tahrir-readonly` with R access

## Relations available

```
             List of relations
 Schema |      Name       | Type  | Owner  
--------+-----------------+-------+--------
 public | alembic_version | table | tahrir
 public | assertions      | table | tahrir
 public | authorizations  | table | tahrir
 public | badges          | table | tahrir
 public | invitations     | table | tahrir
 public | issuers         | table | tahrir
 public | milestone       | table | tahrir
 public | persons         | table | tahrir
 public | series          | table | tahrir
 public | team            | table | tahrir
(10 rows)
```

### `alembic_version`

#### Metadata

```
                                         List of relations
 Schema |      Name       | Type  | Owner  | Persistence | Access method |    Size    | Description 
--------+-----------------+-------+--------+-------------+---------------+------------+-------------
 public | alembic_version | table | tahrir | permanent   | heap          | 8192 bytes | 
(1 row)
```

#### Columns

```
                                               Table "public.alembic_version"
   Column    |         Type          | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
-------------+-----------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 version_num | character varying(32) |           | not null |         | extended |             |              | 
Access method: heap
```

### `assertions`

#### Metadata

```
                                    List of relations
 Schema |    Name    | Type  | Owner  | Persistence | Access method | Size  | Description 
--------+------------+-------+--------+-------------+---------------+-------+-------------
 public | assertions | table | tahrir | permanent   | heap          | 95 MB | 
(1 row)
```

#### Columns

```
                                                    Table "public.assertions"
   Column   |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id         | character varying(128)      |           | not null |         | extended |             |              | 
 badge_id   | character varying(128)      |           | not null |         | extended |             |              | 
 person_id  | integer                     |           | not null |         | plain    |             |              | 
 salt       | character varying(128)      |           | not null |         | extended |             |              | 
 issued_on  | timestamp without time zone |           | not null |         | plain    |             |              | 
 recipient  | character varying(256)      |           | not null |         | extended |             |              | 
 issued_for | character varying(256)      |           |          |         | extended |             |              | 
Indexes:
    "assertions_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "assertions_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id) MATCH FULL ON UPDATE CASCADE
    "assertions_person_id_fkey" FOREIGN KEY (person_id) REFERENCES persons(id)
Access method: heap
```

### `authorizations`

#### Metadata

```
                                      List of relations
 Schema |      Name      | Type  | Owner  | Persistence | Access method | Size  | Description 
--------+----------------+-------+--------+-------------+---------------+-------+-------------
 public | authorizations | table | tahrir | permanent   | heap          | 88 kB | 
(1 row)
```

#### Columns

```
                                                                Table "public.authorizations"
  Column   |          Type          | Collation | Nullable |                  Default                   | Storage  | Compression | Stats target | Description 
-----------+------------------------+-----------+----------+--------------------------------------------+----------+-------------+--------------+-------------
 id        | integer                |           | not null | nextval('authorizations_id_seq'::regclass) | plain    |             |              | 
 badge_id  | character varying(128) |           | not null |                                            | extended |             |              | 
 person_id | integer                |           | not null |                                            | plain    |             |              | 
Indexes:
    "authorizations_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "authorizations_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
    "authorizations_person_id_fkey" FOREIGN KEY (person_id) REFERENCES persons(id)
Access method: heap
```

### `badges`

#### Metadata

```
                                   List of relations
 Schema |  Name  | Type  | Owner  | Persistence | Access method |  Size  | Description 
--------+--------+-------+--------+-------------+---------------+--------+-------------
 public | badges | table | tahrir | permanent   | heap          | 208 kB | 
(1 row)
```

#### Columns

```
                                                      Table "public.badges"
   Column    |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
-------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id          | character varying(128)      |           | not null |         | extended |             |              | 
 name        | character varying(128)      |           | not null |         | extended |             |              | 
 image       | character varying(128)      |           | not null |         | extended |             |              | 
 description | character varying(128)      |           | not null |         | extended |             |              | 
 criteria    | character varying(128)      |           | not null |         | extended |             |              | 
 issuer_id   | integer                     |           | not null |         | plain    |             |              | 
 created_on  | timestamp without time zone |           | not null |         | plain    |             |              | 
 tags        | character varying(128)      |           |          |         | extended |             |              | 
 stl         | character varying(128)      |           |          |         | extended |             |              | 
Indexes:
    "badges_pkey" PRIMARY KEY, btree (id)
    "badges_name_key" UNIQUE CONSTRAINT, btree (name)
Foreign-key constraints:
    "badges_issuer_id_fkey" FOREIGN KEY (issuer_id) REFERENCES issuers(id)
Referenced by:
    TABLE "assertions" CONSTRAINT "assertions_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id) MATCH FULL ON UPDATE CASCADE
    TABLE "authorizations" CONSTRAINT "authorizations_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
    TABLE "invitations" CONSTRAINT "invitations_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
    TABLE "milestone" CONSTRAINT "milestone_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
Access method: heap
```

### `invitations`

#### Metadata

```
                                     List of relations
 Schema |    Name     | Type  | Owner  | Persistence | Access method | Size  | Description 
--------+-------------+-------+--------+-------------+---------------+-------+-------------
 public | invitations | table | tahrir | permanent   | heap          | 64 kB | 
(1 row)
```

#### Columns

```
                                                   Table "public.invitations"
   Column   |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id         | character varying(32)       |           | not null |         | extended |             |              | 
 created_on | timestamp without time zone |           | not null |         | plain    |             |              | 
 expires_on | timestamp without time zone |           | not null |         | plain    |             |              | 
 badge_id   | character varying(128)      |           | not null |         | extended |             |              | 
 created_by | integer                     |           | not null |         | plain    |             |              | 
Indexes:
    "invitations_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "invitations_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
    "invitations_created_by_fkey" FOREIGN KEY (created_by) REFERENCES persons(id)
Access method: heap
```

### `issuers`

#### Metadata

```
                                   List of relations
 Schema |  Name   | Type  | Owner  | Persistence | Access method | Size  | Description 
--------+---------+-------+--------+-------------+---------------+-------+-------------
 public | issuers | table | tahrir | permanent   | heap          | 16 kB | 
(1 row)
```

#### Columns

```
                                                                   Table "public.issuers"
   Column   |            Type             | Collation | Nullable |               Default               | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+-------------------------------------+----------+-------------+--------------+-------------
 id         | integer                     |           | not null | nextval('issuers_id_seq'::regclass) | plain    |             |              | 
 origin     | character varying(128)      |           | not null |                                     | extended |             |              | 
 name       | character varying(128)      |           | not null |                                     | extended |             |              | 
 org        | character varying(128)      |           | not null |                                     | extended |             |              | 
 contact    | character varying(128)      |           | not null |                                     | extended |             |              | 
 created_on | timestamp without time zone |           | not null |                                     | plain    |             |              | 
Indexes:
    "issuers_pkey" PRIMARY KEY, btree (id)
    "issuers_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "badges" CONSTRAINT "badges_issuer_id_fkey" FOREIGN KEY (issuer_id) REFERENCES issuers(id)
Access method: heap
```

### `milestone`

#### Metadata

```
                                     List of relations
 Schema |   Name    | Type  | Owner  | Persistence | Access method |  Size   | Description 
--------+-----------+-------+--------+-------------+---------------+---------+-------------
 public | milestone | table | tahrir | permanent   | heap          | 0 bytes | 
(1 row)
```

#### Columns

```
                                                                Table "public.milestone"
  Column   |          Type          | Collation | Nullable |                Default                | Storage  | Compression | Stats target | Description 
-----------+------------------------+-----------+----------+---------------------------------------+----------+-------------+--------------+-------------
 id        | integer                |           | not null | nextval('milestone_id_seq'::regclass) | plain    |             |              | 
 position  | integer                |           |          |                                       | plain    |             |              | 
 badge_id  | character varying(128) |           | not null |                                       | extended |             |              | 
 series_id | character varying(128) |           | not null |                                       | extended |             |              | 
Indexes:
    "milestone_pkey" PRIMARY KEY, btree (id)
    "milestone_position_badge_id_series_id_key" UNIQUE CONSTRAINT, btree ("position", badge_id, series_id)
Foreign-key constraints:
    "milestone_badge_id_fkey" FOREIGN KEY (badge_id) REFERENCES badges(id)
    "milestone_series_id_fkey" FOREIGN KEY (series_id) REFERENCES series(id)
Access method: heap
```

### `persons`

#### Metadata

```
                                    List of relations
 Schema |  Name   | Type  | Owner  | Persistence | Access method |  Size   | Description 
--------+---------+-------+--------+-------------+---------------+---------+-------------
 public | persons | table | tahrir | permanent   | heap          | 5744 kB | 
(1 row)
```

#### Columns

```
                                                                   Table "public.persons"
   Column   |            Type             | Collation | Nullable |               Default               | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+-------------------------------------+----------+-------------+--------------+-------------
 id         | integer                     |           | not null | nextval('persons_id_seq'::regclass) | plain    |             |              | 
 email      | character varying(128)      |           | not null |                                     | extended |             |              | 
 nickname   | character varying(128)      |           |          |                                     | extended |             |              | 
 website    | character varying(128)      |           |          |                                     | extended |             |              | 
 bio        | character varying(140)      |           |          |                                     | extended |             |              | 
 created_on | timestamp without time zone |           | not null |                                     | plain    |             |              | 
 opt_out    | boolean                     |           | not null |                                     | plain    |             |              | 
 rank       | integer                     |           |          |                                     | plain    |             |              | 
 last_login | timestamp without time zone |           |          |                                     | plain    |             |              | 
Indexes:
    "persons_pkey" PRIMARY KEY, btree (id)
    "persons_email_key" UNIQUE CONSTRAINT, btree (email)
    "persons_nickname_key" UNIQUE CONSTRAINT, btree (nickname)
Referenced by:
    TABLE "assertions" CONSTRAINT "assertions_person_id_fkey" FOREIGN KEY (person_id) REFERENCES persons(id)
    TABLE "authorizations" CONSTRAINT "authorizations_person_id_fkey" FOREIGN KEY (person_id) REFERENCES persons(id)
    TABLE "invitations" CONSTRAINT "invitations_created_by_fkey" FOREIGN KEY (created_by) REFERENCES persons(id)
Access method: heap
```

### `series`

#### Metadata

```
                                     List of relations
 Schema |  Name  | Type  | Owner  | Persistence | Access method |    Size    | Description 
--------+--------+-------+--------+-------------+---------------+------------+-------------
 public | series | table | tahrir | permanent   | heap          | 8192 bytes | 
(1 row)
```

#### Columns

```
                                                       Table "public.series"
    Column    |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
--------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id           | character varying(128)      |           | not null |         | extended |             |              | 
 name         | character varying(128)      |           | not null |         | extended |             |              | 
 description  | character varying(128)      |           | not null |         | extended |             |              | 
 created_on   | timestamp without time zone |           | not null |         | plain    |             |              | 
 last_updated | timestamp without time zone |           | not null |         | plain    |             |              | 
 tags         | character varying(128)      |           |          |         | extended |             |              | 
 team_id      | character varying(128)      |           | not null |         | extended |             |              | 
Indexes:
    "series_pkey" PRIMARY KEY, btree (id)
    "series_name_key" UNIQUE CONSTRAINT, btree (name)
Foreign-key constraints:
    "series_team_id_fkey" FOREIGN KEY (team_id) REFERENCES team(id)
Referenced by:
    TABLE "milestone" CONSTRAINT "milestone_series_id_fkey" FOREIGN KEY (series_id) REFERENCES series(id)
Access method: heap
```

### `team`

#### Metadata

```
                                    List of relations
 Schema | Name | Type  | Owner  | Persistence | Access method |    Size    | Description 
--------+------+-------+--------+-------------+---------------+------------+-------------
 public | team | table | tahrir | permanent   | heap          | 8192 bytes | 
(1 row)
```

#### Columns

```
                                                       Table "public.team"
   Column   |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id         | character varying(128)      |           | not null |         | extended |             |              | 
 name       | character varying(128)      |           | not null |         | extended |             |              | 
 created_on | timestamp without time zone |           | not null |         | plain    |             |              | 
Indexes:
    "team_pkey" PRIMARY KEY, btree (id)
    "team_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "series" CONSTRAINT "series_team_id_fkey" FOREIGN KEY (team_id) REFERENCES team(id)
Access method: heap
```

## Experimentation

If the members want to take the database for a spin by themselves, a snapshot 
of the Tahrir database is made available in a selhosted community 
infrastructure at `badgesdb-main.apexaltruism.net:5432` with both the 
aforementioned users with their respective access levels. The credentials of
the users are mentioned below.

| # | Username          | Password                                         | Access |
|---|-------------------|--------------------------------------------------|--------|
| 1 | `tahrir`          | (Can be requested by reaching out to @t0xic0der) | CRUD   |
| 2 | `tahrir-readonly` | `tahrir-readonly`                                | R      |

A dashboard application is also made available at 
https://explorer.apexaltruism.net for those who are not confident with 
interacting with PostgreSQL environments to comfortably explore the existing 
database environment. Unlike the aforementioned database environment, this has
credentials available only for the read access. The credentials of the users
are mentioned below.

| # | Username            | Password           | Access |
|---|---------------------|--------------------|--------|
| 1 | `badgesdb-readonly` | `l0v3f3d0r4b4d8e5` | R      |



