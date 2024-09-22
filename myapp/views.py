from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import UserProfile1
import sqlite3
import re

def chat_interface(request):
    return render(request, 'chat.html')

def get_user_data(request):
    user_input = request.GET.get('query', '').lower()
    return handle_query(user_input)

def handle_query(user_input):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Get all column names from the UserProfile1 table
    cursor.execute("PRAGMA table_info(myapp_userprofile1)")
    columns = [column[1] for column in cursor.fetchall()]

    fields = set()
    conditions = []
    specific_name = None

    # Map common terms to database fields
    field_mappings = {
        "name": "name",
        "age": "age",
        "email": "email",
        "bio": "bio",
        "skill": "skills",
        "location": "location",
        "job": "job_title",
        "experience": "years_experience",
    }

    # Check for specific name
    name_match = re.search(r'\b(\w+)\'s\b|\bof (\w+)\b|\babout (\w+)\b', user_input)
    if name_match:
        specific_name = next(group for group in name_match.groups() if group)
        conditions.append(f"name LIKE '%{specific_name}%'")

    # Identify requested fields
    for term, field in field_mappings.items():
        if term in user_input and field in columns:
            fields.add(field)

    # Handle specific conditions
    if "older than" in user_input or "younger than" in user_input:
        age = re.search(r'\d+', user_input)
        if age:
            age = int(age.group())
            operator = ">=" if "older" in user_input else "<="
            conditions.append(f"age {operator} {age}")
            fields.add("age")

    if "more than" in user_input and "experience" in user_input:
        years = re.search(r'\d+', user_input)
        if years:
            years = int(years.group())
            conditions.append(f"years_experience >= {years}")
            fields.add("years_experience")

    if "skill" in user_input:
        skill = re.search(r'skill\s+in\s+(\w+)', user_input)
        if skill:
            conditions.append(f"skills LIKE '%{skill.group(1)}%'")
            fields.add("skills")

    # If no specific fields are requested, return an error
    if not fields and not specific_name:
        return JsonResponse({"message": "Please specify what information you're looking for."})

    # If no specific fields are requested but a name is specified, return all fields for that person
    if not fields and specific_name:
        fields = set(columns)

    # Always include name field for reference
    fields.add("name")

    # Construct the SQL query
    query = f"SELECT {', '.join(fields)} FROM myapp_userprofile1"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query)
    results = [dict(zip(fields, row)) for row in cursor.fetchall()]

    conn.close()

    # If a specific name was requested, filter the results to only include that person
    if specific_name:
        results = [result for result in results if specific_name.lower() in result['name'].lower()]

    return format_response(results)

def format_response(data):
    if not data:
        return JsonResponse({"message": "No information found."})

    formatted_data = [{key.replace('_', ' ').title(): value for key, value in item.items()} for item in data]
    return JsonResponse({"results": formatted_data})