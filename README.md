

# Vehicle Safety Check API

This is the **backend API** for the Vehicle Safety Check application, built using Python and Flask. It provides RESTful endpoints to perform Create, Read, Update, and Delete (CRUD) operations on vehicle safety records.

Looking for the frontend? Check out the [Flutter app here](https://github.com/alexraajan/vehicle-safety-check-flutter)

---

Features

- Add new vehicle safety records
- Fetch a single or all vehicle records
- Update vehicle safety check status
- Delete vehicle records
- Swagger documentation (Auto-generated)
  Unit tests with `unittest`
- MSSQL Database integration
- Dependency Injection (for clean architecture)

---

Tech Stack

- Python 3.11+
- Flask
- SQL Server (MSSQL)
- PyODBC
- Flasgger (Swagger UI)
- unittest

---

Project Structure

```plaintext
project_API/
├── app.py                  # Main Flask application
├── businessLayer.py        # Business logic layer
├── databaseLayer.py        # Database operations layer
├── entity.py               # Entity class for Vehicle
├── env_parameters.json     # Environment configuration
├── tests/
│   └── test_app.py         # Unit tests for all endpoints

---

### Unit Testing


python -m unittest tests/test_app.py
Sample test coverage includes:
test_1_post_vehicle_success
test_1_post_vehicle_conflict
test_2_get_specific_vehicle_found
test_2_get_specific_vehicle_not_found
test_3_update_vehicle_success
test_3_update_vehicle_fail
test_4_get_all_vehicles_success
test_4_get_all_vehicles_empty
test_5_delete_vehicle_success
test_5_delete_vehicle_not_found
test_5_delete_vehicle_missing_param

![Test Result](assets/test-result.png)


Setup Instructions
1) Clone the repository:
                      git clone https://github.com/alexraajan/vehicle-safety-check-api.git
                      cd vehicle-safety-check-api
2) Install dependencies:
                        pip install python-dotenv
                        pip install flask 
                        pip install pyodbc 
                        pip install flasgger 
                        pip install pytest
                        pip install flask-cors
3) Configure the database in env_parameters.json:
                                    {
                                      "environment": "dev",
                                      "dev": {
                                        "DbConnectionString": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALEX_LENOVO\\SQLEXPRESS;DATABASE=ProjectSG;Trusted_Connection=yes"
                                      }
                                    }
4) Run the app: python app.py

Database Setup
CREATE DATABASE ProjectSG;
USE ProjectSG;

CREATE TABLE VehicleDetails (
  vehicle_no VARCHAR(10) PRIMARY KEY,
  no_of_safety_check INT,
  isCompleted TINYINT
);

API Endpoints
All endpoints are documented via Swagger UI at: http://localhost:5000/apidocs

POST    /api/vehicle-details    Add a new vehicle
GET 	  /api/vehicle-details	  Get all / specific vehicle
PUT 	  /api/vehicle-details    Update vehicle info
DELETE	/api/vehicle-details	  Delete a vehicle
Swagger UI Screenshot:
![Swagger UI](https://raw.githubusercontent.com/alexraajan/vehicle-safety-check-api/main/assets/swagger-ui.png)

![Swagger UI](assets/swagger-ui.png)
<img width="950" alt="image" src="https://github.com/user-attachments/assets/b63e497d-6456-4c00-844e-7d57f70ef4c0" />

Architecture Notes
This project follows a layered architecture with dependency injection for the database connection:
connection_string = get_db_connection_string()
db_context = DatabaseContext(connection_string)
vehicle_repo = VehicleRepository(db_context)
vehicle_service = VehicleService(vehicle_repo)

Additional Screenshots
<img width="935" alt="image" src="https://github.com/user-attachments/assets/ba146061-a9ce-4bc2-88a2-0f126f42af61" />
<img width="933" alt="image" src="https://github.com/user-attachments/assets/0757d348-a466-4d44-81a8-8394a0f3fdc0" />
<img width="935" alt="image" src="https://github.com/user-attachments/assets/dc4d217e-2be4-4253-a371-b924414ce7d8" />
<img width="933" alt="image" src="https://github.com/user-attachments/assets/23406472-2271-4a68-8181-11cc1e71aaf0" />





