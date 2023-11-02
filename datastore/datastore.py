import json
from typing import Dict, Optional

from fastapi import HTTPException


class DataStore:
    def __init__(self):
        self.data_file = "data.json"
        self.data = self.load_data_from_file()

    def load_data_from_file(self) -> Dict[str, str]:
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data_to_file(self):
        with open(self.data_file, "w") as file:
            json.dump(self.data, file)

    def set_value(self, key: str, value: str):
        if key in self.data:
            raise HTTPException(status_code=400, detail="The key already exists")
        self.data[key] = value
        self.save_data_to_file()

    def get_value(self, key: str) -> Optional[str]:
        return self.data.get(key)

    def delete_value(self, key: str):
        if key in self.data:
            del self.data[key]
            self.save_data_to_file()
        else:
            raise HTTPException(status_code=404, detail="The key does not exis")

    def find_keys(self, value: str) -> list:
        keys = [key for key, val in self.data.items() if val == value]
        return keys


data_store = DataStore()
