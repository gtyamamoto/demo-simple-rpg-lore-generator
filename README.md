# VoidMasters Crew

Welcome to the VoidMasters Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/void_masters/config/agents.yaml` to define your agents
- Modify `src/void_masters/config/tasks.yaml` to define your tasks
- Modify `src/void_masters/crew.py` to add your own logic, tools and specific args
- Modify `src/void_masters/main.py` to add custom inputs for your agents and tasks

## Running the Project

This repository contains an AI story-telling service built on top of crewAI. The
`void_masters` crew is normally run via the CLI but also exposes an HTTP API
that you can call from other applications.

### CLI mode

To kickstart your crew of AI agents and begin task execution, run this from the
root folder of your project:

```bash
$ crewai run
# or equivalently:
$ python -m void_masters.main
```

The `crewai run` (or `python -m void_masters.main`) command initializes the
void-masters crew, assembling the agents and assigning them tasks as defined in
your configuration files (`config/agents.yaml` and `config/tasks.yaml`).

With the stock configuration the crew will generate a short story and write it
into `report.md` in the workspace root.

### API mode

The project also includes a lightweight HTTP server that exposes the crew as a
service. Start it with:

```bash
$ python -m void_masters.main serve
# or using the installed script
$ serve
```

By default the server listens on `0.0.0.0:8000`.

#### Endpoints

- `POST /craft` – submit a story creation request. Accepts a JSON body:
  ```json
  { "age": "medieval", "names": ["Alice","Bob"] }
  ```
  Returns `202 Accepted` with `{"status":"accepted","task_id":"..."}`.
  The crew will run asynchronously and save the result to a Markdown file.

- `GET /craft/status?task_id=<id>` – query the current status of a task (queued,
  running, completed, failed) and metadata including an `output_path` when done.

- `GET /craft/download?task_id=<id>` – once completed, download the generated
  Markdown result as an attachment.

This API makes it easy to integrate the story-telling crew into web
applications or automation pipelines.

### Example integration

```bash
# create a task
TASK=$(curl -s \
  -X POST http://localhost:8000/craft \
  -H "Content-Type: application/json" \
  -d '{"age":"ancient","names":["Zeus","Hera"]}' | jq -r .task_id)

# poll until finished
while :; do
  S=$(curl -s "http://localhost:8000/craft/status?task_id=$TASK" | jq -r .task.status)
  echo "status=$S"; [[ $S != queued && $S != running ]] && break
  sleep 1
done

# download
curl -O -J "http://localhost:8000/craft/download?task_id=$TASK"
```


## Understanding Your Crew

The void-masters Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the VoidMasters Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
