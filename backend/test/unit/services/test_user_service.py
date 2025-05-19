
async def test_create_user_success(db_session):
    user_data = UserCreate(full_name="Test", phone_number="+1234567890", password="pass123")
    user = await UserService(db_session).create_user(user_data)
    assert user.phone_number == "+1234567890"

async def test_create_user_duplicate_phone(db_session):
    user_data = UserCreate(...)
    await UserService(db_session).create_user(user_data)
    with pytest.raises(ValueError, match="already exists"):
        await UserService(db_session).create_user(user_data)  # Дубликат