''' Main python file - selects and runs the appropriate function based on ROLE '''

from constants import ROLE

if ROLE == "R":
    from server import main
    main()

elif ROLE == "S":
    from api_client import main
    main()

elif ROLE == "US":
    from user_client import main
    main()

else:
    print(f"Invalid role: {ROLE}")