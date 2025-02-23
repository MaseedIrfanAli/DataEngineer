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
    
    print(f"Query execution ID: {query_execution_id}")
    return {
        'statusCode': 200,
        'body': json.dumps({'query_execution_id': query_execution_id})
    }