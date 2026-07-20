"""Refresh cache once (useful for a scheduled/systemd-timer extension)."""

from app import create_app, get_data

app = create_app()
with app.app_context():
    print(get_data(app)["source"])
