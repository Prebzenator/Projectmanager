"""
INTERACTIVE APPLICATION WALKTHROUGH
====================================

When you run: python projectplanner.py

This is what happens step-by-step:
"""

print("""
STEP 1: Application Starts
==================================================

You run: python projectplanner.py

The application displays:

    ==================================================
      VELKOMMEN TIL PROJECT PLANNER
    ==================================================

    Version 0.1 - Basis Foundation
    Prèm Enter for å begynne...

[You press Enter]


STEP 2: Main Menu
==================================================

You're now in the main menu:

    ==================================================
      HOVEDMENY
    ==================================================
    1. Lag organisasjon
    2. Administrer organisasjon
    3. Administrer prosjekter
    4. Vis organisasjonsstatus
    0. Tilbake/Avslutt

    Velg alternativ: 

[You select option 1]


STEP 3: Create Organization
==================================================

You're prompted to create an organization:

    ==================================================
      LAG ORGANISASJON
    ==================================================
    Organisasjonsnavn: My Company

    ✓ Organisasjon 'My Company' opprettet!
    Trykk Enter for å fortsette...

[You press Enter]


STEP 4: Back to Main Menu
==================================================

Back at the main menu:

    ==================================================
      HOVEDMENY
    ==================================================
    1. Lag organisasjon
    2. Administrer organisasjon
    3. Administrer prosjekter
    4. Vis organisasjonsstatus
    0. Tilbake/Avslutt

    Velg alternativ: 

[You select option 2 - Administrer organisasjon]


STEP 5: Organization Administration Submenu
==================================================

    ==================================================
      ADMINISTRER ORGANISASJON
    ==================================================
    1. Legg til kvalitet
    2. Legg til begrensning
    3. Legg til medlem
    4. Vis alle medlemmer
    5. Vis alle kvaliteter og begrensninger
    0. Tilbake/Avslutt

    Velg alternativ: 

[You select option 1 - Legg til kvalitet]


STEP 6: Add Quality
==================================================

    ==================================================
      LEGG TIL KVALITET
    ==================================================
    Kvalitetsnavn: Python
    Beskrivelse (valgfritt): Python programming skill

    ✓ Kvalitet 'Python' lagt til!
    Trykk Enter for å fortsette...


STEP 7: Back to Organization Menu
==================================================

You can:
- Add more qualities
- Add constraints (limitations like "No weekends")
- Add team members with their skills
- View members and their assignments


STEP 8: Add Team Member
==================================================

    ==================================================
      LEGG TIL MEDLEM
    ==================================================
    Medlemsnavn: Alice Johnson
    Rolle: Senior Developer
    Tilgjengelige timer: 40

    Tilgjengelige kvaliteter:
      1. Python
      2. Leadership
    
    Søk til kvaliteter (kommaseparert nummer): 1,2

    ✓ Medlem 'Alice Johnson' lagt til!
    Trykk Enter for å fortsette...


STEP 9: Create Projects
==================================================

From the main menu, select 3 (Administrer prosjekter):

    ==================================================
      ADMINISTRER PROSJEKTER
    ==================================================
    1. Lag nytt prosjekt
    2. Velg prosjekt for å administrere
    3. Vis alle prosjekter
    0. Tilbake/Avslutt

    Velg alternativ: 1

Then:

    ==================================================
      LAG NYTT PROSJEKT
    ==================================================
    Prosjektnavn: Website Redesign
    Varighet i uker (valgfritt): 8

    ✓ Prosjekt 'Website Redesign' opprettet!
    Trykk Enter for å fortsette...


STEP 10: Manage Project
==================================================

Select "2. Velg prosjekt for å administrere":

    ==================================================
      VELG PROSJEKT
    ==================================================
    1. Website Redesign

    Velg prosjekt: 1

Then you're in project management:

    ==================================================
      PROSJEKT: Website Redesign
    ==================================================
    1. Legg til oppgave
    2. Legg til medlem i prosjekt
    3. Vis oppgaver
    4. Vis medlemmer i prosjekt
    5. Tilordne oppgave til medlem
    0. Tilbake/Avslutt

    Velg alternativ: 


STEP 11: Add Tasks to Project
==================================================

Select option 1 (Legg til oppgave):

    ==================================================
      LEGG TIL OPPGAVE
    ==================================================
    Oppgavenavn: Design API Architecture
    Antall timer: 16
    Frist (f.eks. 2026-03-15): 2026-03-20

    Tilgjengelige kvaliteter:
      1. Python
      2. Leadership
    
    Påkrevd kvaliteter (kommaseparert nummer): 1,2

    ✓ Oppgave 'Design API Architecture' lagt til prosjektet!
    Trykk Enter for å fortsette...


STEP 12: Assign Tasks to Members
==================================================

Select option 5 (Tilordne oppgave til medlem):

The system shows:

    ==================================================
      TILORDNE OPPGAVE TIL MEDLEM
    ==================================================
    1. Design API Architecture (16 timer)

    Velg oppgave: 1

    Kompatible medlemmer for 'Design API Architecture':
    1. Alice Johnson (40 timer tilgjengelig)

    Velg medlem: 1

    ✓ Oppgave 'Design API Architecture' tilordnet til Alice Johnson!
    Trykk Enter for å fortsette...


THE WORKFLOW IN PRACTICE:
==================================================

Typical session flow:

1. Start application
2. Create organization → "Tech Company"
3. Define organizational qualities:
   - Python
   - JavaScript
   - Leadership
   - UI Design
4. Define constraints:
   - Remote
   - Flexible hours
5. Add team members:
   - Alice: Senior Developer (Python, Leadership)
   - Bob: Frontend Dev (JavaScript)
   - Charlie: Designer (UI Design)
6. Create projects:
   - "Website Redesign"
   - "Mobile App"
7. Assign members to projects
8. Add tasks to projects:
   - "Build API" (requires Python)
   - "Create UI" (requires UI Design)
9. Let the system match tasks to qualified members
10. Track progress as tasks are completed


KEY FEATURES IN ACTION:
==================================================

✓ The system validates that members have required skills
✓ Hours are automatically deducted when tasks are assigned
✓ Can't assign task if member doesn't have time available
✓ Can view all members, projects, and tasks
✓ Task status can be tracked (pending → assigned → in progress → completed)
✓ Constraints are checked (members with conflicting constraints skip tasks)
✓ Can see organization overview with counts and details


ON EACH SCREEN:
==================================================

- Press "0" to go back to the previous menu
- Press "Ctrl+C" to exit at any time
- Invalid input shows error and asks to try again
- All data is held in memory during the session


DATA PERSISTENCE:
==================================================

Currently: Data is stored in memory only (lost when you close)
Next step: Team member working on persistence could:
  - Save to JSON file
  - Save to database
  - Add CSV export
  - Add backup/restore


EXAMPLE SESSION DURATION:
==================================================

- Quick test: 2-3 minutes (create org, add 1 member, 1 project, 1 task)
- Full workflow: 10-15 minutes (complete organization setup)
- Integration testing: 20-30 minutes (multiple projects and scenarios)

---

READY TO TRY IT?
==================================================

Run this command:

    python3.exe projectplanner.py

Or double-click:

    run.bat

Then interact with the menus using numbers (1, 2, 3...) and press Enter.

The application guides you through each step with clear prompts.

Let's go! 🚀
""")
