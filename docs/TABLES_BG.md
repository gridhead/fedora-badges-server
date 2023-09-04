# Relations available

## Primary entities

### Relation - `accolade`

This relation stores the records of an accolade i.e. the awarding unit used on the Fedora Badges platform.

#### Metadata

```
                                    List of relations
 Schema |   Name   | Type  |  Owner   | Persistence | Access method | Size  | Description
--------+----------+-------+----------+-------------+---------------+-------+-------------
 public | accolade | table | badgesdb | permanent   | heap          | 16 kB |
(1 row)
```

#### Columns

```
                                                                  Table "public.accolade"
  Column  |            Type             | Collation | Nullable |               Default                | Storage  | Compression | Stats target | Description
----------+-----------------------------+-----------+----------+--------------------------------------+----------+-------------+--------------+-------------
 id       | integer                     |           | not null | nextval('accolade_id_seq'::regclass) | plain    |             |              |
 name     | text                        |           | not null |                                      | extended |             |              |
 desc     | text                        |           |          |                                      | extended |             |              |
 imageurl | text                        |           | not null |                                      | extended |             |              |
 criteria | text                        |           |          |                                      | extended |             |              |
 type_id  | integer                     |           |          |                                      | plain    |             |              |
 sequence | integer                     |           |          |                                      | plain    |             |              |
 tags     | text                        |           |          |                                      | extended |             |              |
 makedate | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text)     | plain    |             |              |
 uuid     | text                        |           | not null |                                      | extended |             |              |
Indexes:
    "accolade_pkey" PRIMARY KEY, btree (id)
    "accolade_name_key" UNIQUE CONSTRAINT, btree (name)
    "accolade_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Foreign-key constraints:
    "accolade_type_id_type_fkey" FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE
Referenced by:
    TABLE "granting" CONSTRAINT "granting_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
    TABLE "invitation" CONSTRAINT "invitation_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
    TABLE "provider" CONSTRAINT "provider_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
Access method: heap
```

### Relation - `type`

This relation stores the records of a type of accolade. These are a group of accolades of a similar kind which can be
either ordered or unordered to define the progression made from one received accolade to another.

#### Metadata

```
                                  List of relations
 Schema | Name | Type  |  Owner   | Persistence | Access method | Size  | Description
--------+------+-------+----------+-------------+---------------+-------+-------------
 public | type | table | badgesdb | permanent   | heap          | 16 kB |
(1 row)
```

#### Columns

```
                                                                  Table "public.type"
  Column  |            Type             | Collation | Nullable |             Default              | Storage  | Compression | Stats target | Description
----------+-----------------------------+-----------+----------+----------------------------------+----------+-------------+--------------+-------------
 id       | integer                     |           | not null | nextval('type_id_seq'::regclass) | plain    |             |              |
 name     | text                        |           | not null |                                  | extended |             |              |
 desc     | text                        |           |          |                                  | extended |             |              |
 arranged | boolean                     |           | not null |                                  | plain    |             |              |
 uuid     | text                        |           | not null |                                  | extended |             |              |
 makedate | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text) | plain    |             |              |
Indexes:
    "type_pkey" PRIMARY KEY, btree (id)
    "type_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Referenced by:
    TABLE "accolade" CONSTRAINT "accolade_type_id_type_fkey" FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE
Access method: heap
```

### Relation - `user`

This relation stores the records of the users registered on the Fedora Badges platform.

#### Metadata

```
                                  List of relations
 Schema | Name | Type  |  Owner   | Persistence | Access method | Size  | Description
--------+------+-------+----------+-------------+---------------+-------+-------------
 public | user | table | badgesdb | permanent   | heap          | 16 kB |
(1 row)
```

#### Columns

```
                                                                  Table "public.user"
  Column  |            Type             | Collation | Nullable |             Default              | Storage  | Compression | Stats target | Description
----------+-----------------------------+-----------+----------+----------------------------------+----------+-------------+--------------+-------------
 id       | integer                     |           | not null | nextval('user_id_seq'::regclass) | plain    |             |              |
 mailaddr | text                        |           | not null |                                  | extended |             |              |
 username | text                        |           | not null |                                  | extended |             |              |
 desc     | text                        |           |          |                                  | extended |             |              |
 withdraw | boolean                     |           | not null |                                  | plain    |             |              |
 headuser | boolean                     |           | not null |                                  | plain    |             |              |
 makedate | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text) | plain    |             |              |
 uuid     | text                        |           | not null |                                  | extended |             |              |
 lastseen | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text) | plain    |             |              |
 rank     | integer                     |           | not null |                                  | plain    |             |              |
Indexes:
    "user_pkey" PRIMARY KEY, btree (id)
    "user_username_key" UNIQUE CONSTRAINT, btree (username)
    "user_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Referenced by:
    TABLE "access" CONSTRAINT "access_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
    TABLE "granting" CONSTRAINT "granting_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
    TABLE "invitation" CONSTRAINT "invitation_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
    TABLE "provider" CONSTRAINT "provider_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
Access method: heap
```

## Secondary entities

### Relation - `granting`

This relation stores the records of the occurrence of a user being provided with an accolade. It can be implied that
the said users meet the conditions required for receiving the said accolade for the automatically awarded ones.

#### Metadata

```
                                       List of relations
 Schema |   Name   | Type  |  Owner   | Persistence | Access method |    Size    | Description
--------+----------+-------+----------+-------------+---------------+------------+-------------
 public | granting | table | badgesdb | permanent   | heap          | 8192 bytes |
(1 row)
```

#### Columns

