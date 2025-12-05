# 🚀 AWS Serverless Data Pipeline (S3 → Lambda → Glue → Athena → QuickSight)
*A fully automated, beginner-friendly, production-style data engineering pipeline.*

This project processes CSV files uploaded into S3, transforms them using AWS Lambda, catalogs them using AWS Glue, queries them with Amazon Athena, and visualizes them through Amazon QuickSight using **Direct Query**.

This README is designed to be **very simple** — spoon-feeding style — so even a complete beginner can follow confidently.

---

#  🌟 1. Architecture Overview  

```
Upload CSV → S3 Raw Folder  
        ↓  
Lambda Trigger (Transforms CSV)  
        ↓  
S3 Processed Folder  
        ↓  
Glue Crawler Creates Schema  
        ↓  
Athena SQL Query  
        ↓  
QuickSight Dashboard (Direct Query)
```

![Architecture Diagram](./screenshots/architecture_diagram.png)

---

# 🗂 2. Project Structure  

```
aws-data-pipeline/
│
├── data/
│   ├── sample_small.csv
│   └── orders_large_10k.csv
│
├── lambda/
│   └── process_file.py
│
├── screenshots/
│   ├── s3_raw.png
│   ├── s3_processed.png
│   ├── lambda_function.png
│   ├── glue_crawler.png
│   ├── athena_preview.png
│   ├── dashboard.png
│   └── architecture_diagram.png
│
└── README.md
```

---

#  🧠 3. Prerequisites

Before you begin, make sure you have:

- AWS Account  
- IAM User with **AdministratorAccess**  
- Region set to **ap-south-1 (Mumbai)**  
- Basic AWS Console knowledge  

---

#  🍽 4. Step-by-Step Setup (Beginner Friendly)

---

# ⭐ STEP 1 — Create S3 Bucket Structure

Create a bucket named:

```
vinit-data-pipeline
```

Inside it, create:

```
raw/
processed/
```

### 📸 Screenshot — S3 Raw Folder  
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/393f3354-582b-4a50-9845-7b91c2006303" />

### 📸 Screenshot — S3 Processed Folder  
*(After Lambda runs)*  
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/aba2deee-44bc-4874-93e9-32641512b1a4" />

---

# ⭐ STEP 2 — Create Lambda Function

Go to:  
AWS Console → **Lambda → Create function**

| Setting | Value |
|--------|--------|
| Name | vinit-process-lambda |
| Runtime | Python 3.x |
| Role | Create new role |

### Paste this code:

```python
import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    raw_bucket = "vinit-data-pipeline"
    processed_bucket = "vinit-data-pipeline"

    for record in event['Records']:
        key = record['s3']['object']['key']

        if "raw/" not in key:
            return

        obj = s3.get_object(Bucket=raw_bucket, Key=key)
        data = obj['Body'].read().decode('utf-8').splitlines()
        reader = csv.reader(data)

        header = next(reader)
        processed_rows = list(reader)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(processed_rows)

        processed_key = key.replace("raw/", "processed/")
        s3.put_object(
            Bucket=processed_bucket,
            Key=processed_key,
            Body=output.getvalue()
        )

        print("Processed:", processed_key)
```

### ⭐ Add S3 Trigger:
- Bucket: `vinit-data-pipeline`
- Prefix: `raw/`
- Event: **PUT**

### 📸 Screenshot — Lambda Function  
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/fbd9eddc-00ca-408e-a786-56d517de379e" />

---

# ⭐ STEP 3 — Upload CSV File

Upload:

```
orders_large_10k.csv
```

into:

```
vinit-data-pipeline/raw/
```

Lambda will:

✔ Read the file  
✔ Process it  
✔ Write to `/processed/`

---

# ⭐ STEP 4 — Create Glue Crawler

**AWS Glue → Crawlers → Create Crawler**

| Option | Value |
|--------|--------|
| Source | S3 |
| S3 Path | s3://vinit-data-pipeline/processed/ |
| IAM Role | AWSGlueServiceRole |
| Database | vinit_db |
| Schedule | On Demand |

Run the crawler → It creates **processed** table.

### 📸 Screenshot — Glue Crawler Completed  
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/b574c411-5e3b-4a75-9955-1f8b1ef75e52" />

---

# ⭐ STEP 5 — Query Data in Athena

Go to Athena → Query Editor  
Select:

- Catalog: **AwsDataCatalog**  
- Database: **vinit_db**  

### Run query:

```sql
SELECT * FROM processed LIMIT 10;
```

### 📸 Screenshot — Athena Preview  
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/cc20d01f-d6d8-48a5-9d42-379129d4e9cd" />

---

# ⭐ STEP 6 — QuickSight Dashboard Setup

Open QuickSight → Datasets → **New Dataset**

Select:

- Source: Athena  
- Database: `vinit_db`  
- Table: `processed`  
- Mode: **Direct Query**

---

# ⭐ STEP 7 — Build Visual Dashboard

### Visuals to create:

#### 1️⃣ Donut Chart  
- Group: product_category  
- Value: average(amount)  

#### 2️⃣ Line Chart  
- X-axis: order_date  
- Value: sum(amount)

#### 3️⃣ Bar Chart  
- X-axis: product_category  
- Value: count(order_id)

#### 4️⃣ Horizontal Bar Chart  
- Y-axis: customer_id  
- Value: sum(amount)

#### KPIs:
- Total Revenue  
- Total Orders  
- Average Order Amount (calculated field)

Finally publish:

```
Vinit Sales Dashboard
```

---

#  👨‍💻 Author

**Vinit Tippanawar**  
AWS | Cloud | Data Engineering Enthusiast  

If you like this project, please ⭐ star the repo!

