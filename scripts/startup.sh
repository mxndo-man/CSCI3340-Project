# This script is mainly just so we dont have to run the following commands constantly
#
# Mando - I am using linux so the steps might differ.
# The easiest way of doing is is going to the terminal in vscode and putting your terminal as git bash: pls do this
#
# In order to run this script:
# 1. chmod +x /scrips/startup.sh 
#   chmod - change mode of file 
#   + - An addition of permisions
#   x - flag that stands for execute
# 2. To run it simply do 
#   /scripts/startup.sh

PORT="${1:-8000}" # Default port of django

echo "Starting server"
set -e 
uv sync 
uv run python manage.py migrate 
uv run python manage.py runserver "127.0.0.1:$PORT" 
# To change the port if you NEED a custom one then do 
# ./scripts/startup.sh "PORT"
