# Forty Hadith Annawawi Learning Platform - Project Checklist

## Project Overview
A web application built with Python (Flask), SQL, and JavaScript to help users learn and continuously apply the Forty Hadith Annawawi through daily reviews, personal reflections, and progress tracking.

**Tech Stack:** Flask, SQLite/PostgreSQL, JavaScript, HTML/CSS  
**Project Type:** CS50x Final Project  
**Start Date:** 2026-05-18

---

## PHASE 1: PLANNING & SETUP ✅ COMPLETE

- [x] Define project scope (must-have vs. nice-to-have features)
- [x] Create GitHub repository for version control
- [x] Set up project documentation (README.md with project overview)
- [x] Choose Flask (recommended for simplicity)
- [x] Set up virtual environment (venv)
- [x] Create project structure and directories
- [x] Create all foundational configuration files
- [x] Initialize git and make all foundational commits

**Completed Files:**
- ✅ `requirements.txt` - Python dependencies
- ✅ `config.py` - Development/test/production configs
- ✅ `.env.example` - Environment variable template
- ✅ `run.py` - Flask entry point
- ✅ `app/__init__.py` - Flask app factory
- ✅ `app/models.py` - SQLAlchemy models (User, Hadith, UserProgress, UserStats, DailyReview)
- ✅ `app/routes.py` - Blueprint structure for all routes
- ✅ `app/forms.py` - WTForms for validation
- ✅ `schema.sql` - Complete database schema with indexes
- ✅ `app/templates/index.html` - Home page template

---

## PHASE 2: DATABASE DESIGN & SETUP ✅ COMPLETE

- [x] Finalize database schema
- [x] Create `schema.sql` file with all CREATE TABLE statements
- [x] Add database indexes for performance
- [x] Set up SQLAlchemy models (User, Hadith, UserProgress, UserStats, DailyReview)
- [x] Create database initialization script
- [x] Test database creation locally

**Completed Files:**
- ✅ `schema.sql` - Complete database schema with tables and indexes
- ✅ `app/models.py` - All 5 SQLAlchemy models fully configured
- ✅ `init_db.py` - Database initialization and management script
  - `init` - Create all tables
  - `drop` - Drop all tables
  - `reset` - Reset database
  - `info` - Show database information
  - `verify` - Verify database structure
  - `test-user` - Create test user

**Verification Status:**
- ✅ Database tables created successfully
- ✅ All models verified
- ✅ Database initialization script tested
- ✅ Test user creation working
- ✅ Database integrity verified

---

## PHASE 3: DATA SEEDING ✅ COMPLETE

- [x] Download/clone hadith-json repository
- [x] Inspect actual JSON structure from hadith-json (verify field names)
- [x] Write Python script to parse hadith JSON
- [x] Write Python script to insert hadith data into database
- [x] Seed hadiths table with all 42 hadiths (note: collection contains 42, not 40)
- [x] Verify data imported correctly (spot-check 3 records)
- [x] Document any data transformations applied

**Completed Files:**
- ✅ `seed_db.py` - Hadith data seeding script
  - `download` - Preview hadith JSON
  - `seed` - Download and seed database (MAIN COMMAND)
  - `verify` - Verify seeded data
  - `reset-seed` - Clear and reseed database
- ✅ `debug_json.py` - JSON structure inspection tool

**Data Import Details:**
- ✅ Source: `https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json`
- ✅ Total hadiths imported: 42 (not 40 as name suggests)
- ✅ Fields extracted: `hadith_number`, `arabic_text`, `english_translation`, `narrator`, `source`, `title`
- ✅ Spot-checked hadiths: #1 (Umar bin al-Khattab), #21 (Sufyan bin Abd Allah), #42 (Anas bin Malik)
- ✅ All Arabic and English texts verified
- ✅ Database integrity verified

---

## PHASE 4: BACKEND - USER AUTHENTICATION

- [ ] Install Flask-Login and password hashing library (werkzeug)
- [ ] Create User model with username, email, password_hash
- [ ] Implement user registration endpoint/form
  - [ ] Validate username (unique, appropriate length)
  - [ ] Validate email format
  - [ ] Validate password strength
  - [ ] Hash passwords securely
- [ ] Implement login endpoint/form
  - [ ] Verify credentials
  - [ ] Create session/login user
- [ ] Implement logout functionality
- [ ] Create login_required decorator for protected routes
- [ ] Test authentication flow (register → login → logout)

---

## PHASE 5: BACKEND - HADITH MANAGEMENT

- [ ] Create Hadith model
- [ ] Create GET endpoint: `/api/hadiths` (list all 42 hadiths)
  - [ ] Include pagination or filters if desired
  - [ ] Return JSON with id, hadith_number, arabic_text, english_text, narrator
- [ ] Create GET endpoint: `/api/hadiths/<id>` (get single hadith)
- [ ] Create GET endpoint: `/api/hadiths/today` (daily hadith feature - optional)
- [ ] Test all hadith endpoints with curl or Postman

---

