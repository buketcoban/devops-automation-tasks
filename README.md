# DevOps Automation Task Set (EPAM)

A compact set of hands-on DevOps/automation tasks I completed during an EPAM DevOps trainee process.
This repository is kept as a portfolio of practical scripting work (Bash + Python) with real inputs/outputs.

## Highlights
- Bash automation & parsing (no extra packages where required)
- Python tooling (CLI args, logging, packaging, archives)
- Templates & config generation (Jinja2 + YAML)
- API integration (Flask + GitHub REST API)
- Reproducible runs with clear outputs

---

## Tasks

### epam1 — CSV normalization (Bash)
Normalize accounts.csv → accounts_new.csv:
- Name casing: first letter uppercase, rest lowercase
- Email rule: first letter of name + full surname (lowercase)
- Duplicate emails include location_id

Run:
    bash epam1/task1.sh epam1/accounts.csv

Output:
- accounts_new.csv

---

### epam2 — Test output → JSON (Bash + jq)
Parse output.txt and generate structured output.json.
Uses the repo-provided ./jq binary as required by the assignment.

Run:
    bash epam2/task2.sh epam2/output.txt

Output:
- output.json

---

### epam3 — passwd transforms (sed/awk)
Create passwd_new from a given passwd file using only sed and awk:
- Change shell for user saned to /bin/bash (AWK)
- Change shell for user avahi to /bin/bash (SED)
- Keep only 1st, 3rd, 5th, 7th columns using : delimiter
- Remove all lines containing the word daemon
- Change shell for all users with even UID to /bin/zsh
- Ensure passwd_new has no newline at EOF

Run:
    bash epam3/task_sedawk.sh epam3/passwd

Output:
- passwd_new

Note:
- If your script filename differs, update the command above to match your actual script.

---

### epam4 — Python structures (basics)
A set of small Python exercises (factorial, digit sum, palindrome, list commands, dict cleanup, set intersection, split/join).
Each task is implemented as a separate .py script inside epam4/.

Run (examples):
    python epam4/loop.py
    python epam4/digits.py
    python epam4/strings.py
    python epam4/lists.py
    python epam4/dicts.py
    python epam4/sets.py
    python epam4/split_join.py

Output:
- Printed results to stdout (per task requirements)

---

### epam5 — Snapshot CLI tool (psutil) + packaging
Task 1:
- A Python CLI tool that prints system snapshots to stdout and appends snapshots to a JSON file
- Default interval is 30 seconds (configurable)
- File is cleaned on start
- Snapshots are written one JSON object per line
- Uses argparse, time.sleep, and includes at least one class

Task 2:
- Package the tool as an installable CLI named snapshot (setup.py + README)

Run (script form example):
    python epam5/snapshot.py -i 1 -f snapshot.json -n 5

Run (installed tool example):
    pip install -U ./epam5
    snapshot -i 1

Output:
- snapshot.json (one JSON snapshot per line)

Note:
- If your entry script/package path differs, adjust the commands above accordingly.

---

### epam6 — Apache vhosts generator (Jinja2 + YAML)
Generate an Apache vhosts.conf from data.yml using a Jinja2 template vhosts.j2 and a Python script conf.py.
The generated config contains multiple <VirtualHost *:80> entries.

Run:
    python epam6/conf.py

Output:
- vhosts.conf (or generated/vhosts.conf depending on your folder structure)

Files expected in this task:
- epam6/vhosts.j2
- epam6/data.yml
- epam6/conf.py
- Generated vhosts.conf

---

### epam7 — Flask app: list boto3 pull requests (GitHub API)
A Flask web application that retrieves pull requests from https://github.com/boto/boto3 using GitHub REST API.
Supports:
- /pull_requests endpoint
- Query param state=open|closed
- Uses per_page=100
- Uses GitHub token from environment variable TOKEN

Run:
    export TOKEN="<your_token>"
    pip install -r epam7/requirements.txt
    python epam7/start.py

Open:
- http://127.0.0.1:5000/pull_requests
- http://127.0.0.1:5000/pull_requests?state=open
- http://127.0.0.1:5000/pull_requests?state=closed

---

### epam8 — Clean Python archive (zip + logging)
Clean a zip archive by removing folders without __init__.py (only root may lack __init__.py).
Creates cleaned.txt (always), and repackages as <old_name>_new.zip. Includes logging.

Run:
    python epam8/clean_app.py <zip-file-name>

Output:
- <old_name>_new.zip
- cleaned.txt

---

## Notes
- This is a task collection repo: each folder is self-contained.
- No secrets are stored in the repository; token-based tasks use environment variables.
