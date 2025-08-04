PSE1: 
Level 1: LLM-Only Smart Assistant
Called using chatbot.py
Refuses to solve Mathematical Operations and Hints to calculator

PSE2: 
Level 2: LLM + Calculation
Handles LLM + Basic Tool
If Mathematical Calculation Detected, LLM calls Calculator tool, Graceful Failure for Multi Step 
Called Using chatbot_with_tool.py

PSE3:
Level 3: Full Agentic AI with Multi-step Tasks
Performs multi-step reasoning
Can answer complex prompts like:
“Translate 'Hello' to German and then multiply 4 and 5”
Step-by-step results are displayed
Called Using full_agent.py


Each level itself consists of its README.md File which consists of System Instruction
Install Packages using
pip install -r requirements.txt