## PHASE 6: BACKEND - USER PROGRESS TRACKING

- [ ] Create UserProgress model
- [ ] Create POST endpoint: `/api/progress/mark-reviewed` 
  - [ ] Accept user_id and hadith_id
  - [ ] Create/update user_progress record
  - [ ] Set is_reviewed_today = 1
  - [ ] Set last_reviewed_at timestamp
- [ ] Create POST endpoint: `/api/progress/mark-memorized`
  - [ ] Accept user_id and hadith_id
  - [ ] Update is_memorized flag
- [ ] Create POST endpoint: `/api/progress/save-reflection`
  - [ ] Accept user_id, hadith_id, and reflection text
  - [ ] Save reflection_text to database
- [ ] Create GET endpoint: `/api/progress/user/<user_id>`
  - [ ] Return all progress records for user
  - [ ] Include statistics (total memorized, total reviewed today, etc.)
- [ ] Test progress tracking endpoints

---

## PHASE 7: BACKEND - STATISTICS & STREAKS

- [ ] Create UserStats model
- [ ] Write function to calculate user statistics:
  - [ ] Count total memorized hadith
  - [ ] Count hadith reviewed today
  - [ ] Calculate current streak (consecutive days with at least 1 review)
  - [ ] Track longest streak ever
- [ ] Create GET endpoint: `/api/stats/user/<user_id>`
  - [ ] Return user's statistics
- [ ] Implement daily streak logic (reset is_reviewed_today at midnight)
  - [ ] Consider timezone handling
- [ ] Test statistics calculations

---

## PHASE 8: FRONTEND - SETUP & STRUCTURE

- [ ] Create `templates/` directory for HTML files
- [ ] Create `static/` directory for CSS and JavaScript
- [ ] Set up base template (`base.html`) with navigation
- [ ] Set up CSS file (or Bootstrap for faster styling)
- [ ] Create main layout (header, sidebar/nav, main content area)
- [ ] Test basic HTML rendering

---

## PHASE 9: FRONTEND - AUTHENTICATION PAGES

- [ ] Create registration page (`register.html`)
  - [ ] Form with username, email, password, confirm password
  - [ ] Client-side validation (optional but good practice)
  - [ ] Submit to registration endpoint
  - [ ] Display error messages
  - [ ] Redirect to login on success
- [ ] Create login page (`login.html`)
  - [ ] Form with username/email and password
  - [ ] Submit to login endpoint
  - [ ] Display error messages
  - [ ] Redirect to dashboard on success
- [ ] Create logout button (navigation)
- [ ] Test authentication flow in browser

---

## PHASE 10: FRONTEND - HADITH VIEWING

- [ ] Create hadith list page (`hadiths.html` or `/hadiths`)
  - [ ] Fetch and display all 42 hadiths
  - [ ] Show hadith_number, arabic_text, english_text
  - [ ] Add click/expand functionality to show narrator and details
  - [ ] Style for readability (especially Arabic text sizing)
- [ ] Create individual hadith detail page (`hadith.html?id=<id>` or `/hadiths/<id>`)
  - [ ] Display full hadith with all fields
  - [ ] Show beautiful formatting for Arabic and English
- [ ] Implement hadith search/filter (by number or keyword) - optional
- [ ] Test hadith viewing pages

---

## PHASE 11: FRONTEND - PROGRESS TRACKING UI

- [ ] Create user dashboard page (`dashboard.html`)
  - [ ] Show user's name and statistics
  - [ ] Display total memorized, reviewed today, streak
  - [ ] Show progress bar or visual indicator (e.g., "32/42 memorized")
- [ ] Create hadith review interface
  - [ ] Button to mark hadith as "reviewed today"
  - [ ] Button to mark hadith as "memorized"
  - [ ] Text area for personal reflection/notes
  - [ ] Show saved reflection if exists
  - [ ] Submit via JavaScript (AJAX) to POST endpoints
- [ ] Create user progress page (`progress.html`)
  - [ ] Show all hadiths with their status (memorized, reviewed, not started)
  - [ ] Color-coding (green = memorized, yellow = reviewed, gray = not started)
  - [ ] Click to view/edit reflection
- [ ] Test progress tracking UI

---

## PHASE 12: FRONTEND - STATISTICS & STREAKS PAGE

- [ ] Create statistics page (`stats.html`)
  - [ ] Display current streak
  - [ ] Display longest streak
  - [ ] Show total hadiths memorized
  - [ ] Show calendar/chart of review activity (optional but nice)
- [ ] Display motivational messages based on milestones
  - [ ] "Great job! You've memorized 10 hadiths!"
  - [ ] "7-day streak! Keep it up!"
- [ ] Test statistics display

---

## PHASE 13: FRONTEND - OPTIONAL FEATURES

- [ ] Implement "Hadith of the Day" feature
  - [ ] Display random hadith on dashboard
  - [ ] Change daily
- [ ] Create reflection/notes viewing page
  - [ ] Show all user's saved reflections
  - [ ] Filter by hadith or date
