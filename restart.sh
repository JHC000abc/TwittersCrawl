#! /bin/bash


export python_env=$(pwd)/.venv/bin/python3
export celery_env=$(pwd)/.venv/bin/celery

source $(pwd)/.venv/bin/activate

# 删除已有日志
rm -rf $(pwd)/logs
mkdir -p $(pwd)/logs

pgrep -af TelegramBot | awk '{print $1}' | xargs kill -9
pgrep -af celery | awk '{print $1}' | xargs kill -9
pgrep -af login_accounts | awk '{print $1}' | xargs kill -9

nohup $celery_env -A tasks worker --loglevel=info --pool=threads --concurrency=4  >> logs/work_$(date +\%Y-\%m-\%d).log 2>&1 < /dev/null &
nohup $celery_env -A tasks beat --loglevel=info > logs/tasks_$(date +\%Y-\%m-\%d).log 2>&1 < /dev/null &
# 启动机器人
#nohup $python_env $(pwd)/TelegramBot.py > logs/TelegramBot_$(date +\%Y-\%m-\%d).log 2>&1 < /dev/null &
# 预登陆
#nohup $python_env $(pwd)/login_accounts.py > logs/login_accounts_$(date +\%Y-\%m-\%d).log 2>&1 < /dev/null &
