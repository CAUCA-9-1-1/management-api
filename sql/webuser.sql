
create table tbl_webuser
(
	id_webuser uuid not null
		constraint tbl_webuser_pkey
			primary key,
	username varchar(100),
	password varchar(100),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_webuser_attributes
(
	id_webuser uuid not null,
	attribute_name varchar(50) not null,
	attribute_value varchar(200),
	constraint tbl_webuser_attributes_pkey
		primary key (id_webuser, attribute_name)
)
;

