# 🚀 SaaS GTM Intelligence

### End-to-End SaaS Growth, Revenue & Customer Analytics Platform

An end-to-end **SaaS Growth and Go-To-Market (GTM) Analytics project** built using **MySQL, SQL, Python, Power BI, and Streamlit**.

The project transforms raw and messy SaaS customer, subscription, and event data into actionable business insights related to:

- 📈 Revenue and MRR growth
- 👥 Customer acquisition
- 🔻 Funnel conversion and drop-offs
- ⚠️ Customer churn and revenue at risk
- 📊 Acquisition channel performance
- 💰 Customer lifetime value
- 🎯 Customer segmentation
- 🔍 Automated data quality monitoring

---

# 📌 Project Overview

SaaS companies generate large amounts of data across customer records, subscriptions, and product events. However, raw operational data is often incomplete, inconsistent, and difficult to analyze directly.

This project simulates a real-world analytics workflow where raw SaaS data is cleaned, validated, analyzed, and visualized using multiple analytics tools.

The final solution includes:

- A structured **MySQL analytics database**
- SQL-based data cleaning and business analysis
- Python-based data validation
- A multi-page **Power BI executive dashboard**
- An interactive **Streamlit analytics application**
- Automated business insights and data quality alerts

The goal is to answer key business questions:

1. How is Monthly Recurring Revenue performing over time?
2. Where are customers dropping off in the acquisition funnel?
3. Which acquisition channels generate the most valuable customers?
4. Which customer segments have the highest churn risk?
5. How much recurring revenue is currently at risk?
6. Which segments provide the highest estimated customer lifetime value?
7. Are there data quality or event tracking issues affecting business reporting?

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐬 MySQL | Database and data storage |
| 🧮 SQL | Data cleaning, transformation and business analysis |
| 🐍 Python | Data validation and analytics |
| 🐼 Pandas | Data processing and manipulation |
| 🔢 NumPy | Numerical operations |
| 📊 Power BI | Interactive business intelligence dashboard |
| 🚀 Streamlit | Interactive web analytics application |
| 📈 Plotly | Interactive data visualization |

---

# 📂 Project Structure

```text
SAAS-GTM-ANALYTICS/
│
├── README.md
│
├── data/
│   ├── customers.csv
│   ├── events.csv
│   └── subscriptions.csv
│
├── sql/
│   ├── 01_raw_table_creation.sql
│   ├── 02_data_cleaning.sql
│   ├── 03_core_metrics.sql
│   ├── 04_funnel_analysis.sql
│   └── 05_optional_analysis.sql
│
├── python/
│   └── data_validation.py
│
├── dashboard/
│   └── SaaS_GTM_Dashboard.pbix
│
└── streamlit_app/
    └── app.py
```

---

# 📊 Dataset

The analysis is based on three SaaS datasets.

## 👤 Customers

Contains customer-level information such as:

- Customer ID
- Signup date
- Customer segment
- Country
- Enterprise status

## 💳 Subscriptions

Contains subscription and revenue information:

- Customer ID
- Subscription start date
- Subscription end date
- Monthly subscription price
- Subscription status

## ⚡ Events

Contains customer product activity and funnel events:

- Customer ID
- Event type
- Event date
- Acquisition source

---

# 🧹 Data Cleaning & Preparation

The raw datasets contained several data quality issues that needed to be addressed before analysis.

### Key data issues included:

| Data Issue | Handling Approach |
|---|---|
| Empty strings | Converted to NULL values |
| Dates stored as text | Converted to proper DATE format |
| Missing signup dates | Preserved as NULL and excluded from time-based analysis |
| Missing customer segments | Preserved for analysis and flagged |
| Boolean values stored as text | Converted into binary values |
| Active subscriptions without end dates | Treated as expected active subscriptions |
| Duplicate events | Identified and removed using SQL logic |
| Multiple subscriptions per customer | Retained while applying appropriate snapshot logic |

Raw data tables are preserved separately from cleaned tables to maintain a clear data transformation process.

The original analysis also documented missing signup dates, missing segments, duplicate events, and an activation-event tracking gap. :contentReference[oaicite:2]{index=2}

---

# 🗄️ SQL Analysis

The SQL workflow is divided into multiple modular scripts.

## 1️⃣ Raw Table Creation

**File:**

```text
01_raw_table_creation.sql
```

Responsibilities:

- Create the database structure
- Create raw staging tables
- Import CSV files
- Preserve original data

---

## 2️⃣ Data Cleaning

**File:**

```text
02_data_cleaning.sql
```

Responsibilities:

- Handle missing values
- Convert data types
- Clean text fields
- Standardize date formats
- Remove duplicate events
- Create cleaned analytics tables

---

## 3️⃣ Core Business Metrics

**File:**

```text
03_core_metrics.sql
```

Key metrics include:

- Total customers
- Active customers
- Churned customers
- Total MRR
- New MRR
- Churn rate
- Retention metrics

---

## 4️⃣ Funnel Analysis

**File:**

