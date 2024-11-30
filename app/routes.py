from fastapi import APIRouter, Body, HTTPException, Query, Path
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from .database import (
    student_collection,
    student_helper,
)
from .models import StudentModel, UpdateStudentModel
from bson import ObjectId

router = APIRouter()

@router.post("/", response_description="Add new student", status_code=201, summary="Create Students", description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.")
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await student_collection.insert_one(student)
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})
    return {"id": str(created_student["_id"])}

@router.get("/", response_description="List all students", summary="List students", description="An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.")
async def get_students(country: Optional[str] = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."), age: Optional[int] = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    students = []
    async for student in student_collection.find(query):
        students.append(student_helper(student))
    return {"data": students}

@router.get("/{id}", response_description="Get a single student", summary="Fetch student", description="API to fetch the details of a student using the student's ID.")
async def get_student(id: str = Path(..., description="The ID of the student previously created")):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)
    raise HTTPException(status_code=404, detail="Student not found")

@router.patch("/{id}", response_description="Update a student", status_code=204, summary="Update student", description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.")
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    update_data = student.dict(exclude_unset=True)
    
    # Retrieve existing student data
    existing_student = await student_collection.find_one({"_id": ObjectId(id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update fields in the existing data
    if "address" in update_data:
        existing_address = existing_student.get("address", {})
        new_address = update_data["address"]
        existing_address.update(new_address)
        update_data["address"] = existing_address
    
    update_result = await student_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    if update_result.modified_count == 1:
        return {"message": "Student updated successfully"}
    
    return {"message": "No changes made"}

@router.delete("/{id}", response_description="Delete a student", summary="Delete student", description="API to delete a student from the system using the student's ID.")
async def delete_student(id: str = Path(..., description="The ID of the student previously created")):
    delete_result = await student_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")