```
                                                                    Table "public.granting"
   Column    |            Type             | Collation | Nullable |               Default                | Storage  | Compression | Stats target | Description
-------------+-----------------------------+-----------+----------+--------------------------------------+----------+-------------+--------------+-------------
 id          | integer                     |           | not null | nextval('granting_id_seq'::regclass) | plain    |             |              |
 accolade_id | integer                     |           | not null |                                      | plain    |             |              |
 user_id     | integer                     |           | not null |                                      | plain    |             |              |
 reason      | text                        |           | not null |                                      | extended |             |              |
 makedate    | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text)     | plain    |             |              |
 uuid        | text                        |           | not null |                                      | extended |             |              |
Indexes:
    "granting_pkey" PRIMARY KEY, btree (id)
    "granting_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Foreign-key constraints:
    "granting_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
    "granting_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
Access method: heap
```

### Relation - `invitation`

This relation stores the records of self-service accolades that can be acquired by visiting a certain URL. These
records have a limited validity for which they can be acquired beyond which they must be manually awarded.

#### Metadata

```
                                        List of relations
 Schema |    Name    | Type  |  Owner   | Persistence | Access method |    Size    | Description
--------+------------+-------+----------+-------------+---------------+------------+-------------
 public | invitation | table | badgesdb | permanent   | heap          | 8192 bytes |
(1 row)
```

#### Columns

```
                                                                    Table "public.invitation"
   Column    |            Type             | Collation | Nullable |                Default                 | Storage  | Compression | Stats target | Description
-------------+-----------------------------+-----------+----------+----------------------------------------+----------+-------------+--------------+-------------
 id          | integer                     |           | not null | nextval('invitation_id_seq'::regclass) | plain    |             |              |
 stopdate    | timestamp without time zone |           |          |                                        | plain    |             |              |
 accolade_id | integer                     |           | not null |                                        | plain    |             |              |
 active      | boolean                     |           | not null |                                        | plain    |             |              |
 user_id     | integer                     |           | not null |                                        | plain    |             |              |
 code        | text                        |           | not null |                                        | extended |             |              |
 makedate    | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text)       | plain    |             |              |
 uuid        | text                        |           | not null |                                        | extended |             |              |
Indexes:
    "invitation_pkey" PRIMARY KEY, btree (id)
    "invitation_code_key" UNIQUE CONSTRAINT, btree (code)
    "invitation_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Foreign-key constraints:
    "invitation_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
    "invitation_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
Access method: heap
```

### Relation - `provider`

This relation stores the records of users that are able to manually award others users with a certain accolade.
Registered users must only award accolades to those users who rightfully deserve having them.

#### Metadata

```
                                     List of relations
 Schema |   Name   | Type  |  Owner   | Persistence | Access method |  Size   | Description
--------+----------+-------+----------+-------------+---------------+---------+-------------
 public | provider | table | badgesdb | permanent   | heap          | 0 bytes |
(1 row)
```

#### Columns

```
                                                         Table "public.provider"
   Column    |  Type   | Collation | Nullable |               Default                | Storage | Compression | Stats target | Description
-------------+---------+-----------+----------+--------------------------------------+---------+-------------+--------------+-------------
 id          | integer |           | not null | nextval('provider_id_seq'::regclass) | plain   |             |              |
 user_id     | integer |           | not null |                                      | plain   |             |              |
 accolade_id | integer |           | not null |                                      | plain   |             |              |
Indexes:
    "provider_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "provider_accolade_id_accolade_fkey" FOREIGN KEY (accolade_id) REFERENCES accolade(id) ON DELETE CASCADE
    "provider_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
Access method: heap
```

### Relation - `access`

This relation stores the records of the users and their access tokens that they can use to interact with the Fedora
Badges platform. Only one access token can be active at any given point in time for a particular user.

#### Metadata

```
                                   List of relations
 Schema |  Name  | Type  |  Owner   | Persistence | Access method | Size  | Description
--------+--------+-------+----------+-------------+---------------+-------+-------------
 public | access | table | badgesdb | permanent   | heap          | 16 kB |
(1 row)

```

#### Columns

```
                                                                  Table "public.access"
  Column  |            Type             | Collation | Nullable |              Default               | Storage  | Compression | Stats target | Description
----------+-----------------------------+-----------+----------+------------------------------------+----------+-------------+--------------+-------------
 id       | integer                     |           | not null | nextval('access_id_seq'::regclass) | plain    |             |              |
 user_id  | integer                     |           | not null |                                    | plain    |             |              |
 stopdate | timestamp without time zone |           |          |                                    | plain    |             |              |
 code     | text                        |           | not null |                                    | extended |             |              |
 active   | boolean                     |           | not null |                                    | plain    |             |              |
 makedate | timestamp without time zone |           | not null | (now() AT TIME ZONE 'utc'::text)   | plain    |             |              |
 uuid     | text                        |           | not null |                                    | extended |             |              |
Indexes:
    "access_pkey" PRIMARY KEY, btree (id)
    "access_code_key" UNIQUE CONSTRAINT, btree (code)
    "access_uuid_key" UNIQUE CONSTRAINT, btree (uuid)
Foreign-key constraints:
    "access_user_id_user_fkey" FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
Access method: heap
```

## Tertiary entities

### Relation - `alembic_version`

This relation stores the record of the current migration version for the schema available in the current database.

#### Metadata

```
                                         List of relations
 Schema |      Name       | Type  |  Owner   | Persistence | Access method |  Size   | Description
--------+-----------------+-------+----------+-------------+---------------+---------+-------------
 public | alembic_version | table | badgesdb | permanent   | heap          | 0 bytes |
(1 row)

```

#### Columns

```
                                               Table "public.alembic_version"
   Column    |         Type          | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
-------------+-----------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 version_num | character varying(32) |           | not null |         | extended |             |              |
Indexes:
    "alembic_version_pkc" PRIMARY KEY, btree (version_num)
Access method: heap
```
