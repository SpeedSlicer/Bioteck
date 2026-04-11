
#!/bin/bash
pkill -f main.py

# start Flask
python3 main.py > flask.log 2>&1 &