- [ ] Implement search functionality
  - [ ] Search hadiths by number, keyword, or topic
- [ ] Add settings page
  - [ ] Change password
  - [ ] Update email
  - [ ] Delete account (optional)

---

## PHASE 14: TESTING

- [ ] Test user registration with valid data
- [ ] Test user registration with invalid data (duplicate username, weak password)
- [ ] Test login with correct and incorrect credentials
- [ ] Test protected routes (redirect to login if not authenticated)
- [ ] Test hadith data (verify all 42 are in database)
- [ ] Test marking hadith as reviewed/memorized
- [ ] Test saving reflections
- [ ] Test statistics calculations
- [ ] Test streak logic (manual testing with fake dates)
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test responsive design on mobile (use browser dev tools)
- [ ] Write basic unit tests for critical functions (optional but recommended)

---

## PHASE 15: DOCUMENTATION

- [ ] Write comprehensive README.md
  - [ ] Project description and purpose
  - [ ] Features overview
  - [ ] Tech stack
  - [ ] Installation instructions
  - [ ] How to run the app
  - [ ] Database schema explanation
  - [ ] API endpoint documentation
- [ ] Add comments to code (especially complex logic)
- [ ] Document any assumptions or design decisions
- [ ] Create a SETUP.md or INSTALLATION.md if needed
- [ ] Document how to seed the database
- [ ] Add screenshots/demo in README (optional but impressive)

---

## PHASE 16: DEPLOYMENT & FINAL POLISH

- [ ] Set up `.gitignore` (exclude venv, __pycache__, .env, etc.)
- [ ] Add environment variables (.env file for database URL, secret key, etc.)
- [ ] Test app one final time from fresh setup
- [ ] Ensure all features work correctly
- [ ] Fix any bugs found during testing
- [ ] Clean up unused code
- [ ] Optimize performance (query optimization, caching if needed)
- [ ] Add error handling for edge cases
- [ ] Test error messages are user-friendly
- [ ] Consider deploying to a platform (Heroku, PythonAnywhere, Replit) - optional for CS50x

---

## PHASE 17: PRESENTATION PREP (CS50x Specific)

- [ ] Record a demo video showing the app in action
  - [ ] User registration
  - [ ] Viewing hadiths
  - [ ] Marking progress
  - [ ] Viewing statistics
- [ ] Prepare a short presentation (3-5 minutes)
  - [ ] Explain motivation and impact
  - [ ] Show tech stack
  - [ ] Demo key features
  - [ ] Discuss challenges overcome
- [ ] Create a final commit with all work
- [ ] Push to GitHub with clear commit history
- [ ] Write a compelling project README

---

## PROGRESS TRACKING

**Start Date:** 2026-05-18  
**Phases Completed:** 3/17  
**Current Phase:** Phase 4 (Backend - User Authentication)  
**Estimated Completion:** ~4-5 weeks  

| Phase | Name | Status |
|-------|------|--------|
| 1 | Planning & Setup | ✅ Complete |
| 2 | Database Design & Setup | ✅ Complete |
| 3 | Data Seeding | ✅ Complete |
| 4 | Backend - Authentication | 🔄 In Progress |
| 5 | Backend - Hadith Management | ⏳ Pending |
| 6 | Backend - Progress Tracking | ⏳ Pending |
| 7 | Backend - Statistics & Streaks | ⏳ Pending |
| 8 | Frontend - Setup | ⏳ Pending |
| 9 | Frontend - Auth Pages | ⏳ Pending |
| 10 | Frontend - Hadith Viewing | ⏳ Pending |
| 11 | Frontend - Progress UI | ⏳ Pending |
| 12 | Frontend - Statistics | ⏳ Pending |
| 13 | Frontend - Optional Features | ⏳ Pending |
| 14 | Testing | ⏳ Pending |
| 15 | Documentation | ⏳ Pending |
| 16 | Deployment & Polish | ⏳ Pending |
| 17 | Presentation Prep | ⏳ Pending |

---

## NOTES & OBSERVATIONS

- **2026-05-18**: Phase 1 complete! All configuration, models, forms, routes, and schema created
- **2026-05-19**: Phase 1 extended - added index.html home page template
- **2026-05-20**: Phase 2 complete! Database initialization script created and fully tested
  - All init_db.py commands working (init, drop, reset, info, verify, test-user)
  - Database structure verified with all 5 tables created correctly
  - Test user creation functional
  - All database models follow SQLAlchemy best practices
- **2026-06-03**: Phase 3 complete! All 42 hadiths successfully imported from JSON
  - Used uthumany/nawawi-40-hadiths repository as primary source
  - Created debug_json.py to inspect actual JSON structure
  - Fixed seed_db.py field mappings: `english_translation` field identified and mapped correctly
  - Successfully parsed and inserted all 42 hadiths (not 40 as name suggests)
  - Spot-checked hadiths #1, #21, and #42 - all data verified
  - Arabic and English texts imported and verified
  - Database ready for authentication implementation