```text
04_funnel_analysis.sql
```

The customer journey is analyzed through the following funnel:

```text
Signup
   ↓
Trial
   ↓
Activated
   ↓
Paid
   ↓
Churned
```

This analysis helps identify major conversion drop-offs and potential product or tracking issues.

---

## 5️⃣ Advanced / Optional Analysis

**File:**

```text
05_optional_analysis.sql
```

Includes additional business analysis such as:

- Channel performance
- Customer segmentation
- Revenue analysis
- Estimated LTV
- Churn comparisons

---

# 🐍 Python Data Validation

Python is used as an additional analytics and validation layer.

The Python workflow uses:

```text
Pandas
NumPy
MySQL Connector
```

Key functionality includes:

- Loading data from MySQL
- Performing data sanity checks
- Checking missing values
- Validating numerical fields
- Inspecting column structures
- Supporting data quality monitoring

This adds an additional validation layer before insights are presented through dashboards.

---

# 🚀 Streamlit Analytics Application

A major extension added to this project is an interactive **Streamlit SaaS Analytics application**.

Unlike a static dashboard, the Streamlit application provides an interactive environment for exploring SaaS business performance.

## Key Features

### 🎛️ Interactive Filters

Users can filter dashboard data by:

- Customer Segment
- Country
- Acquisition Source

---

### 📊 KPI Monitoring

The application provides key SaaS metrics such as:

- Total Customers
- Active Customers
- Paid Customers
- Total MRR
- Churned Customers
- Churn Rate
- Revenue at Risk

---

### 🔻 Customer Funnel Analysis

The application visualizes the customer journey:

```text
Signup → Trial → Activated → Paid → Churned
```

This helps identify where customers are dropping out of the product journey.

---

### ⚠️ Automated Business Alerts

The Streamlit application automatically identifies potential business problems.

Examples include:

#### Activation Tracking Gap

If the number of paying customers exceeds the number of customers with recorded activation events, the dashboard highlights a potential event tracking issue.

#### High Churn Alert

The application monitors churn rate and displays a warning when churn exceeds a defined threshold.

#### Revenue at Risk

Revenue associated with customers without recorded activation activity is highlighted as a potential onboarding or engagement opportunity.

The current Streamlit application includes automated data-quality metrics, business alerts, and a live database summary. :contentReference[oaicite:3]{index=3}

---

# 🖥️ Power BI Dashboard

The Power BI dashboard is divided into three analytical pages.

---

## 📈 Page 1 — Acquisition & Funnel

### Business Question

> Where is growth coming from and where are customers dropping off?

### Visualizations

- New MRR by Month
- Customer Funnel
- Signups by Month
- Signups by Acquisition Source

### Key Insight

The funnel highlights a significant gap between activation and paid customers, suggesting a possible activation event tracking issue.

The original analysis notes that paid customers can exceed recorded activated customers because of this documented tracking gap. :contentReference[oaicite:4]{index=4}

---

## ⚠️ Page 2 — Revenue & Churn

### Business Question

> How much revenue is at risk and which customers are most likely to churn?

### Visualizations

- Active vs Cancelled Customers
- Total MRR
- MRR at Risk
- Churned Customers
- Churn Risk by Level

### Key Insights

The dashboard helps identify:

- Revenue exposure
- High-risk customers
- Churn distribution
- Customers requiring retention or onboarding attention

The analysis identifies high-risk customers as a major area for customer-success action. :contentReference[oaicite:5]{index=5}

---

## 🎯 Page 3 — Channel & Segment Analysis

### Business Question

> Which acquisition channels and customer segments are most valuable?

### Visualizations

- Channel Efficiency Scorecard
- Estimated LTV by Segment
- ARPC by Segment
- Churn Rate by Segment

### Key Insights

The analysis compares:

- Customer acquisition efficiency
- Revenue per customer
- Retention performance
- Estimated customer lifetime value
- Segment-level churn

The original analysis found differences between ARPC, churn, and estimated LTV across SMB, Enterprise, Mid-Market, and customers without a segment value. :contentReference[oaicite:6]{index=6}

---

# 🔍 Key Business Insights

## 1. Activation Tracking Gap

A significant number of paying customers do not have a corresponding activation event.

This can create situations where:

```text
Paid Customers > Activated Customers
```

This should be investigated with the product or engineering team to determine whether activation events were not consistently instrumented.

---

## 2. Revenue at Risk

A significant portion of recurring revenue is associated with customers who may require additional onboarding or engagement.

Recommended actions:

- Improve onboarding
- Monitor product adoption
- Identify inactive customers
- Create targeted customer-success campaigns

---

## 3. Churn Risk

Customers can be categorized according to churn risk levels.

High-risk customers should be prioritized for:

- Retention campaigns
- Customer success outreach
- Product usage analysis
- Personalized engagement

---

## 4. Channel Efficiency

Acquisition channels should not be evaluated based only on the number of signups.

A strong channel should balance:

```text
Signups
+
Conversion
+
Retention
+
Revenue Per Customer
```

