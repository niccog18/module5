"""
Tests for Student CRUD endpoints.

Covered scenarios:
- Creating students
- Listing students
- Retrieving students by ID
- Updating students
- Patching students
- Deleting students
- Validation errors
- Duplicate email handling
- Authentication protection
"""

import pytest


# -----------------------------
# Test data
# -----------------------------

student_payload = {
    "name": "John Smith",
    "email": "johnsmith@test.com",
    "grade_level": 10,
    "gpa": 3.8,
    "is_enrolled": True
}


# -----------------------------
# CREATE STUDENT
# -----------------------------

def test_create_student(client, auth_headers):
    """
    Test creating a new student.

    Verifies:
    - Student creation succeeds
    - Response status is 201 Created
    - Returned data matches submitted student information
    """

    response = client.post(
        "/students/",
        headers=auth_headers,
        json=student_payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John Smith"
    assert data["email"] == "johnsmith@test.com"
    assert data["grade_level"] == 10
    assert data["gpa"] == 3.8


# -----------------------------
# GET ALL STUDENTS
# -----------------------------

def test_get_students(client, auth_headers):
    """
    Test retrieving all students.

    Verifies:
    - Response status is 200 OK
    - Response returns a list of students
    """

    response = client.get(
        "/students/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_get_student_not_found(client, auth_headers):
    """
    Test retrieving a student that does not exist.

    Verifies:
    - Response status is 404 Not Found
    """
    response = client.get(
        "/students/99999",
        headers=auth_headers
    )

    assert response.status_code == 404


# -----------------------------
# GET STUDENT BY ID
# -----------------------------

def test_get_student_by_id(client, auth_headers):
    """
    Test retrieving a student by ID.

    Verifies:
    - A student can be created
    - The created student can be retrieved
    - Response status is 200 OK
    """
    create_response = client.post(
        "/students/",
        headers=auth_headers,
        json=student_payload
    )
    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

# -----------------------------
# UPDATE STUDENT (PUT)
# -----------------------------

def test_update_student(client, auth_headers):
    """
    Test replacing a student record.

    Verifies:
    - Existing student records can be updated
    - Updated values are returned
    - Response status is 200 OK
    """
    create_response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            **student_payload,
            "email": "update@test.com"
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]


    updated_student = {
        "name": "Updated Student",
        "email": "update@test.com",
        "grade_level": 11,
        "gpa": 4.0,
        "is_enrolled": True
    }


    response = client.put(
        f"/students/{student_id}",
        headers=auth_headers,
        json=updated_student
    )


    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Student"
    assert data["grade_level"] == 11


def test_update_student_not_found(client, auth_headers):
    """
    Test updating a student that does not exist.

    Verifies:
    - Response status is 404 Not Found
    """

    response = client.put(
        "/students/99999",
        headers=auth_headers,
        json={
            "name": "Missing Student",
            "email": "missing@test.com",
            "grade_level": 10,
            "gpa": 3.5,
            "is_enrolled": True,
        },
    )

    assert response.status_code == 404


# -----------------------------
# PATCH STUDENT
# -----------------------------

def test_patch_student(client, auth_headers):
    """
    Test partially updating a student.

    Verifies:
    - Student can be updated using PATCH
    - Updated fields are returned
    """

    create_response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            **student_payload,
            "email": "patch@test.com"
        }
    )
    assert create_response.status_code == 201

    student_id = create_response.json()["id"]


    response = client.patch(
    f"/students/{student_id}",
    headers=auth_headers,
    json={
        **student_payload,
        "email": "patch@test.com",
        "gpa": 3.5
    }
)

    assert response.status_code == 200

    data = response.json()

    assert data["gpa"] == 3.5


# -----------------------------
# DELETE STUDENT
# -----------------------------

def test_delete_student(client, auth_headers):
    """
    Test deleting a student.

    Verifies:
    - Student deletion succeeds
    - Response status is 204 No Content
    - Deleted student cannot be retrieved afterward
    """

    create_response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            **student_payload,
            "email": "delete@test.com"
        }
    )
    assert create_response.status_code == 201

    student_id = create_response.json()["id"]


    response = client.delete(
        f"/students/{student_id}",
        headers=auth_headers
    )


    assert response.status_code == 204


    # Confirm deletion

    get_response = client.get(
        f"/students/{student_id}",
        headers=auth_headers
    )


    assert get_response.status_code == 404



# -----------------------------
# VALIDATION TESTS
# -----------------------------

def test_invalid_grade_level(client, auth_headers):
    """
    Test student creation with an invalid grade level.

    Verifies:
    - Grade level validation rejects values outside 1-12
    - Response status is 422 Unprocessable Entity
    """

    response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            "name": "Bad Grade",
            "email": "badgrade@test.com",
            "grade_level": 15,
            "gpa": 3.0,
            "is_enrolled": True
        }
    )


    assert response.status_code == 422



def test_duplicate_email(client, auth_headers):
    """
    Test duplicate email handling.

    Verifies:
    - Creating a student with an existing email fails
    - Response status is 409 Conflict
    """

    client.post(
        "/students/",
        headers=auth_headers,
        json={
            **student_payload,
            "email": "duplicate@test.com"
        }
    )


    response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            **student_payload,
            "email": "duplicate@test.com"
        }
    )


    assert response.status_code == 409


def test_create_student_without_token(client):
    """
    Test protected endpoint authentication.

    Verifies:
    - Creating a student without an authorization token
      returns 401 Unauthorized
    """

    response = client.post(
        "/students/",
        json={
            "name": "No Auth",
            "email": "noauth@test.com",
            "grade_level": 10,
            "gpa": 3.5,
            "is_enrolled": True,
        },
    )

    assert response.status_code == 401


def test_invalid_gpa(client, auth_headers):
    """
    Test student creation with an invalid GPA.

    Verifies:
    - GPA validation rejects values above 4.0
    - Response status is 422 Unprocessable Entity
    """

    response = client.post(
        "/students/",
        headers=auth_headers,
        json={
            "name": "Bad GPA",
            "email": "badgpa@test.com",
            "grade_level": 10,
            "gpa": 5.5,
            "is_enrolled": True,
        },
    )

    assert response.status_code == 422