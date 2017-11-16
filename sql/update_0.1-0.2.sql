ALTER TABLE public.tbl_access_token ADD session_id VARCHAR(40) NULL;

CREATE UNIQUE INDEX tbl_webuser_username_uindex ON public.tbl_webuser (username);