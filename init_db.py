"""
Database initialization and management script.
Provides utilities for creating, clearing, and resetting the database.
"""

import os
import sys
from datetime import datetime
from app import create_app, db
from app.models import User, Hadith, UserProgress, UserStats, DailyReview

# Create app context
app = create_app(os.getenv('FLASK_ENV', 'development'))

def init_db():
    """Initialize the database - create all tables"""
    with app.app_context():
        print("🔄 Initializing database...")
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            print_db_info()
            return True
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False

def drop_db():
    """Drop all tables from the database"""
    with app.app_context():
        print("⚠️  WARNING: This will delete ALL data from the database!")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        
        if confirm.lower() == 'yes':
            try:
                db.drop_all()
                print("✅ All tables dropped successfully!")
                return True
            except Exception as e:
                print(f"❌ Error dropping tables: {e}")
                return False
        else:
            print("❌ Operation cancelled.")
            return False

def reset_db():
    """Reset database - drop all tables and recreate them"""
    with app.app_context():
        print("🔄 Resetting database...")
        print("⚠️  WARNING: This will delete ALL data!")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        
        if confirm.lower() == 'yes':
            try:
                db.drop_all()
                print("  ✓ Dropped all tables")
                db.create_all()
                print("  ✓ Created new tables")
                print("✅ Database reset successfully!")
                print_db_info()
                return True
            except Exception as e:
                print(f"❌ Error resetting database: {e}")
                return False
        else:
            print("❌ Operation cancelled.")
            return False

def print_db_info():
    """Print information about database tables"""
    with app.app_context():
        print("\n📊 Database Information:")
        print("-" * 50)
        
        # Count records in each table
        user_count = User.query.count()
        hadith_count = Hadith.query.count()
        progress_count = UserProgress.query.count()
        stats_count = UserStats.query.count()
        daily_count = DailyReview.query.count()
        
        print(f"  Users:          {user_count} records")
        print(f"  Hadiths:        {hadith_count} records")
        print(f"  User Progress:  {progress_count} records")
        print(f"  User Stats:     {stats_count} records")
        print(f"  Daily Reviews:  {daily_count} records")
        print("-" * 50)
        
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'forty_hadith.db')
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / 1024  # Size in KB
            print(f"  Database file:  {db_path}")
            print(f"  Database size:  {db_size:.2f} KB")
        print()

def create_test_user():
    """Create a test user for development"""
    with app.app_context():
        print("👤 Creating test user...")
        
        # Check if user already exists
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print("⚠️  Test user already exists!")
            return False
        
        try:
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            test_user.set_password('testpass123')
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created successfully!")
            print(f"  Username: testuser")
            print(f"  Email: test@example.com")
            print(f"  Password: testpass123")
            return True
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            db.session.rollback()
            return False

def verify_database():
    """Verify database structure and integrity"""
    with app.app_context():
        print("🔍 Verifying database structure...")
        
        try:
            # Try to query each table
            User.query.first()
            print("  ✓ Users table OK")
            
            Hadith.query.first()
            print("  ✓ Hadiths table OK")
            
            UserProgress.query.first()
            print("  ✓ User Progress table OK")
            
            UserStats.query.first()
            print("  ✓ User Stats table OK")
            
            DailyReview.query.first()
            print("  ✓ Daily Reviews table OK")
            
            print("✅ Database structure verified successfully!")
            print_db_info()
            return True
        except Exception as e:
            print(f"❌ Error verifying database: {e}")
            return False

def main():
    """Main function with CLI options"""
    if len(sys.argv) < 2:
        print("Database Initialization Script")
        print("=" * 50)
        print("\nUsage: python init_db.py [command]")
        print("\nCommands:")
        print("  init        - Initialize database (create tables)")
        print("  drop        - Drop all tables")
        print("  reset       - Reset database (drop and recreate)")
        print("  info        - Show database information")
        print("  verify      - Verify database structure")
        print("  test-user   - Create a test user")
        print("\nExamples:")
        print("  python init_db.py init")
        print("  python init_db.py info")
        print("  python init_db.py test-user")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_db()
    elif command == 'drop':
        drop_db()
    elif command == 'reset':
        reset_db()
    elif command == 'info':
        with app.app_context():
            print_db_info()
    elif command == 'verify':
        verify_database()
    elif command == 'test-user':
        create_test_user()
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python init_db.py' for usage information")

if __name__ == '__main__':
    main()
