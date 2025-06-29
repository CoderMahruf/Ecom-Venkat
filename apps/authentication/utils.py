from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int
from datetime import datetime, timedelta, timezone

class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

    def check_token(self, user, token):
        try:
            # Get timestamp (before calling super)
            ts_b36 = token.split("-")[0]
            ts_int = base36_to_int(ts_b36)
            token_time = datetime(2001, 1, 1, tzinfo=timezone.utc) + timedelta(days=ts_int)
            age = timezone.now() - token_time

            print(f"🔍 Token age: {age.total_seconds()} seconds")

            if age > timedelta(minutes=50):
                return False

            # Now check token integrity
            return super().check_token(user, token)
        except Exception as e:
            print("❌ Token validation error:", e)
            return False

# Global instance
activation_token_generator = ExpiringTokenGenerator()