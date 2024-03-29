### What is this?
1. It creates Athena table from a CSV file stored on S3
2. Waits for create-table query to complete its execution using exponential-backoff algorithm
3. Queries the Athena table containing CSV data. Waits for query execution to complete using exponential backoff algo.
4. Athena query results are stored on S3.

### Prerequisites
1. Create a workgroup, database on Athena
2. Configure query-results-location-on-s3 in workgroup settings
3. Ensure you have CSV file on S3 as per `sql/create-athena-table.sql` specifications.
4. Run `pip install -r requirements.txt` to install Python dependencies.
5. Run `aws configure` to configure AWS.

### How to run?
Execute `python app.py`