This project combines these metrics to create a broader view of acquisition channel performance.

---

## 5. Segment-Level Performance

Customer segments demonstrate different relationships between:

- ARPC
- Churn Rate
- Estimated LTV

This highlights why revenue alone is not sufficient for evaluating customer quality.

---

# 💡 Business Recommendations

## 🎯 Improve Activation Tracking

The difference between paid customers and recorded activated customers suggests that event tracking should be reviewed.

Recommended action:

- Audit activation event implementation
- Confirm event definitions
- Validate event coverage
- Monitor tracking completeness

---

## 💰 Focus on Revenue at Risk

Customers generating recurring revenue without strong activation signals may require intervention.

Recommended action:

- Create onboarding campaigns
- Monitor product usage
- Trigger customer-success outreach
- Develop engagement alerts

---

## 📉 Investigate High-Churn Segments

Segments with high churn should be analyzed further.

Potential next steps:

- Cohort analysis
- Customer interviews
- Product usage analysis
- Feature adoption analysis
- Pricing sensitivity analysis

---

## 📢 Optimize Acquisition Channels

Marketing investment should consider both acquisition volume and long-term customer quality.

Recommended approach:

```text
High Signups
        ↓
High Conversion
        ↓
Strong Retention
        ↓
Higher Customer Value
```

---

# ▶️ How to Run the Project

## Step 1 — Clone the Repository

```bash
git clone <your-repository-url>
cd SAAS-GTM-ANALYTICS-MAIN
```

---

## Step 2 — Create the MySQL Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE saasgtm;
USE saasgtm;
```

Then execute the SQL files in order:

```text
01_raw_table_creation.sql
        ↓
02_data_cleaning.sql
        ↓
03_core_metrics.sql
        ↓
04_funnel_analysis.sql
        ↓
05_optional_analysis.sql
```

---

# 🚀 Running the Streamlit Application

Navigate to the Streamlit folder:

```bash
cd streamlit_app
```

Install dependencies:

```bash
python -m pip install streamlit pandas numpy mysql-connector-python plotly
```

Run the application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

# 📦 Requirements

Create a `requirements.txt` file containing:

```text
streamlit
pandas
numpy
mysql-connector-python
plotly
```

Install all dependencies using:

```bash
python -m pip install -r requirements.txt
```

---

# 🔐 Configuration & Security

Database credentials should **not be committed directly to GitHub**.

Recommended approach:

Create:

```text
streamlit_app/.streamlit/secrets.toml
```

Example:

```toml
[mysql]
host = "localhost"
port = 3306
user = "your_username"
password = "your_password"
database = "saasgtm"
```

Add the following to `.gitignore`:

```text
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
```

⚠️ **Never upload your real database password to a public GitHub repository.**

---

# 📸 Dashboard Preview

Add your screenshots inside the `dashboard/` folder or a separate `screenshots/` folder.

Recommended structure:

```text
screenshots/
├── powerbi_page1.png
├── powerbi_page2.png
├── powerbi_page3.png
└── streamlit_dashboard.png
```

You can then add them to the README:

```markdown
## Power BI Dashboard

![Acquisition & Funnel](screenshots/powerbi_page1.png)

![Revenue & Churn](screenshots/powerbi_page2.png)

![Channel & Segment](screenshots/powerbi_page3.png)

## Streamlit Application

![Streamlit Dashboard](screenshots/streamlit_dashboard.png)
```

---

# 🚧 Limitations

This project also highlights several important analytical limitations.

- The dataset represents a limited time period.
- Missing activation events may affect funnel calculations.
- Some customer attributes contain missing values.
- Cost and gross margin data are unavailable.
- Estimated LTV is based on available revenue and churn information.
- Additional cohort and behavioral data would improve churn analysis.

These limitations should be considered before using the analysis for real-world strategic decisions. :contentReference[oaicite:7]{index=7}

---

# 🔮 Future Improvements

Possible future enhancements include:

- 📅 Customer cohort analysis
- 🤖 Churn prediction using machine learning
- 🔔 Automated churn alerts
- 📧 Customer retention campaign integration
- 📈 Real-time database refresh
- ☁️ Cloud deployment
- 🔄 Automated ETL pipeline
- 📊 Advanced customer segmentation
- 🧠 Predictive revenue forecasting
- 🚀 Streamlit Cloud deployment

---

# 🎯 Skills Demonstrated

This project demonstrates practical skills in:

```text
SQL
MySQL
Data Cleaning
Data Transformation
Data Validation
Exploratory Data Analysis
Business Analytics
Customer Analytics
Revenue Analytics
Churn Analysis
Funnel Analysis
Data Visualization
Power BI
Python
Pandas
Streamlit
Plotly
Dashboard Development
Business Storytelling
```

---

# 👩‍💻 Author

**Atharva Deshmukh**

Aspiring Data Analyst | SQL | Python | Power BI | Streamlit

---

# ⭐ If You Like This Project

If you found this project interesting, feel free to ⭐ star the repository!