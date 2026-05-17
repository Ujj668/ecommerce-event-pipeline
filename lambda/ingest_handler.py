import json
import boto3
import os
from datetime import datetime

s3 = boto3.client("s3")

BUCKET_NAME = "ecommerce-events-pipeline"

def lambda_handler(event, context):
    try:
        # validate required fields
        required_fields = ["event_id", "event_type", "event_timestamp", "user_id", "product_id"]
        for field in required_fields:
            if field not in event:
                raise ValueError(f"Missing required field: {field}")

        # build S3 key with date partition
        now = datetime.utcnow()
        s3_key = (
            f"raw/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"{event['event_id']}.json"
        )

        # write to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(event),
            ContentType="application/json",
        )

        print(f"Written to S3: {s3_key}")
        return {"statusCode": 200, "key": s3_key}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e