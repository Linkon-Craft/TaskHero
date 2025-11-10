import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# ---- Setup Django Environment ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 🔁 change 'yourproject' to your Django project name
django.setup()

from django.contrib.auth import get_user_model
from taskhero.models import Task  # 🔁 change 'tasks' to your actual app name

User = get_user_model()

# ---- Random Data Pools ----
TASK_TITLES = [
    "Write progress report", "Fix critical bug", "Update server settings",
    "Design new landing page", "Plan team meeting", "Refactor old code",
    "Create API documentation", "Optimize database", "Test user authentication",
    "Draft client proposal", "Schedule system backup", "Analyze customer feedback",
    "Research competitors", "Design app icons", "Implement email notifications",
    "Create data visualization", "Review pull requests", "Prepare marketing strategy",
    "Plan UI/UX improvements", "Update project timeline"
]

STATUSES = ["To Do", "In Progress", "Completed"]
PRIORITIES = ["Low", "Medium", "High"]

def generate_random_tasks_for_users(task_count_per_user=10):
    """Generate unique random tasks for all users, avoiding duplicates."""
    users = User.objects.all()
    total_created = 0

    if not users.exists():
        print("⚠️ No users found. Please create at least one user first.")
        return

    for user in users:
        print(f"👤 Creating tasks for user: {user.username}")

        available_titles = TASK_TITLES.copy()
        random.shuffle(available_titles)

        for title in available_titles[:task_count_per_user]:
            # Check if task with this title already exists for this user
            if Task.objects.filter(title=title, added_by=user).exists():
                print(f"⚠️ Skipping duplicate for {user.username}: {title}")
                continue

            task = Task.objects.create(
                title=title,
                description=f"{title} — Auto-generated task for {user.username}.",
                due_date=timezone.now().date() + timedelta(days=random.randint(1, 30)),
                priority=random.choice(PRIORITIES),
                status=random.choice(STATUSES),
                added_by=user
            )
            total_created += 1

    print(f"✅ Successfully added {total_created} new tasks across {users.count()} users.")

if __name__ == "__main__":
    generate_random_tasks_for_users(15)
