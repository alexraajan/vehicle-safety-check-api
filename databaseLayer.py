from entity import Vehicle
from logger_config import setup_logger

logger = setup_logger(__name__)

class VehicleRepository:
    def __init__(self, db_context):
        self.db_context = db_context

    def insert_vehicle(self, vehicle):
        conn = None
        cursor = None
        try:
            conn = self.db_context.get_connection()
            cursor = conn.cursor()

            logger.info("Checking if vehicle exists: %s", vehicle.vehicle_no)
            cursor.execute("SELECT COUNT(*) FROM VehicleDetails WHERE vehicle_no = ?", (vehicle.vehicle_no,))
            if cursor.fetchone()[0] > 0:
                logger.warning("Insert failed - Vehicle already exists: %s", vehicle.vehicle_no)
                raise Exception("Vehicle already exists")

            query = """
                INSERT INTO VehicleDetails (vehicle_no, no_of_safety_check, isCompleted)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (vehicle.vehicle_no, vehicle.no_of_safety_check, vehicle.isCompleted))
            conn.commit()
            logger.info("Vehicle inserted: %s", vehicle.vehicle_no)

        except Exception as e:
            logger.error("Error inserting vehicle %s: %s", vehicle.vehicle_no, str(e))
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            logger.debug("DB connection closed after insert")

    def get_all_vehicles(self):
        conn = None
        cursor = None
        try:
            conn = self.db_context.get_connection()
            cursor = conn.cursor()
            logger.info("Fetching all vehicles")
            cursor.execute("SELECT * FROM VehicleDetails")
            rows = cursor.fetchall()
            logger.info("Fetched %d vehicles", len(rows))
            return rows
        except Exception as e:
            logger.error("Error fetching all vehicles: %s", str(e))
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            logger.debug("DB connection closed after fetch all")

    def get_vehicle_by_number(self, vehicle_no):
        conn = None
        cursor = None
        try:
            conn = self.db_context.get_connection()
            cursor = conn.cursor()
            logger.info("Fetching vehicle by number: %s", vehicle_no)
            cursor.execute("SELECT * FROM VehicleDetails WHERE vehicle_no = ?", (vehicle_no,))
            row = cursor.fetchone()
            if row:
                logger.info("Vehicle found: %s", vehicle_no)
            else:
                logger.warning("Vehicle not found: %s", vehicle_no)
            return row
        except Exception as e:
            logger.error("Error fetching vehicle %s: %s", vehicle_no, str(e))
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            logger.debug("DB connection closed after fetch by number")

    def update_vehicle(self, vehicle):
        conn = None
        cursor = None
        try:
            conn = self.db_context.get_connection()
            cursor = conn.cursor()
            logger.info("Updating vehicle: %s", vehicle.vehicle_no)
            cursor.execute("""
                SET NOCOUNT OFF;
                UPDATE VehicleDetails
                SET no_of_safety_check = ?, isCompleted = ?
                WHERE vehicle_no = ?
            """, (vehicle.no_of_safety_check, vehicle.isCompleted, vehicle.vehicle_no))
            conn.commit()
            updated = cursor.rowcount
            if updated > 0:
                logger.info("Vehicle updated: %s", vehicle.vehicle_no)
            else:
                logger.warning("Update failed - vehicle not found: %s", vehicle.vehicle_no)
            return updated > 0
        except Exception as e:
            logger.error("Error updating vehicle %s: %s", vehicle.vehicle_no, str(e))
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            logger.debug("DB connection closed after update")

    def delete_vehicle(self, vehicle_no):
        conn = None
        cursor = None
        try:
            conn = self.db_context.get_connection()
            cursor = conn.cursor()
            logger.info("Deleting vehicle: %s", vehicle_no)
            cursor.execute("DELETE FROM VehicleDetails WHERE vehicle_no = ?", (vehicle_no,))
            conn.commit()
            deleted = cursor.rowcount
            if deleted > 0:
                logger.info("Vehicle deleted: %s", vehicle_no)
            else:
                logger.warning("Delete failed - vehicle not found: %s", vehicle_no)
            return deleted > 0
        except Exception as e:
            logger.error("Error deleting vehicle %s: %s", vehicle_no, str(e))
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            logger.debug("DB connection closed after delete")
