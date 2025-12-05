import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    bucket_name = "vinit-data-pipeline"

    for record in event['Records']:
        key = record['s3']['object']['key']

        # Only process files inside raw/ folder
        if not key.startswith("raw/"):
            print("Skipping non-raw file:", key)
            return

        print("Processing:", key)

        # Read the raw CSV file
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read().decode("utf-8").splitlines()
        reader = csv.reader(data)

        header = next(reader)  # Extract header
        rows = list(reader)    # Extract rows

        # Prepare output CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(rows)

        # Write to processed/ folder
        processed_key = key.replace("raw/", "processed/")
        s3.put_object(
            Bucket=bucket_name,
            Key=processed_key,
            Body=output.getvalue()
        )

        print("File processed successfully:", processed_key)

    return {
        "statusCode": 200,
        "body": f"Processed file saved to {processed_key}"
    }
