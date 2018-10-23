#!/usr/bin/env bash

# https://stackoverflow.com/questions/13692519/linux-bash-script-running-multiple-python
# python3 "./MinerServer.py" -p 5000 &
# python3 "./MinerServer.py" -p 5010 &

python3 "./MinerClient.py" -i 5000 &
python3 "./MinerClient.py" -i 5010 &

exit 0
