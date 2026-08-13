# 📊 CSV Data Q&A AI Agent 

An agentic data inquiry system built for the **ROOMAN AI Challenge (Junior AI Research Associate Selection Round)**. It translates natural language questions into executable Pandas code and calculates exact results in a Python sandbox to eliminate LLM mathematical hallucinations.

---

## 🎯 1-Sentence Summary
> "My agent takes a natural language question about a CSV spreadsheet and produces an exact, mathematically computed answer backed by executable Python code execution."

---

## ⚡ Quickstart Guide

### Prerequisites
- Python 3.9+
- A free API Key from [Groq Console](https://console.groq.com/)

### 1. Installation
```bash
git clone [https://github.com/rishitha2811/CSV-Data-Q-A-Agent.git](https://github.com/rishitha2811/CSV-Data-Q-A-Agent.git)
cd CSV-Data-Q-A-Agent
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

```

### 2. Set API Key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_actual_groq_key_here

```

### 3. Run the Agent

Launch the interactive chat loop:

```bash
python app.py

```

---

## 🧮 How Numbers Are Computed (Zero Hallucination Strategy)

1. **Schema & Preview Analysis:** The agent inspects `df.info()` and top sample rows without sending full confidential raw data to context windows.
2. **Deterministic Code Generation:** The LLM (`llama-3.3-70b-versatile`) acts strictly as a code generator, converting plain English questions into runnable `pandas` Python code.
3. **Sandbox Execution:** The generated code runs in an isolated Python runtime using `exec()`. The mathematical computation happens strictly on local CPU/Memory.
4. **Natural Synthesis:** The raw numerical output from `pandas` is fed back to the LLM to format a human-readable explanation with exact cited numbers.

---

## 🧪 Deliverables: Sample Questions & Outputs

Below are the actual test queries executed against `data/sales_data.csv` with exact agent outputs:

### Q1: "What is the total sales amount across all regions?"

* **Executed Code:**
```python
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Sales_Amount'] = df_split['Sales_Amount'].astype(float)
result = df_split['Sales_Amount'].sum()

```


* **Computed Result:** `12870.5`
* **Answer:** The total sales amount across all regions is **12870.5**.

---

### Q2: "Which region recorded the highest total profit?"

* **Executed Code:**
```python
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Profit'] = pd.to_numeric(df_split['Profit'])
total_profit = df_split.groupby('Region')['Profit'].sum().reset_index()
result = total_profit.loc[total_profit['Profit'].idxmax()]['Region']

```


* **Computed Result:** `South`
* **Answer:** The region that recorded the highest total profit is **South**.

---

### Q3: "What is the total revenue per Product Category?"

* **Executed Code:**
```python
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Sales_Amount'] = df_split['Sales_Amount'].astype(float)
result = df_split.groupby('Product_Category')['Sales_Amount'].sum()

```


* **Computed Result:**
```text
Product_Category
Clothing       1600.0
Electronics    8200.5
Furniture      3070.0
Name: Sales_Amount, dtype: float64

```


* **Answer:** The total revenue per Product Category is as follows: **Clothing ($1600.0)**, **Electronics ($8200.5)**, and **Furniture ($3070.0)**.

---

### Q4: "How many total units were sold?"

* **Executed Code:**
```python
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Units_Sold'] = df_split['Units_Sold'].astype(int)
result = df_split['Units_Sold'].sum()

```


* **Computed Result:** `64`
* **Answer:** The total units sold is **64**, as calculated from the 'Units_Sold' column in the dataframe.

---

### Q5: "What is the average profit per transaction?"

* **Executed Code:**
```python
import pandas as pd
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Profit'] = pd.to_numeric(df_split['Profit'])
result = df_split['Profit'].mean()

```


* **Computed Result:** `311.0`
* **Answer:** The average profit per transaction is **$311.0**.

---

### Q6: "Which product category sold the most units in the West region?"

* **Executed Code:**
```python
df = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df['Units_Sold'] = df['Units_Sold'].astype(int)
west_region_df = df[df['Region'] == 'West']
if not west_region_df.empty:
    product_category_units_sold = west_region_df.groupby('Product_Category')['Units_Sold'].sum().reset_index()
    result = product_category_units_sold.loc[product_category_units_sold['Units_Sold'].idxmax()]['Product_Category']
else:
    result = "No data available for the West region"

```


* **Computed Result:** `Clothing`
* **Answer:** The product category that sold the most units in the West region is **Clothing**.

---

### Q7: "List all transactions where Sales Amount exceeded $1500."

* **Executed Code:**
```python
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Sales_Amount'] = df_split['Sales_Amount'].astype(float)
result = df_split[df_split['Sales_Amount'] > 1500]

```


* **Computed Result:**
```text
  Transaction_ID        Date Region Product_Category  Sales_Amount Units_Sold  Profit
2         TX1003  2025-02-02   East      Electronics        2100.0          7  550.00
5         TX1006  2025-03-01  South      Electronics        3100.0          9  800.00
8         TX1009  2025-03-20  North      Electronics        1800.0          5  450.00

```


* **Answer:** The transactions where the Sales Amount exceeded $1500 are **TX1003**, **TX1006**, and **TX1009** ($2100.0, $3100.0, and $1800.0 respectively).

---

### Q8: "What was the total profit for the month of March 2025?"

* **Executed Code:**
```python
import pandas as pd
df_split = df['Transaction_ID,Date,Region,Product_Category,Sales_Amount,Units_Sold,Profit'].str.split(',', expand=True)
df_split.columns = ['Transaction_ID', 'Date', 'Region', 'Product_Category', 'Sales_Amount', 'Units_Sold', 'Profit']
df_split['Date'] = pd.to_datetime(df_split['Date'])
df_split['Profit'] = pd.to_numeric(df_split['Profit'])
df_march_2025 = df_split[(df_split['Date'].dt.month == 3) & (df_split['Date'].dt.year == 2025)]
result = df_march_2025['Profit'].sum()

```


* **Computed Result:** `1740.0`
* **Answer:** The total profit for the month of March 2025 is **$1740.0**.

---

## Design Tradeoffs & Future Enhancements

| Feature Choice | Advantage | Tradeoff / Limitation |
| --- | --- | --- |
| **Code Execution vs. Direct Prompting** | 100% mathematical accuracy; zero numerical hallucination. | Requires runtime syntax checking and error handling. |
| **Groq (Llama-3.3-70B)** | Sub-second latency; free tier access. | Free API rate limits under heavy batch load. |
| **CLI / Terminal Interactive Loop** | Zero port/browser dependencies; fast testing for reviewers. | Lacks visual chart plotting (can be extended using `matplotlib`). |

```

---
