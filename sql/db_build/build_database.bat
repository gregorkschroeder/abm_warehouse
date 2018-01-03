@echo off


set script_path=
set db_server=
set db_name=
rem db_path and log_path values must be enclosed in double quotes
set db_path=""
set log_path=""

echo Creating %db_name% on %db_server% at %db_path%
sqlcmd -S %db_server% -i %script_path%create_database.sql -E -C -v db_name=%db_name% db_path=%db_path% log_path=%log_path%

echo Creating dimension tables in %db_name%
sqlcmd -S %db_server% -i %script_path%create_dimensions.sql -E -C -v db_name=%db_name%
