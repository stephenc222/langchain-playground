#!/usr/bin/env bash


# load the local open source database before running "sql_chain.py"
curl -o Chinook_Sqlite.sql https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql \
&& cat Chinook_Sqlite.sql | sqlite3 chinook.db
