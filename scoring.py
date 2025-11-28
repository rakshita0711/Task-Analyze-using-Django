from datetime import date, datetime

def calculate_urgency(due_date):
    # ✅ Handle string → date conversion
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

    today = date.today()
    delta = (due_date - today).days

    if delta < 0:
        return 10
    elif delta == 0:
        return 9
    elif delta <= 3:
        return 7
    elif delta <= 7:
        return 5
    else:
        return 2



def calculate_effort_score(hours):
    if hours <= 1:
        return 10
    elif hours <= 3:
        return 7
    elif hours <= 6:
        return 4
    else:
        return 2


def calculate_dependency_bonus(deps):
    if not deps:
        return 0
    return min(len(deps), 5)  # cap at 5


def calculate_priority(task, strategy="smart"):
    urgency = calculate_urgency(task["due_date"])
    importance = task["importance"]
    effort = calculate_effort_score(task["estimated_hours"])
    deps = calculate_dependency_bonus(task.get("dependencies", []))

    # Strategies (assignment requires 4 sorting modes)
    if strategy == "fastest":
        return (effort * 0.6) + (urgency * 0.2) + (importance * 0.2)

    if strategy == "impact":
        return (importance * 0.7) + (urgency * 0.2) + (effort * 0.1)

    if strategy == "deadline":
        return (urgency * 0.7) + (importance * 0.2) + (effort * 0.1)

    # SMART BALANCE (default)
    return (
        importance * 0.4 +
        urgency * 0.3 +
        effort * 0.2 +
        deps * 0.1
    )
def has_cycle(task_id, dep_map, visited=set()):
    if task_id in visited:
        return True
    visited.add(task_id)
    for dep in dep_map.get(task_id, []):
        if has_cycle(dep, dep_map, visited):
            return True
    visited.remove(task_id)
    return False
