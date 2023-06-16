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

More information about the relations can be found [here](https://gitlab.com/fedora/websites-apps/fedora-badges/database-models/-/blob/main/legacydb/TABLES.md).

Related entity relationship diagram can be found [here](https://gitlab.com/fedora/websites-apps/fedora-badges/database-models/-/blob/main/legacydb/ERDIAG.md).

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

More information about the Developer Database Environment can be found [here](https://discussion.fedoraproject.org/t/fedora-badges-developer-database-environment-is-now-available/84168).
