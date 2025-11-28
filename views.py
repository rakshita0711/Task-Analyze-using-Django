from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .scoring import calculate_priority
from datetime import date, datetime


@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    results = []

    for t in tasks:
        score = calculate_priority(t, strategy)
        t["score"] = round(score, 2)

        # Convert due_date string → date object
        due_date = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
        due_days = (due_date - date.today()).days

        reason_parts = []

        if due_days < 0:
            reason_parts.append(f"Overdue by {abs(due_days)} day(s)")
        else:
            reason_parts.append(f"Due in {due_days} day(s)")

        reason_parts.append(f"Importance {t['importance']} / 10")
        reason_parts.append(f"Effort {t['estimated_hours']} hrs")
        reason_parts.append(f"Dependencies {len(t.get('dependencies', []))}")

        t["reason"] = ", ".join(reason_parts)

        results.append(t)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return Response(results)


@api_view(["GET"])
def suggest_tasks(request):
    tasks = request.data.get("tasks", [])
    scored = []

    for t in tasks:
        score = calculate_priority(t, "smart")
        t["score"] = round(score, 2)
        scored.append(t)

    top3 = sorted(scored, key=lambda x: x["score"], reverse=True)[:3]
    return Response(top3)
