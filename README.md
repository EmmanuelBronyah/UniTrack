# UniTrack

UniTrack is a python-based desktop application that records, manages and generates reports on employee uniform deductions.

## Features

* Secure Authentication (Login/Logout)
* Import employee deductions from Excel files
* Export all records or filtered records of employee deductions to Excel
* Add standalone deductions for employees
* Auto-calculated outstanding amounts and balances
* Search employee records by name or service number
* Backup management and user account controls

## Requirements

* Python 3.10+
* PySide6
* SQLAlchemy
* Alembic
* Pandas
* Pyinstaller
* (other dependencies listed in `requirements.txt`)

## Installation

### 1. Clone project

  ```bash
  git clone https://github.com/EmmanuelBronyah/UniTrack.git
  ```

### 2. Navigate into project root
  
  ```bash
  cd UniTrack
  ```

### 3. Activate virtual environment
  
  ```bash
  source venv/Scripts/activate
  ```

### 4. Install dependencies
  
  ```bash
  pip install -r requirements.txt
  ```

### 5. Run application
  
  ```bash
  python -m src.main
  ```

### Building an executable

To generate a standalone `.exe` using PyInstaller:
  
  ```bash
  pyinstaller main.spec
  ```

After the build completes, the executable will be located at:

```bash
./dist/UniTrack
```
  
## Visuals (Usage Demonstration)

### Splash screen → Login → Dashboard

* Default credentials
  * Username: `admin`
  * Password: `010101`

![Splash → Login → Dashboard](assets/video/splashscreen%20to%20login.gif)

### Adding a Deduction to an Existing Employee Record
  
![Adding a deduction](assets/video/add%20record.gif)

### Importing & Exporting Records

* A sample Excel file (`test_employees.xlsx`) containing 6000 rows of dummy employee records is located in the project root for testing import and export functionality.
  
![Input/Export](assets/video/import%20export.gif)

### Searching Employee Records

![Search operation](assets/video/search%20and%20record%20update.gif)

### Exporting Filtered Results

![Filtered export](assets/video/filtered%20exports.gif)

### Database Backup, Logout, and Editing User Credentials
  
![Backup, logout, user updates](assets/video/backup%20database,%20logout%20and%20update%20user%20credentials.gif)

## Know Issues

* When a deduction record is added using the add record button and is saved, adding a subsequent deduction record to the same employee without closing and re-opening the add record window will result in an auto-calculated outstanding amount that is generated based on the outstanding amount used for the initial deduction record added.

## License

This project is distributed under a proprietary license.
See the **LICENSE** file for full details.

## Contact Information

For more enquires, support or feedback, please contact:

* Email: <emmanuelbronyah7@gmail.com>
