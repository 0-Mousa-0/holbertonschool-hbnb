from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def get_all_users(self):
        """ Retrieve a list of all users """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """ Updates user data using your User class """
        user = self.get_user(user_id)
        if not user:
            return None

        # Using the profileUpdate method from your class
        # We use .get() to avoid errors if the user doesn't send all fields
        user.profileUpdate(
            firstName=user_data.get('firstName'),
            lastName=user_data.get('lastName'),
            email=user_data.get('email')
        )

        self.user_repo.update(user.id, user)
        return user
