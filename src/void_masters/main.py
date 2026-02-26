#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from void_masters.crew import VoidMasters  # Replace with your crew class
from void_masters.api import run_server

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def train():
    """
    Train the crew for a given number of iterations.
    """
    print("🎓 Training Mode")
    age = input("Enter training age (e.g., medieval): ").strip()
    names = input("Enter training character names (comma-separated): ").strip()

    inputs = {
        'age': age,
        'names': names,
        'current_year': str(datetime.now().year)
    }

    try:
        VoidMasters().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew from a specific task.
    """
    try:
        task_id = sys.argv[1]
        VoidMasters().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution.
    """
    inputs = {
        'age': 'futuristic',
        'names': 'Neo, Trinity',
        'current_year': str(datetime.now().year)
    }
    try:
        VoidMasters().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with a JSON trigger payload.
    """
    import json
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Pass JSON as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON in trigger payload.")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "age": "medieval",
        "names": "Arthur, Merlin",
        "current_year": str(datetime.now().year)
    }

    try:
        result = VoidMasters().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


def run(host: str = "0.0.0.0", port: int = 8000):
    """CLI entrypoint that starts the API server."""
    run_server(host=host, port=port)



if __name__ == "__main__":
    # Example CLI usage: python main.py
    # For train: python main.py train 5 trained_data.pkl
    run()   