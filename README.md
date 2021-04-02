# red-app

python3 -m venv env

pip install -r requirements.txt


first console:
  export FLASK_APP=runner
  flask run
  
  
second console:
  python coordinator.py -h -> for help
  python coordinator.py get -> get os and cpu data 
  python coordinator.py clone {one argument from the list} -> clones selected repo and builds them 
  python coordinator.py clean_repo {one argument from the list} -> remove selected repo


