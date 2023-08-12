import json
import sys
import logging
import psycopg2
import os
from decimal import *

def lambda_handler(event, context):
    # create the database connection outside of the handler to allow connections to be
    # re-used by subsequent function invocations.
    try:
        connection = psycopg2.connect(database=event["queryStringParameters"]["db_name"],
                            user=os.environ["USERNAME"],
                            password=os.environ["PASSWORD"],
                            host=os.environ["HOST"],
                            port="5432")
        try:
            cursor = connection.cursor()
            connection.autocommit = True
            cursor.execute(event["queryStringParameters"]["query_str"])
            print(event["queryStringParameters"]["query_str"])
            try: # if there is results to be returned
                result = cursor.fetchall()
                for i in range(len(result)):
                    result[i] = list(result[i])
                    for j in range(len(result[i])):
                        if isinstance(result[i][j], Decimal):
                            result[i][j] = float(result[i][j])
                    result[i] = tuple(result[i])
                return {
                    'statusCode': 200,
                    'body': json.dumps(list(result))
                }
            except Exception as e: # if there is no results to be returned
                return {
                    'statusCode': 200,
                    'body': str(e)
                }
        except Exception as e:
            connection.commit()
            cursor.close()
            connection.close()
            return {
                'statusCode': 200,
                'body': str(e)
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 200,
            'body': str(e)
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
