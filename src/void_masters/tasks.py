import os
import json
from datetime import datetime
from typing import Dict

from void_masters.crew import VoidMasters

# in-memory store for task metadata
TASKS: Dict[str, dict] = {}


def _save_result_markdown(task_id: str, inputs: dict, result) -> str:
    """Save the task result to a well-formatted Markdown file and return the path."""
    out_dir = os.path.join(os.getcwd(), "craft_results")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = f"craft_{task_id}_{ts}.md"
    path = os.path.join(out_dir, filename)

    try:
        # pretty-print result as JSON if possible
        try:
            pretty = json.dumps(result, ensure_ascii=False, indent=2)
            result_block = f"```json\n{pretty}\n```"
        except Exception:
            result_block = f"```\n{str(result)}\n```"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Craft Result\n\n")
            f.write(f"- Task ID: {task_id}\n")
            f.write(f"- Age: {inputs.get('age')}\n")
            f.write(f"- Names: {inputs.get('names_array') or inputs.get('names')}\n")
            f.write(f"- Started: {datetime.now().isoformat()}\n\n")
            f.write("## Result\n\n")
            f.write(result_block)

        return path
    except Exception:
        return ""



def run_task_background(task_id: str, inputs: dict):
    """Execute the crew kickoff in background and update TASKS with results."""
    TASKS[task_id]["status"] = "running"
    TASKS[task_id]["started_at"] = datetime.now().isoformat()
    try:
        result = VoidMasters().crew().kickoff(inputs=inputs)
        TASKS[task_id]["status"] = "completed"
        TASKS[task_id]["finished_at"] = datetime.now().isoformat()
        path = _save_result_markdown(task_id, inputs, result)
        TASKS[task_id]["output_path"] = path
        TASKS[task_id]["result"] = result
    except Exception as e:
        TASKS[task_id]["status"] = "failed"
        TASKS[task_id]["finished_at"] = datetime.now().isoformat()
        TASKS[task_id]["error"] = str(e)
