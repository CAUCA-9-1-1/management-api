CREATE EXTENSION "uuid-ossp";

create table tbl_access_secretkey
(
	id_access_secretkey uuid not null
		constraint tbl_access_secretkey_pkey
			primary key,
	id_webuser uuid,
	application_name varchar(50),
	randomkey varchar(100),
	secretkey varchar(100),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_access_token
(
	id_access_token uuid not null
		constraint tbl_access_token_id_access_token_pk
			primary key,
	id_webuser uuid not null,
	access_token varchar(100),
	refresh_token varchar(100),
	created_on timestamp default now(),
	expires_in integer default 7200,
	session_id varchar(40),
	logout_on timestamp
)
;

create table tbl_apis_action
(
	id_apis_action uuid not null
		constraint tbl_field_action_pkey
			primary key,
	id_webuser uuid,
	method varchar(10),
	params text,
	action_object varchar(50),
	action_object_id uuid,
	action_ip varchar(40),
	action_time timestamp default now()
)
;

create table tbl_external_import
(
	id_external_import uuid not null
		constraint tbl_external_import_pkey
			primary key,
	internal_id uuid not null,
	internal_table varchar(50),
	external_id varchar(50),
	external_table varchar(50),
	imported_on timestamp default now()
)
;

create table tbl_language_content
(
	id_language_content uuid not null,
	language_code varchar(2) not null,
	description varchar(250),
	constraint tbl_language_content_pkey
		primary key (id_language_content, language_code)
)
;
