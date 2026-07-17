class TestCreateBook:
    """Tests for POST /books"""

    def test_create_book_success(self, client):
        response = client.post("/books", json={
            "title": "Python Basics",
            "author": "John Doe",
            "price": 29.99
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Python Basics"
        assert "id" in data
        assert "created_at" in data

    def test_create_book_missing_title(self, client):
        response = client.post("/books", json={"author": "John Doe", "price": 29.99})
        assert response.status_code == 422

    def test_create_book_negative_price(self, client):
        response = client.post("/books", json={"title": "Free Book", "author": "Author", "price": -5.00})
        assert response.status_code == 422

    def test_create_book_empty_title(self, client):
        response = client.post("/books", json={"title": "", "author": "Author", "price": 10.00})
        assert response.status_code == 422

class TestReadBooks:
    """Tests for GET /books and GET /books/{id}"""

    def test_list_books_empty(self, client):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_books_with_data(self, client, sample_book):
        response = client.get("/books")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_book_by_id(self, client, sample_book):
        response = client.get(f"/books/{sample_book['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Book"

    def test_get_book_not_found(self, client):
        response = client.get("/books/9999")
        assert response.status_code == 404

class TestUpdateBook:
    """Tests for PATCH /books/{id}"""

    def test_patch_book_title(self, client, sample_book):
        response = client.patch(f"/books/{sample_book['id']}", json={"title": "Updated Title"})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["author"] == "Test Author"  # Unchanged

    def test_patch_nonexistent_book(self, client):
        response = client.patch("/books/9999", json={"title": "Nope"})
        assert response.status_code == 404

class TestDeleteBook:
    """Tests for DELETE /books/{id}"""

    def test_delete_book(self, client, sample_book):
        response = client.delete(f"/books/{sample_book['id']}")
        assert response.status_code == 204
        # Verify it's gone
        response = client.get(f"/books/{sample_book['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_book(self, client):
        response = client.delete("/books/9999")
        assert response.status_code == 404
