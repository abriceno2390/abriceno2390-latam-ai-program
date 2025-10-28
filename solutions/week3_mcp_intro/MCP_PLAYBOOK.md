# MCP Playbook v1

## 1. Evaluation & Logging
Log rows in `PROMPT_PLAYBOOK.md` (Week 3 section):
| Query What is the temperature in Paris? What's the weather in dollars ? What is the time in Cairo? | Intent get_weather get_weather null| Tool Used? true true false| Params Paris dollars none | Latency ms 0.2932548522949219 0.025272369384765625 0.0 | Success True True true | Notes Good response, the answer was Weather for Paris: 22.2\u00b0C, Windy. The response is given but the parameter is not a city. It explains that the query passed does not meet the required criteria.|
|-------|--------|------------|--------|------------|---------|-------|