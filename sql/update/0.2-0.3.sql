DO $$
  BEGIN
    BEGIN
      -- The first query need to be a breaking one
      -- Something who make a exception is this has already be update
      ALTER TABLE public.tbl_access_token ADD logout_on TIMESTAMP NULL;

      RAISE NOTICE 'Update to version 0.3';
    EXCEPTION WHEN duplicate_column THEN
      RAISE NOTICE 'Version 0.3 is already installed';
    END;
  END;
$$