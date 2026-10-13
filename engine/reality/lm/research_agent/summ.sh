#!/bin/bash
cd /home/user/SomeRepository/engine/reality/lm/research_agent
for f in *.json; do python3 -c "import json;r=json.load(open('$f'));print('%-28s'%'$f',r.get('params'),r.get('train_s'),r.get('bpc'),r.get('bpc_2x'),r.get('error',''))"; done
