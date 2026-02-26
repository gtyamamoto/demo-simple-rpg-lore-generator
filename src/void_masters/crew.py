from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from void_masters.tools.character_tool import CharacterInputTool

@CrewBase
class VoidMasters:
    """VoidMasters crew for RPG story generation"""

    # Define paths as class variables
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def validate_names(self, names):
        if not names:
            raise ValueError("At least one character name must be provided.")
        return names
    
    @before_kickoff
    def collect_inputs(self, inputs):
        print("Enter 'done' to exit.")
        
        # Get age, if age is not provided, ask for it
        age = inputs.get("age", "").strip().lower()
        if not age:
            age = input("Story age (medieval/modern/futuristic): ").strip().lower()
        while age not in ["medieval", "modern", "futuristic"]:
            if age == "done":
                raise SystemExit("Operation cancelled.")
            age = input("Invalid. Enter medieval, modern, or futuristic: ").strip().lower()

        # Get names, if names are not provided, ask for them
        names = inputs.get("names", [])
        if isinstance(names, str):
            names = [name.strip() for name in names.split(",") if name.strip()]
        if not names:
            names = []
            while True:
                name = input("Enter character name (or 'done' to finish): ").strip()
                if name.lower() == "done":
                    break
                if name:
                    names.append(name)

        # Inject into inputs
        inputs["age"] = age
        inputs["names"] = ", ".join(names)
        return inputs  # Must return inputs
    
    @agent
    def character_builder(self) -> Agent:
        return Agent(
            config=self.agents_config["character_builder"],  # ✅ Safe: loaded by @CrewBase
        )

    @agent
    def story_builder(self) -> Agent:
        return Agent(
            config=self.agents_config["story_builder"],  # ✅ Safe: loaded by @CrewBase
        )
    
    @agent
    def story_reviser(self) -> Agent:
        return Agent(
            config=self.agents_config["story_reviser"],  # ✅ Safe: loaded by @CrewBase
        )
    
    @task
    def compose_characters(self) -> Task:
        return Task(
            config=self.tasks_config["compose_characters"]  # ✅ Loaded from YAML
        )

    @task
    def compose_story(self) -> Task:
        return Task(
            config=self.tasks_config["compose_story"]  # ✅ Loaded from YAML
        )
    
    @task
    def revise_story(self) -> Task:
        return Task(
            config=self.tasks_config["revise_story"]  # ✅ Loaded from YAML
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # ✅ Auto-populated by @agent
            tasks=self.tasks,    # ✅ Auto-populated by @task
            process=Process.sequential,
            verbose=True
        )   