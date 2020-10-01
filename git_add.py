import os,subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("loc", 
                    help="Add complete path of the repository to update")
parser.add_argument("-b","--branch", 
                    help="branch name for push and pull",
                    default="master")
parser.add_argument("-m","--message", 
                    help="commit message",
                    default=" ")

args = parser.parse_args()

try:
    os.chdir(f"/{args.loc}")
    
    # attempt to add    
    subprocess.check_output("git add .", shell=True)  
    returned_value = subprocess.check_output("git status -s", shell=True) 
    if returned_value==b'':
        print("Nothing to add")
    else:
        print('updated files:', returned_value)

    # commit
    if not returned_value==b'':

        if args.branch !="master":
            subprocess.check_output(f"git checkout -b {args.branch}", shell=True)  
        commit_message='Added/Updated Following files '

        if len(str(returned_value).split(r'\n'))>0:        
            for file_name in str(returned_value).split(r'\n'):
                commit_message=commit_message+file_name[5:]+" "
            if args.message ==" ":
                cmd = f'git commit -m "{commit_message}"'
            else:
                cmd = f'git commit -m "{args.message}"'

            print("Commit message ",subprocess.check_output(cmd, shell=True))

    # pull 
    try:
        cmd = f"git pull origin {args.branch}"
        returned_value = subprocess.check_output(cmd, shell=True)
    except:
        print("Pull failed")
    finally:
        # push 
        try:
            cmd= f"git push origin {args.branch}"
            result = subprocess.check_output(cmd, shell=True)
            print(result) 
        except:
            print("Push Failed")
except:
    print(f"Path {args.loc}, does not exsist")
