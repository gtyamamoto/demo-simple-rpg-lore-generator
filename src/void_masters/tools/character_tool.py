from crewai.tools import BaseTool

class CharacterInputTool(BaseTool):
    name: str = "Character and Setting Input"
    description: str = "Collect story age (medieval/modern/futuristic) and character names until 'done' is entered."

    def _run(self, prompt: str) -> dict:
        print("Enter 'done' at any time to stop input.")
        age = input("Enter story age (medieval, modern, futuristic): ").strip().lower()
        while age not in ["medieval", "modern", "futuristic"]:
            if age == "done":
                return {"age": None, "names": []}
            age = input("Please enter a valid age (medieval, modern, futuristic): ").strip().lower()

        names = []
        while True:
            name = input("Enter a character name (or 'done' to finish): ").strip()
            if name.lower() == "done":
                break
            if name:
                names.append(name)

        return {"age": age, "names": names}   