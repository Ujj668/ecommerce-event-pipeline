import json
import random
import boto3
import time
from datetime import datetime
from faker import Faker

fake = Faker()

LAMBDA_FUNCTION_NAME = "ecommerce-ingest-handler"
AWS_REGION = "ap-south-1"  # change to your region

client = boto3.client("lambda", region_name=AWS_REGION)

EVENT_TYPES = ["page_view", "add_to_cart", "remove_from_cart", "purchase"]
PRODUCTS = [
    {"id": "P001", "name": "Running Shoes", "category": "Footwear", "price": 2999},
    {"id": "P002", "name": "Yoga Mat", "category": "Fitness", "price": 899},
    {"id": "P003", "name": "Backpack", "category": "Accessories", "price": 1499},
    {"id": "P004", "name": "Water Bottle", "category": "Fitness", "price": 499},
    {"id": "P005", "name": "Sunglasses", "category": "Accessories", "price": 1999},
]

def generate_event():
    product = random.choice(PRODUCTS)
    event_type = random.choices(
        EVENT_TYPES,
        weights=[50, 25, 10, 15]  # page_view most common, purchase least
    )[0]

    return {
        "event_id": fake.uuid4(),
        "event_type": event_type,
        "event_timestamp": datetime.utcnow().isoformat(),
        "user_id": fake.uuid4(),
        "session_id": fake.uuid4(),
        "product_id": product["id"],
        "product_name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "quantity": random.randint(1, 3) if event_type in ["add_to_cart", "purchase"] else None,
        "page_url": fake.uri(),
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "country": random.choice(["IN", "US", "UK", "DE", "SG"]),
    }

def send_event(event):
    response = client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="Event",  # async, fire and forget
        Payload=json.dumps(event).encode("utf-8"),
    )
    print(f"Sent: {event['event_type']} | {event['product_name']} | status: {response['StatusCode']}")

if __name__ == "__main__":
    print("Starting event producer... sending 50 events")
    for i in range(50):
        event = generate_event()
        send_event(event)
        time.sleep(0.5)  # half second gap between events
    print("Done. 50 events sent.")