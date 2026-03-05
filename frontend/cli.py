"""
Command-line interface for the Project Planner application
"""

from features.planner import Planner


class ProjectPlannerCLI:
    """Interactive command-line interface for project planning"""
    
    def __init__(self):
        self.planner = Planner()
        self.current_project = None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*50)
        print(f"  {title}")
        print("="*50)
    
    def print_menu(self, options: list):
        """Print menu options"""
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Tilbake/Avslutt")
    
    def main_menu(self):
        """Main menu"""
        while True:
            self.print_header("HOVEDMENY")
            options = [
                "Lag organisasjon",
                "Administrer organisasjon",
                "Administrer prosjekter",
                "Vis organisasjonsstatus"
            ]
            self.print_menu(options)
            
            choice = input("\nVelg alternativ: ").strip()
            
            if choice == "0":
                print("\nAvslutter applikasjonen...")
                break
            elif choice == "1":
                self.create_organization_menu()
            elif choice == "2":
                self.organization_menu()
            elif choice == "3":
                self.projects_menu()
            elif choice == "4":
                self.show_organization_status()
            else:
                print("Ugyldig valg. Prøv igjen.")
    
    def create_organization_menu(self):
        """Menu for creating organization"""
        self.print_header("LAG ORGANISASJON")
        
        org_name = input("Organisasjonsnavn: ").strip()
        if not org_name:
            print("Organisasjonsnavn kan ikke være tomt!")
            return
        
        self.planner.create_organization(org_name)
        print(f"\n✓ Organisasjon '{org_name}' opprettet!")
        input("Trykk Enter for å fortsette...")
    
    def organization_menu(self):
        """Menu for managing organization"""
        if not self.planner.get_organization():
            print("Ingen organisasjon opprettet. Opprett organisasjon først!")
            input("Trykk Enter for å fortsette...")
            return
        
        while True:
            self.print_header("ADMINISTRER ORGANISASJON")
            options = [
                "Legg til kvalitet",
                "Legg til begrensning",
                "Legg til medlem",
                "Vis alle medlemmer",
                "Vis alle kvaliteter og begrensninger"
            ]
            self.print_menu(options)
            
            choice = input("\nVelg alternativ: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.add_quality_menu()
            elif choice == "2":
                self.add_constraint_menu()
            elif choice == "3":
                self.add_member_menu()
            elif choice == "4":
                self.show_members()
            elif choice == "5":
                self.show_org_qualities_constraints()
            else:
                print("Ugyldig valg. Prøv igjen.")
    
    def add_quality_menu(self):
        """Menu for adding quality to organization"""
        self.print_header("LEGG TIL KVALITET")
        
        name = input("Kvalitetsnavn: ").strip()
        if not name:
            print("Kvalitetsnavn kan ikke være tomt!")
            return
        
        description = input("Beskrivelse (valgfritt): ").strip()
        
        self.planner.add_quality_to_organization(name, description)
        print(f"\n✓ Kvalitet '{name}' lagt til!")
        input("Trykk Enter for å fortsette...")
    
    def add_constraint_menu(self):
        """Menu for adding constraint to organization"""
        self.print_header("LEGG TIL BEGRENSNING")
        
        name = input("Begrensningsnavn: ").strip()
        if not name:
            print("Begrensningsnavn kan ikke være tomt!")
            return
        
        description = input("Beskrivelse (valgfritt): ").strip()
        
        self.planner.add_constraint_to_organization(name, description)
        print(f"\n✓ Begrensning '{name}' lagt til!")
        input("Trykk Enter for å fortsette...")
    
    def add_member_menu(self):
        """Menu for adding member to organization"""
        self.print_header("LEGG TIL MEDLEM")
        
        org = self.planner.get_organization()
        
        name = input("Medlemsnavn: ").strip()
        if not name:
            print("Medlemsnavn kan ikke være tomt!")
            return
        
        role = input("Rolle: ").strip()
        if not role:
            print("Rolle kan ikke være tomt!")
            return
        
        try:
            hours = int(input("Tilgjengelige timer: ").strip() or "0")
        except ValueError:
            print("Timer må være et tall!")
            return
        
        # Ask for qualities
        qualities = []
        if org.qualities:
            print("\nTilgjengelige kvaliteter:")
            for i, q in enumerate(org.qualities, 1):
                print(f"  {i}. {q.name}")
            
            qual_input = input("Søk til kvaliteter (kommaseparert nummer, eller trykk Enter for å hoppe over): ").strip()
            if qual_input:
                try:
                    indices = [int(x.strip())-1 for x in qual_input.split(",")]
                    qualities = [org.qualities[i].name for i in indices if 0 <= i < len(org.qualities)]
                except (ValueError, IndexError):
                    print("Ugyldig valg!")
        
        # Ask for constraints
        constraints = []
        if org.constraints:
            print("\nTilgjengelige begrensninger:")
            for i, c in enumerate(org.constraints, 1):
                print(f"  {i}. {c.name}")
            
            const_input = input("Hva gjelder begrensninger (kommaseparert nummer, eller trykk Enter for å hoppe over): ").strip()
            if const_input:
                try:
                    indices = [int(x.strip())-1 for x in const_input.split(",")]
                    constraints = [org.constraints[i].name for i in indices if 0 <= i < len(org.constraints)]
                except (ValueError, IndexError):
                    print("Ugyldig valg!")
        
        self.planner.create_member(name, role, hours, qualities, constraints)
        print(f"\n✓ Medlem '{name}' lagt til!")
        input("Trykk Enter for å fortsette...")
    
    def projects_menu(self):
        """Menu for managing projects"""
        if not self.planner.get_organization():
            print("Ingen organisasjon opprettet. Opprett organisasjon først!")
            input("Trykk Enter for å fortsette...")
            return
        
        while True:
            self.print_header("ADMINISTRER PROSJEKTER")
            options = [
                "Lag nytt prosjekt",
                "Velg prosjekt for å administrere",
                "Vis alle prosjekter"
            ]
            self.print_menu(options)
            
            choice = input("\nVelg alternativ: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.create_project_menu()
            elif choice == "2":
                self.select_project_menu()
            elif choice == "3":
                self.show_projects()
            else:
                print("Ugyldig valg. Prøv igjen.")
    
    def create_project_menu(self):
        """Menu for creating a project"""
        self.print_header("LAG NYTT PROSJEKT")
        
        name = input("Prosjektnavn: ").strip()
        if not name:
            print("Prosjektnavn kan ikke være tomt!")
            return
        
        try:
            duration = input("Varighet i uker (valgfritt): ").strip()
            duration = int(duration) if duration else None
        except ValueError:
            print("Varighet må være et tall!")
            return
        
        self.planner.create_project(name, duration)
        print(f"\n✓ Prosjekt '{name}' opprettet!")
        input("Trykk Enter for å fortsette...")
    
    def select_project_menu(self):
        """Menu for selecting a project"""
        projects = self.planner.get_projects()
        
        if not projects:
            print("Ingen prosjekter opprettet ennå!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("VELG PROSJEKT")
        
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name}")
        
        try:
            choice = int(input("\nVelg prosjekt: ").strip())
            if 1 <= choice <= len(projects):
                self.current_project = projects[choice - 1]
                self.project_management_menu()
            else:
                print("Ugyldig valg!")
        except ValueError:
            print("Vennligst skriv inn et tall!")
    
    def project_management_menu(self):
        """Menu for managing a selected project"""
        if not self.current_project:
            return
        
        while True:
            self.print_header(f"PROSJEKT: {self.current_project.name}")
            options = [
                "Legg til oppgave",
                "Legg til medlem i prosjekt",
                "Vis oppgaver",
                "Vis medlemmer i prosjekt",
                "Tilordne oppgave til medlem"
            ]
            self.print_menu(options)
            
            choice = input("\nVelg alternativ: ").strip()
            
            if choice == "0":
                self.current_project = None
                break
            elif choice == "1":
                self.add_task_menu()
            elif choice == "2":
                self.add_member_to_project_menu()
            elif choice == "3":
                self.show_tasks()
            elif choice == "4":
                self.show_project_members()
            elif choice == "5":
                self.assign_task_menu()
            else:
                print("Ugyldig valg. Prøv igjen.")
    
    def add_task_menu(self):
        """Menu for adding a task to project"""
        self.print_header("LEGG TIL OPPGAVE")
        
        title = input("Oppgavenavn: ").strip()
        if not title:
            print("Oppgavenavn kan ikke være tomt!")
            return
        
        try:
            hours = int(input("Antall timer: ").strip())
        except ValueError:
            print("Timer må være et tall!")
            return
        
        deadline = input("Frist (f.eks. 2026-03-15): ").strip()
        
        org = self.planner.get_organization()
        
        # Ask for required qualities
        required_qualities = []
        if org.qualities:
            print("\nTilgjengelige kvaliteter:")
            for i, q in enumerate(org.qualities, 1):
                print(f"  {i}. {q.name}")
            
            qual_input = input("Påkrevd kvaliteter (kommaseparert nummer, eller trykk Enter for å hoppe over): ").strip()
            if qual_input:
                try:
                    indices = [int(x.strip())-1 for x in qual_input.split(",")]
                    required_qualities = [org.qualities[i].name for i in indices if 0 <= i < len(org.qualities)]
                except (ValueError, IndexError):
                    print("Ugyldig valg!")
        
        # Ask for required constraints
        required_constraints = []
        if org.constraints:
            print("\nTilgjengelige begrensninger:")
            for i, c in enumerate(org.constraints, 1):
                print(f"  {i}. {c.name}")
            
            const_input = input("Påkrevd begrensninger (kommaseparert nummer, eller trykk Enter for å hoppe over): ").strip()
            if const_input:
                try:
                    indices = [int(x.strip())-1 for x in const_input.split(",")]
                    required_constraints = [org.constraints[i].name for i in indices if 0 <= i < len(org.constraints)]
                except (ValueError, IndexError):
                    print("Ugyldig valg!")
        
        self.planner.add_task_to_project(self.current_project, title, hours, 
                                        deadline, required_qualities, required_constraints)
        print(f"\n✓ Oppgave '{title}' lagt til prosjektet!")
        input("Trykk Enter for å fortsette...")
    
    def add_member_to_project_menu(self):
        """Menu for adding a member to the project"""
        members = self.planner.get_members()
        
        if not members:
            print("Ingen medlemmer i organisasjonen!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("LEGG TIL MEDLEM I PROSJEKT")
        
        # Show members not already in project
        available_members = [m for m in members if m not in self.current_project.members]
        
        if not available_members:
            print("Alle medlemmer er allerede lagt til prosjektet!")
            input("Trykk Enter for å fortsette...")
            return
        
        for i, member in enumerate(available_members, 1):
            print(f"{i}. {member.name} ({member.role})")
        
        try:
            choice = int(input("\nVelg medlem: ").strip())
            if 1 <= choice <= len(available_members):
                self.planner.assign_member_to_project(self.current_project, 
                                                      available_members[choice - 1])
                print(f"\n✓ Medlem lagt til prosjektet!")
            else:
                print("Ugyldig valg!")
        except ValueError:
            print("Vennligst skriv inn et tall!")
        
        input("Trykk Enter for å fortsette...")
    
    def assign_task_menu(self):
        """Menu for assigning tasks to members"""
        if not self.current_project.tasks:
            print("Ingen oppgaver i prosjektet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("TILORDNE OPPGAVE TIL MEDLEM")
        
        unassigned_tasks = [t for t in self.current_project.tasks if t.assigned_to is None]
        
        if not unassigned_tasks:
            print("Alle oppgaver er allerede tilordnet!")
            input("Trykk Enter for å fortsette...")
            return
        
        for i, task in enumerate(unassigned_tasks, 1):
            print(f"{i}. {task.title} ({task.hours} timer)")
        
        try:
            task_choice = int(input("\nVelg oppgave: ").strip())
            if 1 <= task_choice <= len(unassigned_tasks):
                task = unassigned_tasks[task_choice - 1]
                
                compatible = self.planner.get_compatible_members(self.current_project, task)
                
                if not compatible:
                    print("Ingen medlemmer med påkrevd kompetanse!")
                    input("Trykk Enter for å fortsette...")
                    return
                
                print(f"\nKompatible medlemmer for '{task.title}':")
                for i, member in enumerate(compatible, 1):
                    print(f"{i}. {member.name} ({member.available_hours} timer tilgjengelig)")
                
                member_choice = int(input("\nVelg medlem: ").strip())
                if 1 <= member_choice <= len(compatible):
                    member = compatible[member_choice - 1]
                    self.planner.assign_task_to_member(task, member)
                    print(f"\n✓ Oppgave '{task.title}' tilordnet til {member.name}!")
                else:
                    print("Ugyldig valg!")
        except ValueError:
            print("Vennligst skriv inn et tall!")
        
        input("Trykk Enter for å fortsette...")
    
    def show_organization_status(self):
        """Show organization status"""
        if not self.planner.get_organization():
            print("Ingen organisasjon opprettet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("ORGANISASJONSSTATUS")
        
        info = self.planner.get_organization_info()
        print(f"\nOrganisasjon: {info['name']}")
        print(f"Medlemmer: {info['members_count']}")
        print(f"Prosjekter: {info['projects_count']}")
        print(f"\nKvaliteter: {len(info['qualities'])}")
        for q in info['qualities']:
            print(f"  - {q}")
        print(f"\nBegrensninger: {len(info['constraints'])}")
        for c in info['constraints']:
            print(f"  - {c}")
        
        input("\nTrykk Enter for å fortsette...")
    
    def show_members(self):
        """Show all members"""
        members = self.planner.get_members()
        
        if not members:
            print("Ingen medlemmer opprettet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("ALLE MEDLEMMER")
        
        for member in members:
            print(f"\n{member.name} - {member.role}")
            print(f"  Tilgjengelige timer: {member.available_hours}")
            if member.qualities:
                print(f"  Kvaliteter: {', '.join(member.qualities)}")
            if member.constraints:
                print(f"  Begrensninger: {', '.join(member.constraints)}")
        
        input("\nTrykk Enter for å fortsette...")
    
    def show_org_qualities_constraints(self):
        """Show organization qualities and constraints"""
        org = self.planner.get_organization()
        
        self.print_header("KVALITETER OG BEGRENSNINGER")
        
        print("\nKvaliteter:")
        if org.qualities:
            for q in org.qualities:
                print(f"  - {q.name}: {q.description}")
        else:
            print("  Ingen kvaliteter definert")
        
        print("\nBegrensninger:")
        if org.constraints:
            for c in org.constraints:
                print(f"  - {c.name}: {c.description}")
        else:
            print("  Ingen begrensninger definert")
        
        input("\nTrykk Enter for å fortsette...")
    
    def show_projects(self):
        """Show all projects"""
        projects = self.planner.get_projects()
        
        if not projects:
            print("Ingen prosjekter opprettet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header("ALLE PROSJEKTER")
        
        for project in projects:
            summary = self.planner.get_project_summary(project)
            print(f"\n{summary['name']}")
            if summary['duration_weeks']:
                print(f"  Varighet: {summary['duration_weeks']} uker")
            print(f"  Oppgaver: {summary['tasks_count']}")
            print(f"  Medlemmer: {summary['members_count']}")
        
        input("\nTrykk Enter for å fortsette...")
    
    def show_tasks(self):
        """Show all tasks in current project"""
        if not self.current_project.tasks:
            print("Ingen oppgaver i prosjektet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header(f"OPPGAVER I {self.current_project.name}")
        
        for task in self.current_project.tasks:
            print(f"\n{task.title}")
            print(f"  Timer: {task.hours}")
            print(f"  Frist: {task.deadline}")
            print(f"  Status: {task.status}")
            if task.assigned_to:
                print(f"  Tilordnet: {task.assigned_to.name}")
            if task.required_qualities:
                print(f"  Kvaliteter: {', '.join(task.required_qualities)}")
        
        input("\nTrykk Enter for å fortsette...")
    
    def show_project_members(self):
        """Show all members in current project"""
        if not self.current_project.members:
            print("Ingen medlemmer i prosjektet!")
            input("Trykk Enter for å fortsette...")
            return
        
        self.print_header(f"MEDLEMMER I {self.current_project.name}")
        
        for member in self.current_project.members:
            print(f"\n{member.name} - {member.role}")
            print(f"  Tilgjengelige timer: {member.available_hours}")
            if member.qualities:
                print(f"  Kvaliteter: {', '.join(member.qualities)}")
        
        input("\nTrykk Enter for å fortsette...")
    
    def run(self):
        """Start the CLI"""
        self.clear_screen()
        print("\n" + "="*50)
        print("  VELKOMMEN TIL PROJECT PLANNER")
        print("="*50)
        print("\nVersion 0.1 - Basis Foundation")
        print("Prèm Enter for å begynne...")
        input()
        
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nApplikasjonen avbrøtt av bruker.")
        except Exception as e:
            print(f"\nFeil oppstod: {e}")
            import traceback
            traceback.print_exc()


def menu():
    """Legacy function for backward compatibility"""
    print("1. Lag organisasjon")
    print("2. Legg til medlem")
    print("3. Lag prosjekt")

