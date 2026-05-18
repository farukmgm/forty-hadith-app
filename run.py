import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add models to Flask shell context"""
    from app.models import User, Hadith, UserProgress, UserStats, DailyReview
    return {
        'db': db,
        'User': User,
        'Hadith': Hadith,
        'UserProgress': UserProgress,
        'UserStats': UserStats,
        'DailyReview': DailyReview
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
