
create table tbl_permission
(
	id_permission uuid not null
		constraint tbl_permission_pkey
			primary key,
	id_permission_object uuid,
	id_permission_system uuid,
	id_permission_system_feature uuid,
	comments varchar(400),
	created_on timestamp default now(),
	access boolean default false not null
)
;

create table tbl_permission_object
(
	id_permission_object uuid not null
		constraint tbl_permission_object_pkey
			primary key,
	id_permission_object_parent uuid,
	object_table varchar(255),
	generic_id varchar(50),
	id_permission_system uuid,
	is_group boolean default false not null,
	group_name varchar(255)
)
;

create table tbl_permission_system
(
	id_permission_system uuid not null
		constraint tbl_permission_system_pkey
			primary key,
	description varchar(400)
)
;

create table tbl_permission_system_feature
(
	id_permission_system_feature uuid not null
		constraint tbl_permission_system_feature_pkey
			primary key,
	id_permission_system uuid,
	feature_name varchar(50),
	description varchar(255),
	default_value boolean default false not null
)
;
