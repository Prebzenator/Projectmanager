# Projectmanager

## Getting Started

1. **Install dependencies**
   - Make sure you have Python 3 installed.
   - (Recommended) Create a virtual environment:
     ```sh
     python -m venv .venv
     source .venv/bin/activate  # macOS/Linux
     .venv\Scripts\activate    # Windows
     ```
   - Install Flask:
     ```sh
     pip install flask
     ```

2. **Start the backend server**
   - Run this command from the project root directory:
     ```sh
     python -m backend.api
     ```

3. **Open the frontend**
   - Open your browser and go to:
     ```
     http://127.0.0.1:5000/
     ```
   - You can also go directly to e.g. `organization.html`:
     ```
     http://127.0.0.1:5000/organization.html
     ```

## Tips
- All data is stored in memory (no database). Data will be lost when the server stops.
- If you get errors, check that you have installed all required Python packages.
- To stop the server: press `Ctrl + C` in the terminal.




