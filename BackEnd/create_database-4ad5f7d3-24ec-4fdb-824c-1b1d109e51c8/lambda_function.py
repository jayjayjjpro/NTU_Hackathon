
import json
import sys
import logging
import psycopg2
import os

def lambda_handler(event, context):
    # TODO implement
    try:
        connection = psycopg2.connect(database=os.environ["DATABASE"],
                            user=os.environ["USERNAME"],
                            password=os.environ["PASSWORD"],
                            host=os.environ["HOST"],
                            port="5432")
        try:
            cursor = connection.cursor()
            connection.autocommit = True
            cursor.execute("CREATE DATABASE " + event["queryStringParameters"]["db_name"])
            return {
                'statusCode': 200,
                'body': json.dumps("Database created")
            }
        except Exception as e:
            print(e)
            return {
                'statusCode': 200,
                'body': json.dumps("ERROR: Unexpected error")
            }
    except Exception as e:
        print("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
        print(e)
        return {
            'statusCode': 200,
            'body': json.dumps('ERROR: Unexpected error: Could not connect to PostgreSQL instance.')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
