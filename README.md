# 🚚 Smart Logistics Management & Analytics Platform

A centralized data analytics system that consolidates 70,000+ shipment records from logistics operations into a MySQL/MariaDB database and visualizes insights through an interactive Streamlit dashboard for real-time decision-making.

---

## 📌 Project Overview

This capstone project builds an end-to-end logistics analytics pipeline:

1. **Data Extraction** — Load raw CSV/JSON datasets using Python & pandas
2. **Database Design** — Normalized MySQL schema (3NF) with 9 tables
3. **Data Loading** — Insert 70,000+ records into MariaDB using Python
4. **Analytics** — SQL queries for KPIs and analytical views
5. **Dashboard** — Interactive Streamlit app with charts and filters

---

## 🗂️ Project Structure

```
logistics/
├── data/                   # Raw dataset files (not committed to GitHub)
│   ├── shipments.json
│   ├── shipment_tracking.csv
│   ├── courier_staff.csv
│   ├── routes.csv
│   ├── warehouses.json
│   └── costs.csv
├── app.py                  # Streamlit dashboard
├── db.py                   # Database query functions
├── ddl.sql                 # Database schema (CREATE statements)
├── dml_lookups.sql         # Lookup table seed data (INSERT statements)
├── explore_data.py         # Data exploration using pandas
├── load_data.py            # Data loading script (CSV/JSON → MariaDB)
├── queries.sql             # All SQL queries (KPIs + analytical views)
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Core programming language |
| pandas | Data reading and manipulation |
| MariaDB / MySQL | Relational database |
| mysql-connector-python | Python to database connection |
| Streamlit | Interactive web dashboard |
| Plotly | Charts and visualizations |

---

## 🗃️ Database Schema

The database `logistics_db` contains 9 tables following **3NF normalization**:

**Lookup Tables:**
- `shipment_statuses` — Delivered, Cancelled, In Transit, Pending
- `tracking_statuses` — Order Placed, Picked Up, In Transit, Out for Delivery, Delivered, Cancelled
- `vehicle_types` — Car, Van, Truck, Bike

**Core Tables:**
- `shipments` — 70,000 shipment records
- `shipment_tracking` — 209,570 tracking events
- `courier_staff` — 1,000 couriers
- `routes` — 500 routes
- `warehouses` — 50 warehouses
- `costs` — Cost breakdown per shipment

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/prabhulakshminarayanan/logistics.git
cd logistics
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install pandas mysql-connector-python streamlit plotly
```

### 4. Set up the database
Make sure MariaDB/MySQL is running, then:
```bash
mysql -u root -p -h 127.0.0.1 < ddl.sql
mysql -u root -p -h 127.0.0.1 < dml_lookups.sql
```

### 5. Add dataset files
Place the following files inside the `data/` folder:
- `shipments.json`
- `shipment_tracking.csv`
- `courier_staff.csv`
- `routes.csv`
- `warehouses.json`
- `costs.csv`

### 6. Load data into the database
```bash
python load_data.py
```

### 7. Run the dashboard
```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📊 Dashboard Features

### Search & Filter (Sidebar)
- Search by Shipment ID
- Filter by Status, Origin, Destination, Courier
- Filter by Date Range

### KPIs
- Total Shipments
- Delivery Percentage
- Cancellation Percentage
- Average Delivery Time (days)
- Total Operational Cost

### Analytical Views

| Tab | What it shows |
|---|---|
| 🚀 Delivery Performance | Monthly trends, most delayed routes, delivery time vs distance |
| 👤 Courier Performance | Shipment volume, delivery rate, rating comparison |
| 💰 Cost Analytics | Cost breakdown by status, fuel vs labour, high-cost shipments, route costs |
| ❌ Cancellation Analysis | Cancellations by origin city, by courier, time-to-cancellation |
| 🏭 Warehouse Insights | Capacity comparison, capacity share, high-traffic warehouses |

---

## 📁 Dataset

The dataset contains 6 files with 70,000+ logistics records.  
Download from: [Google Drive — Logistics Dataset](https://drive.google.com/drive/folders/1quR-EsaUUel_AAg6zKMHMvDUs8yX6PYU?usp=sharing)

---

## 👤 Author

**Prabhu Lakshminarayanan**  
GitHub: [@prabhulakshminarayanan](https://github.com/prabhulakshminarayanan)
