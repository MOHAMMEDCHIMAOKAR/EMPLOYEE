# Employee Management System

A desktop application built with Python and Tkinter that provides a complete employee management solution with database integration.

## Features

### User Authentication
- Secure login system
- Admin credentials required
- Welcome page with modern UI

### Employee Management
- Add new employees
- Remove existing employees
- Promote employees
- Search employee records
- Filter and sort capabilities

### Database Operations
- MySQL database integration
- Secure data storage
- Real-time data updates
- Auto-increment ID management

### User Interface
- Modern and intuitive GUI
- Responsive design
- Easy navigation
- Form validation

## Technology Stack

- **Frontend**: Tkinter (Python GUI Library)
- **Backend**: Python 3.x
- **Database**: MySQL
- **Additional Libraries**: 
  - mysql-connector-python
  - pathlib

## Prerequisites

1. Python 3.x
2. MySQL Server
3. Required Python packages:
```bash
pip install mysql-connector-python
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/employee-management.git
```

2. Set up the MySQL database
```sql
CREATE DATABASE emp;
USE emp;

CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    post VARCHAR(100),
    salary DECIMAL(10,2)
);
```

3. Configure database connection
- Update database credentials in `employee.py`:
```python
host="localhost"
user="your_username"
password="your_password"
database="emp"
```

4. Run the application
```bash
python employee.py
```

## Usage

1. **Login**
   - Username: admin
   - Password: admin123

2. **Employee Operations**
   - Add Employee: Enter employee details and save
   - Remove Employee: Select employee and confirm deletion
   - Promote Employee: Update position and salary
   - Search: Find employees by ID

3. **Data Management**
   - Sort by: ID, Name, Post, or Salary
   - Filter by: Position
   - View all employees in tabular format

## Project Structure
```
employee-management/
│
├── employee.py        # Main application file
├── database.sql      # Database schema
├── README.md        # Documentation
└── assets/          # UI assets and images
    └── frame0/      # Welcome page assets
    └── frame1/      # Login page assets
    └── frame3/      # Main app assets
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)