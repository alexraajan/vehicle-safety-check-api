import entity
import re
from logger_config import setup_logger

logger = setup_logger(__name__)

class VehicleService:
    def __init__(self, repo):
        self.repo = repo

    def vehicle_details(self, details):
        try:
            vehicle_no = details.get('vehicle_no')
            no_of_safety_check = details.get('no_of_safety_check')
            is_completed = details.get('isCompleted')

            # Validate vehicle_no using RegExp
            pattern = re.compile(r'^[A-Z0-9\- ]{5,10}$')
            if not pattern.match(vehicle_no):
                raise ValueError("Invalid vehicle number. It must be 5–10 characters long and contain only A-Z, 0–9, hyphen, or space.")

            vehicle = entity.Vehicle(vehicle_no, no_of_safety_check, is_completed)
            logger.info("Creating vehicle: vehicle_no=%s, no_of_safety_check=%s, isCompleted=%s",
                        vehicle.vehicle_no, vehicle.no_of_safety_check, vehicle.isCompleted)
            self.repo.insert_vehicle(vehicle)
        except Exception as e:
            logger.error("Error in vehicle_details(): %s", str(e))
            raise

    def get_all_vehicle_details(self, vehicle_no=None):
        try:
            if vehicle_no:
                logger.info("Fetching vehicles by number prefix: %s", vehicle_no)
                rows = self.repo.get_vehicle_by_number(vehicle_no)
                return [entity.Vehicle(*row) for row in rows] if rows else []
            else:
                logger.info("Fetching all vehicles")
                rows = self.repo.get_all_vehicles()
                return [entity.Vehicle(*row) for row in rows] if rows else []
        except Exception as e:
            logger.error("Error in get_all_vehicle_details(): %s", str(e))
            raise


    def update_vehicle_details(self, vehicle):
        try:
            logger.info("Updating vehicle: vehicle_no=%s", vehicle.vehicle_no)
            result = self.repo.update_vehicle(vehicle)
            if result:
                logger.info("Update successful for vehicle: %s", vehicle.vehicle_no)
            else:
                logger.warning("Update failed: vehicle not found - %s", vehicle.vehicle_no)
            return result
        except Exception as e:
            logger.error("Error in update_vehicle_details(): %s", str(e))
            raise

    def delete_vehicle(self, vehicle_no):
        try:
            logger.info("Deleting vehicle: %s", vehicle_no)
            result = self.repo.delete_vehicle(vehicle_no)
            if result:
                logger.info("Delete successful: %s", vehicle_no)
            else:
                logger.warning("Delete failed: vehicle not found - %s", vehicle_no)
            return result
        except Exception as e:
            logger.error("Error in delete_vehicle(): %s", str(e))
            raise
