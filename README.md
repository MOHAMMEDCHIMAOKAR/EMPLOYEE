# Employee Management System

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A desktop **Employee Management System** built with **Python, Tkinter, and MySQL**. It provides a role-based, image-rich GUI (Welcome → Login → Dashboard) for managing employee records — adding, removing, promoting, searching, and filtering staff — backed by a relational database.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Default Login Credentials](#default-login-credentials)
- [Role-Based Access](#role-based-access)
- [Database Schema](#database-schema)
- [Application Flow](#application-flow)
- [Known Limitations](#known-limitations)
- [Suggested Enhancements](#suggested-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This application walks a user through three screens:

1. **Welcome Page** – a full-screen splash screen with branding and a "Continue" button.
2. **Login Page** – authenticates the user and routes them to a role-specific dashboard.
3. **Employee Dashboard** – a data-grid view of all employees with actions to add, remove, promote, search, and filter/sort records, all backed by a live MySQL connection.

All screens are built as hand-tuned Tkinter `Canvas` layouts (originally exported from a design tool) and have been adapted to scale responsively to the user's screen resolution, with `Pillow`-based image resizing and graceful fallbacks (plain buttons/text) if an image asset fails to load.

---

## Project Timeline

| Milestone | Details |
|-----------|---------|
| **Academic Year** | **2023–24** |
| **Project Type** | College Academic Project |
| **Institution** | Developed as part of an academic coursework project during the 2023–24 academic year. |
| **Technology Focus** | Python, Tkinter, MySQL, Desktop Application Development |
| **Current Status** | Repository maintained with improved documentation, MIT licensing, and minor maintenance updates while preserving the original project implementation. |

> **Project History**
>
> This Employee Management System was originally developed as a **college academic project during the 2023–24 academic year** to demonstrate desktop application development concepts using **Python**, **Tkinter**, and **MySQL**. The repository has since been professionally documented and maintained for portfolio purposes, while intentionally preserving the original application architecture and implementation.

---

## Features

**Authentication & Access Control**
- Simple username/password login gate.
- Two roles — `admin` and `hr` — each rendering a different set of dashboard actions.

**Employee Records Management**
- **Add Employee** — form dialog for name, post, and salary.
- **Remove Employee** — deletes the selected row and re-normalizes the table's `AUTO_INCREMENT` counter to the next available ID.
- **Promote Employee** — partial update dialog; you can update post, salary, or both for the selected employee.
- **Search Employee** — instant lookup by Employee ID.
- **Filter & Sort** — filter by post and salary bracket, then sort by ID/name/post/salary in ascending or descending order.

**Data Grid**
- A `ttk.Treeview` table listing Employee ID, Name, Post, and Salary, refreshed after every operation.

**Resilient UI**
- Screen-size–aware layout scaling for different monitor resolutions.
- Try/except guards around image loading and database calls, with user-facing error dialogs instead of silent crashes.

## Tech Stack

| Layer            | Technology                                   |
|------------------|-----------------------------------------------|
| GUI              | Python `tkinter` + `ttk` (Canvas-based layout) |
| Image handling   | `Pillow` (PIL) for resizing/scaling assets     |
| Database         | MySQL 8.x                                      |
| DB Driver        | `mysql-connector-python`                       |
| Language         | Python 3.8+                                    |

## Project Structure

```
EMPLOYEE/
├── Final.py               # Main application (entry point)
├── requirements.txt        # Python dependencies
├── query.txt                # Note on importing the SQL dump
├── database/
│   └── database.sql        # Schema + seed data for the `emp` database
└── assets/
    ├── a.png, b.png, c.png  # Logo / icon assets
    ├── frame0/              # Welcome page images & button
    ├── frame1/              # Login page images, button, entry fields
    └── frame3/              # Dashboard background image
```

## Prerequisites

- **Python 3.8+**
- **MySQL Server 8.x** (or compatible), running and reachable
- Tkinter support for your Python install:
  - Windows/macOS: bundled with the standard Python installer.
  - Debian/Ubuntu Linux: `sudo apt-get install python3-tk`

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/MOHAMMEDCHIMAOKAR/EMPLOYEE.git
cd EMPLOYEE

# 2. (Recommended) create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Database Setup

1. Make sure MySQL Server is running and you can log in with an account that can create databases.
2. Create the database and load the schema + seed data from `database/database.sql`:

   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS emp;"
   mysql -u root -p emp < database/database.sql
   ```

   Alternatively, from inside the MySQL shell:

   ```sql
   CREATE DATABASE IF NOT EXISTS emp;
   USE emp;
   SOURCE /full/path/to/EMPLOYEE/database/database.sql;
   ```

  
This creates a single `employees` table and populates it with 20 sample records.

## Configuration

The app connects to MySQL using `mysql.connector` in `Final.py`, reading credentials from environment variables (with fallback defaults for local development):

| Variable      | Default     | Description            |
|---------------|-------------|-------------------------|
| `DB_HOST`     | `localhost` | MySQL server host       |
| `DB_USER`     | `root`      | MySQL username          |
| `DB_PASSWORD` | `Root`      | MySQL password          |
| `DB_NAME`     | `emp`       | Database name           |

Set these before launching the app instead of relying on the defaults, e.g.:

```bash
# macOS/Linux
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=emp

# Windows (PowerShell)
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="emp"
```

## Running the Application

```bash
python Final.py
```

The window opens maximized on the Welcome screen. Click **Continue** to reach the Login screen.

## Default Login Credentials

| Role  | Username | Password |
|-------|----------|----------|
| Admin | `admin`  | `admin123` |
| HR    | `hr`     | `hr123`    |

> ⚠️ **Security note:** these credentials are hardcoded directly in `Final.py` for demonstration purposes — there is no password hashing or external user store. Change or remove them before using this project with real employee data, and consider externalizing credentials and adding proper authentication for anything beyond local/demo use.

## Role-Based Access

| Action              | Admin | HR |
|---------------------|:-----:|:--:|
| View employee list  | ✅    | ✅ |
| Search employee     | ✅    | ✅ |
| Add employee        | ✅    | ❌ |
| Remove employee     | ✅    | ❌ |
| Promote employee    | ✅    | ❌ |
| Filter & sort       | ✅    | ❌ |
| Logout              | ✅    | ✅ |

## Database Schema

`database/database.sql` defines a single table:

```sql
CREATE TABLE `employees` (
  `emp_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Seeded with 20 sample employees across four posts: Developer, Manager, HR, and Intern.

> **Note:** the schema includes an `email` column and the seed data populates it, but the current UI (add-employee form and results grid) only surfaces `emp_id`, `name`, `post`, and `salary`. New rows added through the app will have `email` left as `NULL`. See [Suggested Enhancements](#suggested-enhancements).

## Application Flow

```
WelcomePage  →  LoginPage  →  EmployeeManagementApp (role="admin" | "hr")
   (splash)      (auth)          ├─ Add Employee     (admin only)
                                  ├─ Remove Employee  (admin only)
                                  ├─ Promote Employee (admin only)
                                  ├─ Search Employee  (admin + hr)
                                  ├─ Filter & Sort    (admin only)
                                  └─ Logout → back to LoginPage
```

## Known Limitations

- **Hardcoded credentials** — login is checked against literal strings in code rather than a users table or hashed store.
- **Windows-oriented full-screen mode** — the app calls `root.state('zoomed')` to maximize the window, which is reliable on Windows but may behave inconsistently or raise an error on some macOS/Linux Tk builds.
- **No automated tests or CI** — there is currently no test suite or GitHub Actions workflow in the repository.
- **Unused `email` field** — present in the schema/seed data but not editable or displayed from the UI.
- **Single-table scope** — no audit trail, no soft deletes, and no multi-user database credentials beyond the two shared app-level roles.

## Suggested Enhancements

- Move credentials to a proper `users` table with hashed passwords.
- Surface and allow editing of the `email` field (e.g., for the "click to email" style feature hinted at in earlier project iterations).
- Add cross-platform window maximizing (e.g., detect OS and use an alternative to `zoomed` on macOS/Linux).
- Add unit tests for `DatabaseOperations` and a CI workflow.
- Add pagination or lazy loading for large employee datasets.

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE) — you're free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided the copyright notice and permission notice are retained. See the `LICENSE` file for the full text.
