create schema "{ns}";

create table "{ns}".things (
  id serial primary key,
  idate timestamptz not null default now(),
  validity interval not null default '10 minutes',
  key text not null,
  value bytea not null
);

create unique index on "{ns}".things(key);
