class User():
    def __init__(self, username, email, password):
        self.username = username
        self._email = email
        self.password = password
    
    def clean_email(self):
        ce = self._email.lower().strip()
        print(ce)
        return ce
    
    def get_email(self):
        return self._email

    

u1 = User("bobby", "  daN@gMAIl.com ", "123")

print(u1.get_email())
        
        