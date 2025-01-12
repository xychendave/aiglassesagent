from datetime import datetime
from typing import Dict, List
from .models import FoodItem, NavigationAlert

# In-memory database
class Database:
    def __init__(self):
        self.food_items: Dict[str, List[FoodItem]] = {}  # user_id -> food items
        self.navigation_history: Dict[str, List[NavigationAlert]] = {}  # user_id -> navigation alerts

    def add_food_item(self, user_id: str, food_item: FoodItem):
        if user_id not in self.food_items:
            self.food_items[user_id] = []
        self.food_items[user_id].append(food_item)
    
    def get_food_items(self, user_id: str) -> List[FoodItem]:
        return self.food_items.get(user_id, [])

    def add_navigation_alert(self, user_id: str, alert: NavigationAlert):
        if user_id not in self.navigation_history:
            self.navigation_history[user_id] = []
        self.navigation_history[user_id].append(alert)
    
    def get_navigation_history(self, user_id: str) -> List[NavigationAlert]:
        return self.navigation_history.get(user_id, [])

# Global database instance
db = Database()
