import json
import os

def get_db_connection_string():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'env_parameters.json')
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        environment = config_data['environment']
        connection_string = config_data[environment]['DbConnectionString']
        return connection_string
    except KeyError:
        raise ValueError("Environment key not found or incorrect environment specified.")
    except FileNotFoundError:
        raise FileNotFoundError("The JSON file was not found.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")