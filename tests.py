from django.test import TestCase
from datetime import date, timedelta
from tasks.scoring import calculate_priority


class PriorityScoringTests(TestCase):

    def test_overdue_task_gets_higher_score(self):
        task = {
            "due_date": date.today() - timedelta(days=1),
            "importance": 5,
            "estimated_hours": 3,
            "dependencies": []
        }
        score = calculate_priority(task)
        self.assertGreater(score, 6)

    def test_high_importance_scores_more(self):
        high = {
            "due_date": date.today(),
            "importance": 9,
            "estimated_hours": 5,
            "dependencies": []
        }
        low = {
            "due_date": date.today(),
            "importance": 2,
            "estimated_hours": 5,
            "dependencies": []
        }
        self.assertGreater(
            calculate_priority(high),
            calculate_priority(low)
        )

    def test_dependencies_increase_priority(self):
        task = {
            "due_date": date.today(),
            "importance": 5,
            "estimated_hours": 2,
            "dependencies": ["1", "2"]
        }
        score = calculate_priority(task)
        self.assertGreater(score, 4)
