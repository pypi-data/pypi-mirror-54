This package provide universal tools to connect all kinds of database
via JDBC, using Fast/Batch load technology to speed the temporary table 
creation and query as well.

It also provide the multiprocessing capablity to pandas dataframe when dealing with cpu intensive operation on large volume data.

sample usage:

    ## connect to mysql
        import pydtc

        conn = pydtc.connect('mysql', '127.0.0.1', 'user', 'pass', database='demo')
        conn.close()

    ## pandas multiprocessing groupby then apply
        def func(df, key, value):
            dd = {key : value}
            dd['some_key'] = [len(df.other_key)]

            return pd.DataFrame(dd)

        new_df = pydtc.p_groupby_apply(func, df, 'group_key')

