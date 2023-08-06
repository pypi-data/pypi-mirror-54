Code generator for rapidly building tabular datasets

Now supports PostgreSQL, MySQL, MS SQL Server, SQLite

Input parameters:
- **table_name** This is the name of the table to be created
- **num_rows** The number of rows to insert into the table
- **column_defs** A dictionary object with key value pairs. More info given below.
- **path** The path to the directory and file name where you want to export the sql
queries which generate the table defined above.

**column_defs** is a dictionary object of the form:
```
{column_name: {"col_type": type, ...}}
```
The definitions of the parameters for **colum_defs** is given below.

- col_type: int, float, varchar, bool
- varchar_length: int (required for MySQL and MS SQL Server)
- is_primary_key: bool
- is_name: bool
- is_email: bool
- is_date: bool
- is_timestamp: bool
- is_country: bool
- is_state: bool
- is_address: bool
- bounds: tuple(lowerbnd, upperbnd)
- fixed_collection: tuple(elem1, elem2, ..., elemn)
- fixed_map: tuple(column_name, {key: value})
- is_nullable: bool
- proportion_null: float

Note that using is_primary_key assumes the column you're defining is an integer
based column starting at 1.

If you're planning on running queries on a MySQL or MS SQL Server machine then you
need to specify the length of each varchar field using the varchar_length parameter.


Latest version notes: Last updated 2019-10-04
- refactored DataGen and child classes: JSONGen, CSVGen, SQLTableGen to force
user to input a destination path for output file
- added JSONGen class which can be used to generate json files
- added CSVGen class which can be used to generate csv files
- added Common.py file to house low level utility functions
- added ./metadata/formats.json to house common_ds_format and common_ts_format
- added SQLTableGen class to create postgres, mysql, sqlite or ms sql server create
and insert queries
- added support for address columns; street_number street city state
- added support for email address
- added support for two letter country codes
- added validation for column definition parameter types


Future improvements:
- Add support for sequential fields
- Add support for generating fixed_map
- Add support for generating fixed_collection
- Add additional names, streets, cities, states, countries
