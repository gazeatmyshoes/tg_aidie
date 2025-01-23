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
            logger.info("Начало инициализации базы данных Firebase")
            
            # Создаем базовые пути, если их нет
            root_ref = db.reference('/')
            data = root_ref.get()
            
            if not data:
                logger.info("Инициализация базовой структуры базы данных")
                initial_data = {
                    'diary': {},
                    'goals': {},
                    'metadata': {
                        'created_at': datetime.now().isoformat(),
                        'version': '1.0'
                    }
                }
                root_ref.set(initial_data)
            
            # Создаем правила для индексации
            logger.info("Настройка правил базы данных")
            rules = {
                "rules": {
                    ".read": "auth != null",
                    ".write": "auth != null",
                    "diary": {
                        "$user_id": {
                            ".read": "auth != null",
                            ".write": "auth != null",
                            ".indexOn": ["timestamp"],
                            "$entry_id": {
                                ".validate": "newData.hasChildren(['text', 'timestamp', 'sentiment_score', 'sentiment_magnitude'])"
                            }
                        }
                    },
                    "goals": {
                        "$user_id": {
                            ".read": "auth != null",
                            ".write": "auth != null",
                            ".indexOn": ["created_at", "completed"],
                            "$goal_id": {
                                ".validate": "newData.hasChildren(['text', 'created_at', 'completed'])"
                            }
                        }
                    }
                }
            }
            
            # Применяем правила
            logger.info("Применение правил базы данных")
            try:
                root_ref.set_rules(rules)
                logger.info("Правила базы данных успешно обновлены")
            except Exception as rules_error:
                logger.warning(f"Не удалось обновить правила базы данных: {str(rules_error)}")
                logger.info("Продолжаем работу с существующими правилами")
            
            # Проверяем подключение
            test_ref = db.reference('test')
            test_ref.set({'test': True})
            test_ref.delete()
            
            logger.info("База данных успешно инициализирована")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {str(e)}", exc_info=True)
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