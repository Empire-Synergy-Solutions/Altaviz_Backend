ERROR = 'Error'
SUCCESS = 'Success'

# Permissions
PERMISSION_ADMINISTRATOR_REQUIRED = 'Administrator permissions needed'
PERMISSION_MODERATOR_REQUIRED = 'Moderator permissions needed'
PERMISSION_ATTENDANT_REQUIRED = 'Gas Attendant\'s permissions needed'
PERMISSION_MANAGERS_REQUIRED = 'Manager\'s permissions needed'
PERMISSION_VENDOR_REQUIRED = 'vendor\'s permissions needed'
PERMISSION_CUSTOMERS_REQUIRED = 'customer\'s permissions needed'

# User roles
USER_ROLE_ADMINISTRATOR = 'administrator'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_ATTENDANTS = 'attendants'
USER_ROLE_CUSTOMERS = 'customers'
USER_ROLE_VENDORS = 'vendors'
USER_ROLE_MANAGERS = 'managers'

# Votes
VOTE_UP = 1
VOTE_DOWN = -1
VOTE_VALUE_CHOICES = (
    (VOTE_UP, 'Up'),
    (VOTE_DOWN, 'Down')
)
