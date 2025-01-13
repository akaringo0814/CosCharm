from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.dispatch import receiver

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'app':  # 対象アプリ名
        print("Loading initial data for app...")
        try:
            call_command('loaddata', 'cosmetic.json')
            print("Initial data loaded successfully.")
        except Exception as e:
            print(f"Error loading initial data: {e}")
