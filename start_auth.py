import sys
from get_auth import *
from db_crud import *

if __name__ == "__main__":
    # print(sys.argv)
    if len(sys.argv) != 3:
        print("Insufficient arguments")
        
    mallid = sys.argv[1]
    auth_code = sys.argv[2]
    
    get_auth(mallid, auth_code)