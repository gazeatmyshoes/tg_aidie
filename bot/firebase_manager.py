import logging
from datetime import datetime
from firebase_admin import db
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class FirebaseManager:
    @staticmethod
    def init_database():
        """Инициализация базы данных и создание необходимых индексов"""
        try:
            # Создаем правила для индексации
            rules = {
                "rules": {
                    "diary": {
                        "$user_id": {
                            ".indexOn": ["timestamp"]
                        }
                    },
                    "goals": {
                        "$user_id": {
                            ".indexOn": ["created_at", "completed"]
                        }
                    }
                }
            }
            
            # Применяем правила
            db.reference('/').set_rules(rules)
            logger.info("Firebase rules updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            return False

    @staticmethod
    def save_diary_entry(user_id: int, text: str, sentiment_score: float, 
                        sentiment_magnitude: float) -> bool:
        """Сохранение записи в дневник"""
        try:
            ref = db.reference(f'diary/{user_id}')
            entry = {
                'text': text,
                'timestamp': datetime.now().isoformat(),
                'sentiment_score': sentiment_score,
                'sentiment_magnitude': sentiment_magnitude
            }
            ref.push(entry)
            return True
        except Exception as e:
            logger.error(f"Error saving diary entry: {str(e)}")
            return False

    @staticmethod
    def add_goal(user_id: int, text: str) -> bool:
        """Добавление новой цели"""
        try:
            ref = db.reference(f'goals/{user_id}')
            goal = {
                'text': text,
                'created_at': datetime.now().isoformat(),
                'completed': False
            }
            ref.push(goal)
            return True
        except Exception as e:
            logger.error(f"Error adding goal: {str(e)}")
            return False

    @staticmethod
    def get_goals(user_id: int) -> List[Dict]:
        """Получение списка целей пользователя"""
        try:
            ref = db.reference(f'goals/{user_id}')
            goals = ref.get()
            if goals:
                return [
                    {
                        'id': goal_id,
                        'text': goal['text'],
                        'completed': goal.get('completed', False),
                        'created_at': goal.get('created_at')
                    }
                    for goal_id, goal in goals.items()
                ]
            return []
        except Exception as e:
            logger.error(f"Error getting goals: {str(e)}")
            return []

    @staticmethod
    def toggle_goal(user_id: int, goal_id: str) -> bool:
        """Переключение статуса цели"""
        try:
            ref = db.reference(f'goals/{user_id}/{goal_id}')
            goal = ref.get()
            if goal:
                goal['completed'] = not goal.get('completed', False)
                ref.update(goal)
                return True
            return False
        except Exception as e:
            logger.error(f"Error toggling goal: {str(e)}")
            return False

    @staticmethod
    def get_mood_history(user_id: int, limit: int = 7) -> Optional[List[Dict]]:
        """Получение истории настроения"""
        try:
            ref = db.reference(f'diary/{user_id}')
            entries = ref.order_by_child('timestamp').limit_to_last(limit).get()
            if entries:
                return [
                    {
                        'timestamp': entry['timestamp'],
                        'sentiment_score': entry['sentiment_score'],
                        'sentiment_magnitude': entry['sentiment_magnitude']
                    }
                    for entry in entries.values()
                ]
            return None
        except Exception as e:
            logger.error(f"Error getting mood history: {str(e)}")
            return None