import boto3
import json
import time

def lambda_handler(event, context):
    # Initialize boto3 client for Athena
    client = boto3.client('athena')
    
    # Define the query
    query = "select * from  sales_db.sales_raw_data_analysis;"
    
    # Define the S3 bucket to store the results
    s3_output = 's3://its-trigger-job/result/'
    
    # Start the query execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'sales_db'
        },
        ResultConfiguration={
            'OutputLocation': s3_output,
        }
    )
    
    # Get the query execution ID
    query_execution_id = response['QueryExecutionId']
    
    # Wait for the query to complete
    while True:
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
        status = query_status['QueryExecution']['Status']['State']
        
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    
    # Check if the query succeeded
    if status == 'SUCCEEDED':
        print(f"Query succeeded and results are stored in {s3_output}")
    else:
        print(f"Query failed with status: {status}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Query execution completed')
    }