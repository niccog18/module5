What you'll do:

    Create a Student SQLAlchemy model:
        id (integer, primary key)
        name (string, required)
        email (string, unique, required)
        grade_level (integer, 1-12)
        gpa (float, optional)
        is_enrolled (boolean, default True)
        created_at (datetime, auto-generated)

    Create Pydantic schemas: StudentCreate, StudentUpdate (full), StudentPatch (partial), StudentResponse

    Implement all six CRUD endpoints:

        POST /students — with duplicate email handling (409)
    
        GET /students — with grade_level and is_enrolled filters
    
        GET /students/{id} — with 404 handling
    
        PUT /students/{id} — full replacement
    
        PATCH /students/{id} — partial update
    
        DELETE /students/{id} — with 204 response
    
    Use a get_student_or_404() helper function
    
    Test the complete CRUD cycle in Swagger UI

