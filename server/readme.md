#installation

pip install fastapi
uvicorn main:app --reload --port 5000
DOCS: http://127.0.0.1:5000/docs



User {
    id: int
    username: str
    email: str
    hashed_password: str
    role: str  # "user" | "admin"
    created_at: datetime
    updated_at: datetime
}

Activity {
    id: int
    name: str
    description: str
    category: str  # "sport", "culture", "kids", "outdoor", etc.
    location: str
    is_outdoor: bool
    weather_condition: str  # "sunny", "rainy", "cloudy", "any"
    start_time: time
    end_time: time
    created_at: datetime
}

Vote {
    id: int
    user_id: int  # FK → User
    activity_id: int  # FK → Activity
    rank: int  # 1 = top choice
    created_at: datetime
}