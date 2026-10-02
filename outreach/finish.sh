#!/bin/bash
# Usage: bash outreach/finish.sh <idx> <msgId> <threadId> [commit message]
set -e
cd /home/user/scouting001
python3 outreach/outreach.py record "$1" "$2" "$3"
git add -A outreach *.xlsx
git commit -qm "${4:-Outreach: record send $1}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XwQBoB1SBrvgpAdZTTqNbP"
git push -q origin claude/trading-bot-prospects-coemnz
echo ok
