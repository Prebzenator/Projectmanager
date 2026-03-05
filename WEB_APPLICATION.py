"""
WEB APPLICATION SETUP & RUN GUIDE
==================================

Project Planner now has a full web interface!
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PROJECT PLANNER - WEB APPLICATION                       ║
║                           Setup & Run Guide                                ║
╚════════════════════════════════════════════════════════════════════════════╝


REQUIREMENTS
============

✓ Python 3.8+ (already installed)
✓ Flask (web framework)
✓ Flask-CORS (for API)


INSTALLATION
============

1. Install dependencies:

   Option A - Using batch file:
   ├─ Double-click: run_web.bat
   └─ (automatically installs dependencies)

   Option B - Manual install:
   ├─ Open PowerShell/terminal
   ├─ Navigate to projectplanner folder
   └─ Run: C:\Users\truls\AppData\Local\Python\bin\python3.exe -m pip install -r requirements.txt


RUNNING THE APPLICATION
=======================

Method 1 - Batch File (Easiest):
├─ Double-click: run_web.bat
├─ Wait for server to start
└─ Browser opens automatically to http://localhost:5000

Method 2 - Manual:
├─ Open PowerShell
├─ Navigate to: C:\Users\truls\OneDrive\Dokumenter\IS211\projectplanner
├─ Run: C:\Users\truls\AppData\Local\Python\bin\python3.exe app.py
└─ Open browser: http://localhost:5000


STOPPING THE APPLICATION
=========================

├─ Press Ctrl+C in the terminal
└─ Server will shut down gracefully


APPLICATION STRUCTURE
=====================

Web Application:
├─ app.py                          (Flask backend)
├─ requirements.txt                (Python dependencies)
├─ run_web.bat                     (Windows launcher)
│
└─ web/
   ├─ templates/
   │  └─ index.html                (Main web page)
   │
   └─ static/
      ├─ css/
      │  └─ style.css              (Styling)
      │
      └─ js/
         └─ app.js                 (Frontend logic)

Backend:
├─ features/
│  ├─ planner.py                  (Business logic)
│  └─ scheduler.py                (Task scheduling)
│
└─ tables/
   ├─ organization.py
   ├─ member.py
   ├─ project.py
   ├─ task.py
   └─ attributes.py


FEATURES
========

Setup Tab:
  • Create organization
  • Add qualities (skills)
  • Add constraints (limitations)

Organization Tab:
  • Add team members
  • Assign qualities and constraints
  • Set available hours
  • View all members

Projects Tab:
  • Create projects
  • Add members to projects
  • Add tasks with skill requirements
  • Assign tasks to members
  • Update task status
  • Smart member matching based on skills


HOW IT WORKS
============

1. Backend (Python/Flask):
   ├─ Runs REST API on http://localhost:5000/api
   ├─ Uses existing Planner class
   ├─ Manages all business logic
   └─ Provides JSON responses

2. Frontend (HTML/CSS/JavaScript):
   ├─ Clean, simple web interface
   ├─ Communicates with API
   ├─ Real-time updates
   └─ Responsive design (works on desktop/tablet/mobile)

3. Communication:
   └─ Frontend → REST API → Backend → Response


FIRST TIME USAGE
================

1. Start the application (run_web.bat)
2. Browser opens to: http://localhost:5000
3. Create an organization
4. Add qualities and constraints
5. Add team members with skills
6. Create a project
7. Add members to the project
8. Add tasks with requirements
9. System shows compatible members
10. Assign tasks and track progress


API ENDPOINTS
=============

Organization:
  POST   /api/organization/create
  GET    /api/organization/info

Qualities:
  POST   /api/qualities/add
  GET    /api/qualities

Constraints:
  POST   /api/constraints/add
  GET    /api/constraints

Members:
  POST   /api/members/create
  GET    /api/members

Projects:
  POST   /api/projects/create
  GET    /api/projects
  GET    /api/projects/<name>
  POST   /api/projects/<name>/members/add

Tasks:
  POST   /api/tasks/add
  POST   /api/tasks/<project>/compatible_members
  POST   /api/tasks/assign
  PUT    /api/tasks/status/<project>/<task>


TROUBLESHOOTING
===============

Problem: "Flask not found"
Solution:
  ├─ Use run_web.bat (auto-installs)
  └─ Or: pip install Flask flask-cors

Problem: Port 5000 already in use
Solution:
  ├─ Close other applications using port 5000
  ├─ Or modify app.py: app.run(port=5001)
  └─ Then access: http://localhost:5001

Problem: API calls fail / CORS errors
Solution:
  ├─ Make sure Flask is running
  ├─ Check console for error messages
  └─ Restart the application

Problem: Browser shows "Cannot GET /"
Solution:
  ├─ Wait for Flask to fully start
  ├─ Refresh the page
  └─ Check that http://localhost:5000 is the correct URL


DEPLOYMENT
==========

For production (not needed for assignment):
  • Use gunicorn instead of Flask development server
  • Deploy to Heroku, AWS, PythonAnywhere, etc.
  • Use environment variables for configuration
  • Enable HTTPS/SSL certificates
  • Add database persistence


DEVELOPMENT
===========

To modify the interface:
  1. Edit: web/templates/index.html (structure)
  2. Edit: web/static/css/style.css (styling)
  3. Edit: web/static/js/app.js (functionality)
  4. Refresh browser to see changes

To add backend features:
  1. Add methods to Planner class (features/planner.py)
  2. Add API endpoints to app.py
  3. Add UI components to index.html
  4. Add JavaScript functions to app.js


DATA PERSISTENCE
================

Current: Data stored in memory (lost when app closes)

To add persistence:
  • Option 1: SQLite database
  • Option 2: JSON file save/load
  • Option 3: PostgreSQL/MySQL
  • See features/planner.py for integration points


DOCUMENTATION FOR ASSIGNMENT
=============================

✓ Business idea: Project Planner for resource allocation
✓ Features: Documented in README.md
✓ Time Complexity: See TECHNICAL_ANALYSIS.py
✓ Data Structures: Heap (scheduler) + Lists
✓ Web Frontend: Fully functional
✓ REST API: Complete endpoints
✓ Code Examples: Available in features/planner.py


NEXT STEPS
==========

1. Run: run_web.bat
2. Test all features in the web interface
3. Create sample data (org, members, projects, tasks)
4. Verify intelligent task assignment works
5. Document everything for assignment
6. Push to GitHub with link in report


TIPS
====

• Keep browser DevTools open (F12) to see API calls
• Check Flask console for any errors
• Use simple test data first before complex scenarios
• Save screenshots of the application for your report
• Test on different browsers if possible


CONTACT & SUPPORT
=================

For issues with the web application:
  • Check Flask console output for error messages
  • Verify all dependencies installed: pip list | grep -i flask
  • Make sure port 5000 is available
  • Try closing and restarting the application


═══════════════════════════════════════════════════════════════════════════════

Ready to run the web application?

Double-click: run_web.bat

Or run: C:\Users\truls\AppData\Local\Python\bin\python3.exe app.py

Then open: http://localhost:5000

═══════════════════════════════════════════════════════════════════════════════
""")
