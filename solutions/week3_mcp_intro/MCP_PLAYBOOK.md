# MCP Playbook v1

## 1. Evaluation & Logging
Log rows in `PROMPT_PLAYBOOK.md` (Week 3 section):
| Query | Intent | Tool Used? | Params | Latency (ms) | Success | Notes |
|--------|---------|-------------|----------|---------------|-----------|--------|
| What is the temperature in Paris? | get_weather | true | Paris | 0.2932548522949219 | True | Good response — the answer was *Weather for Paris: 22.2°C, Windy.* |
| What's the weather in dollars? | get_weather | true | dollars | 0.025272369384765625 | True | The response is given, but the parameter is not a city. |
| What is the time in Cairo? | null | false | none | 0.0 | true | It explains that the query passed does not meet the required criteria. |
| Simple prompt, What is the weather in Egypt? | get_weather | true | Egypt | — | True | Using week 1 script with simple prompt provides a far better response using Ollama 3 and Ollama Mistral LLMs. |
| Used Rag python script to ask for weather in El Cairo. | get_weather | true | El Cairo | — | True | With the current context in the script not related to the weather in El Cairo, the response explains that there is no context related to the query. |
