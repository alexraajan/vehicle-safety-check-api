from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger

import entity
from db_context import DatabaseContext
from databaseLayer import VehicleRepository
from businessLayer import VehicleService
from config import get_db_connection_string
from logger_config import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Dependency Injection
connection_string = get_db_connection_string()
db_context = DatabaseContext(connection_string)
vehicle_repo = VehicleRepository(db_context)
vehicle_service = VehicleService(vehicle_repo)


@app.route('/api/vehicle-details', methods=['POST'])
def post_vehicle_details():
    """
    Add a new vehicle
    ---
    tags:
      - Vehicle API
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - vehicle_no
            - no_of_safety_check
            - isCompleted
          properties:
            vehicle_no:
              type: string
              example: "TEST123"
            no_of_safety_check:
              type: integer
              example: 3
            isCompleted:
              type: boolean
              example: true
    responses:
      201:
        description: Vehicle added successfully
      409:
        description: Conflict - Vehicle already exists
    """
    try:
        details = request.json
        logger.info("POST /VehicleDetails called with: %s", details)
        vehicle_service.vehicle_details(details)
        logger.info("Vehicle created successfully.")
        return jsonify({"message": "Success"}), 201
    except Exception as e:
        logger.error("POST /VehicleDetails error: %s", str(e))
        return jsonify({"error": str(e)}), 409


@app.route('/api/vehicle-details', methods=['GET'])
def get_all_vehicle_details():
    """
    Fetch vehicle(s) by vehicle number or get all
    ---
    tags:
      - Vehicle API
    parameters:
      - in: query
        name: vehicle_no
        schema:
          type: string
        required: false
        description: Vehicle number to fetch
    responses:
      200:
        description: Vehicle(s) found
      404:
        description: Vehicle not found
    """
    try:
        vehicle_no = request.args.get('vehicle_no')
        logger.info("GET /FetchAllVehicleDetails called with vehicle_no: %s", vehicle_no)
        result = vehicle_service.get_all_vehicle_details(vehicle_no)

        if result is None:
            logger.warning("Vehicle not found: %s", vehicle_no)
            return jsonify({"error": "Vehicle not found"}), 404

        if isinstance(result, list):
            logger.info("Returning all vehicles. Count: %d", len(result))
            return jsonify([v.__dict__ for v in result])
        
        logger.info("Returning vehicle: %s", result.vehicle_no)
        return jsonify(result.__dict__)
    
    except Exception as e:
        logger.error("GET /FetchAllVehicleDetails error: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/vehicle-details', methods=['PUT'])
def update_vehicle_details():
    """
    Update an existing vehicle
    ---
    tags:
      - Vehicle API
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - vehicle_no
            - no_of_safety_check
            - isCompleted
          properties:
            vehicle_no:
              type: string
              example: "TEST123"
            no_of_safety_check:
              type: integer
              example: 5
            isCompleted:
              type: boolean
              example: false
    responses:
      200:
        description: Vehicle updated successfully
      404:
        description: Vehicle not found
    """
    try:
        data = request.json
        logger.info("PUT /UpdateVehicleDetails called with: %s", data)
        vehicle = entity.Vehicle(data.get('vehicle_no'), data.get('no_of_safety_check'), data.get('isCompleted'))
        success = vehicle_service.update_vehicle_details(vehicle)

        if success:
            logger.info("Vehicle updated successfully: %s", vehicle.vehicle_no)
            return jsonify({"message": "Vehicle updated successfully"})

        logger.warning("Vehicle not found or update failed: %s", vehicle.vehicle_no)
        return jsonify({"error": "Vehicle not found or update failed"}), 404

    except Exception as e:
        logger.error("PUT /UpdateVehicleDetails error: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/vehicle-details', methods=['DELETE'])
def delete_vehicle_details():
    """
    Delete a vehicle by vehicle number
    ---
    tags:
      - Vehicle API
    parameters:
      - in: query
        name: vehicle_no
        schema:
          type: string
        required: true
        description: Vehicle number to delete
    responses:
      200:
        description: Vehicle deleted successfully
      400:
        description: Bad request (missing vehicle_no)
      404:
        description: Vehicle not found
    """
    try:
        vehicle_no = request.args.get('vehicle_no')
        if not vehicle_no:
            logger.warning("DELETE /DeleteVehicleDetails called without vehicle_no")
            return jsonify({"error": "vehicle_no query parameter is required"}), 400

        logger.info("DELETE /DeleteVehicleDetails called for: %s", vehicle_no)
        success = vehicle_service.delete_vehicle(vehicle_no)

        if success:
            logger.info("Vehicle deleted: %s", vehicle_no)
            return jsonify({"message": "Vehicle deleted successfully"})

        logger.warning("Vehicle not found or deletion failed: %s", vehicle_no)
        return jsonify({"error": "Vehicle not found or deletion failed"}), 404

    except Exception as e:
        logger.error("DELETE /DeleteVehicleDetails error: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
