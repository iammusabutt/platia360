# Platia360

**Platia360** is a custom ERPNext / Frappe application designed for **real estate service management**. It provides real‑estate–specific functionality built on top of ERPNext, helping property managers, brokers, and developers manage assets, maintenance, tenants, and more.


## Requirements

- ERPNext v15 (version compatible with your app)

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

## Usage

- Once installed, access the **Platia360** module from your ERPNext desk.
