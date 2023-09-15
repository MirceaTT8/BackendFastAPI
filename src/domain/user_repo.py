class UserRepository:
    
    def __init__(self, persistance):
        self.persistance = persistance

    def create_user(self, user):
        return self.persistance.create_user(user)

    def read_users(self):
        return self.persistance.read_users()
    
    def read_user(self, username):
        return self.persistance.read_user(username)
    
    def delete_user(self, username):
        return self.persistance.delete_user(username)
    
    def update_user(self, username, field, new_data):
        return self.persistance.update_user(username, field, new_data)


# define a user object, with private fields
# user repo receives in constructor an object which
# knows how to save the users in a file or db
# create a config.json in which we can tell what ype of persistence we have