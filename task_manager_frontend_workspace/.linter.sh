#!/bin/bash
cd /home/kavia/workspace/code-generation/taskflow-web-28219-192d3016/task_manager_frontend_workspace/task_manager_frontend
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

