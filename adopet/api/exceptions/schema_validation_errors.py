class PhoneNumberException(ValueError):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "Please provide a valid mobile phone number"
