# Grievance Management System

A web-based application built with Streamlit and MySQL for managing user complaints and grievances efficiently.

## Features

- **User Authentication**
  - Secure registration and login system
  - Session management
  - Password protection

- **Complaint Management**
  - Submit new complaints
  - Track complaint status
  - View complaint history
  - Update complaint resolutions
  - Automatic timestamp tracking

- **User Interface**
  - Clean and intuitive dashboard
  - Responsive design
  - Real-time updates
  - Tabular view of complaints

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the repository**
```
git clone https://github.com/BairiRohithReddy/Grievance-Management-System.git
cd grievance-management-system
```

2. **Create a virtual environment (recommended)**
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install required packages**
```
pip install -r requirements.txt
```

4. **Set up MySQL Database**
```
CREATE DATABASE Grievances;
```

## Configuration

1. Update the database connection parameters in the code:
```
host='localhost'
user='root'
password='your_password'
database='Grievances'
```

2. Create a `requirements.txt` file with the following dependencies:
```
streamlit==1.28.0
mysql-connector-python==9.2.0
pandas==2.1.1
```

## Running the Application

1. **Start MySQL Server**
   - Ensure your MySQL server is running
   - Verify database connection parameters

2. **Launch the application**
```
streamlit run grievance_app.py
```

3. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`

## Usage

1. **Registration/Login**
   - Create a new account using the registration form
   - Login with existing credentials
   - Logout option available in sidebar

2. **Submit Complaints**
   - Navigate to "Submit Complaint" tab
   - Enter complaint description
   - Submit and receive complaint ID

3. **View Complaints**
   - Access "View Complaints" tab
   - See all submitted complaints in tabular format
   - Track status and resolution

4. **Update Complaints**
   - Use "Update Complaint" tab
   - Select complaint by ID
   - Add resolution description
   - Update status

## Database Schema

### Users Table
```
CREATE TABLE USERS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(25) NOT NULL
)
```

### Complaints Table
```
CREATE TABLE COMPLAINTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description TEXT,
    status VARCHAR(25),
    created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_desc VARCHAR(255) DEFAULT "Not Available",
    resolved_At TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```


## Future Enhancements

- Email notifications
- Admin dashboard
- Advanced search functionality
- File attachment support
- Analytics dashboard
- Export functionality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
