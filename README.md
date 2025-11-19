# Platia360

**Platia360** is a custom ERPNext / Frappe application designed for **real estate management**. It provides real‑estate–specific functionality built on top of ERPNext, helping property managers, brokers, and developers manage assets, leases, tenants, and more.

## Features

- Property listing and management  
- Lease / rental contract management  
- Tenant onboarding and communications  
- Maintenance request tracking  
- Financials (rent, security deposit, payments)  
- Custom dashboards and reports tailored for real estate  
- Integration with ERPNext’s core modules (Accounts, CRM, etc.)

## Requirements

- Frappe / ERPNext (version compatible with your app)  
- Python (as required by Frappe)  
- Bench (Frappe’s CLI tool) :contentReference[oaicite:0]{index=0}  
- Redis, MariaDB / Postgres, Node.js, Yarn (as per Frappe / ERPNext setup) :contentReference[oaicite:1]{index=1}  

## Installation

Here’s how to install **Platia360** in a Frappe / ERPNext environment.

1. **Clone or download this app**

   ```bash
   cd /path/to/your/frappe-bench/apps
   git clone https://github.com/iammusabutt/platia360.git

2. **Install the app on your site**

   ```bash
   cd /path/to/your/frappe-bench
   bench --site your-site-name install-app platia360

3. **Build and migrate (if necessary)**

   ```bash
   bench build
   bench --site your-site-name migrate

4. **Start the bench**

   ```bash
   bench start

5. **Enable developer mode (optional but recommended for development)**

   ```bash
   {
      "developer_mode": 1
   }


