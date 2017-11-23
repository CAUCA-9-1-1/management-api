DO $$
  BEGIN
    BEGIN
      -- The first query need to be a breaking one
      -- Something who make a exception is this has already be update
      ALTER TABLE public.tbl_access_token ADD session_id VARCHAR(40) NULL;
      CREATE UNIQUE INDEX tbl_webuser_username_uindex ON public.tbl_webuser (username);

      RAISE NOTICE 'Update to version 0.2';
    EXCEPTION WHEN duplicate_column THEN
      RAISE NOTICE 'Version 0.2 is already installed';
    END;
  END;
$$