from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    Category
)


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


contacts = []

@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate):

    new_contact = {
        "id": len(contacts) + 1,
        **contact.model_dump(),
        "created_at": datetime.now().isoformat()
    }

    contacts.append(new_contact)

    return new_contact


@router.get("/", response_model=list[ContactResponse])
def get_contacts(category: Category | None = None):

    if category:
        return [
            contact
            for contact in contacts
            if contact["category"] == category
        ]

    return contacts


@router.get("/{id}", response_model=ContactResponse)
def get_contact(id: int):

    for contact in contacts:
        if contact["id"] == id:
            return contact

    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )


@router.patch("/{id}", response_model=ContactResponse)
def update_contact(id: int, updated_contact: ContactUpdate):

    for contact in contacts:

        if contact["id"] == id:

            updates = updated_contact.model_dump(
                exclude_unset=True
            )

            contact.update(updates)

            return contact


    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )