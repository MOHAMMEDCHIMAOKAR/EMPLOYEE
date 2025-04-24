# Employee Management System

A modern desktop application built with Python and Tkinter for comprehensive employee management with secure database integration.

## Features

### User Authentication
- Multi-level user access (Admin/HR)
- Secure login system
- Custom designed welcome page
- Role-based access control

### Employee Management
- Add new employees with detailed information
- Remove employees with data cleanup
- Promote/Update employee details
- Advanced search functionality
- Email integration with one-click email opening

### Database Operations
- Secure MySQL integration
- Real-time data updates
- Auto-increment ID management
- Data validation and sanitization
- Transaction management

### Advanced UI Features
- Responsive design scaling
- Modern themed interface
- Interactive data grid
- Sortable columns
- Filter and search capabilities
- Email clickability

## Technology Stack

- **Frontend**: Tkinter with custom styling
- **Backend**: Python 3.x
- **Database**: MySQL
- **Additional Libraries**: 
  - mysql-connector-python
  - PIL (Python Imaging Library)
  - pathlib
  - webbrowser

## Prerequisites

1. Python 3.x
2. MySQL Server
3. Required packages:
```bash
pip install mysql-connector-python Pillow
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
    salary DECIMAL(10,2),
    email VARCHAR(100)
);
```

3. Configure database connection
Edit `employee.py`:
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

### Login Credentials
- **Admin Access**
  - Username: admin
  - Password: admin123
- **HR Access**
  - Username: hr
  - Password: hr123

### Main Features
1. **Employee Management**
   - Add new employees
   - Update employee information
   - Remove employees
   - Search and filter records

2. **Data Operations**
   - Sort by any column
   - Filter by department
   - Export employee data
   - Email integration

3. **System Features**
   - Real-time updates
   - Data validation
   - Secure access control
   - Error handling

## Project Structure
```
employee-management/
│
├── employee.py        # Main application
├── database.sql      # Database schema
├── README.md        # Documentation
├── requirements.txt  # Dependencies
└── assets/          # UI resources
    ├── frame0/      # Welcome screen
    ├── frame1/      # Login interface
    └── frame3/      # Main dashboard
```

## Security Features
- Password-protected access
- Role-based permissions
- Database connection encryption
- Input validation
- Error handling

## Error Handling
- Database connection errors
- Invalid input validation
- Authentication failures
- File operation errors

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments
- Modern UI design implementation
- Secure database practices
- Python best practices
- Tkinter optimization techniques