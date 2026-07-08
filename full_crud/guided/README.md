Testing the Full CRUD Cycle

In Swagger UI, walk through the complete lifecycle:

    POST /books — Create a book. Note the 201 status and the returned id.
    GET /books — Verify it appears in the list.
    GET /books/1 — Retrieve it by ID.
    PATCH /books/1 — Send {"price": 29.99}. Only the price changes.
    PUT /books/1 — Send the complete updated book data.
    DELETE /books/1 — Remove it. Note the 204 with no body.
    GET /books/1 — Verify it returns 404.