# Prompt Playbook v1

## Objective
Capture empirical observations comparing prompt variants and model behaviors. Use this as a living artifact you will refine in future weeks.

## How to Use This File
1. After each script run, append rows to the Results Table.
2. Tag failure modes (see legend) so patterns emerge quickly.
3. Summarize insights after completing stretch assignments.

## Scoring Rubric (1–5)
| Score | Instruction Adherence | Reasoning Depth | Style / Persona | Format Fidelity |
|-------|-----------------------|-----------------|-----------------|-----------------|
| 1 | Misses key directives | Single sentence | Ignores persona | Broken / ignores |
| 3 | Mostly follows | Some steps implicit | Partial persona | Minor drift |
| 5 | Precise & complete | Clear multi-step chain | Fully consistent | Exact, parsable |

## Failure Mode Tags
hallucination, verbosity, shallow, drift (format), persona-loss, json-break, constraint-fail

## Results Table (Populate During Lab)
| Prompt Pattern | Example Used | Model | Adherence (1–5) | Reasoning (1–5) | Style (1–5) | Format (1–5) | Failure Modes | Notes | Reuse? (Y/N) |
|----------------|--------------|-------|------------------|-----------------|-------------|--------------|---------------|-------|--------------|
Simple| Explain photosynthesis|llama3|5|5|5|5|verbosity|Provides a detailed explanation.|Y
Simple|Explain Photosynthesis|Mistral|3|3|3|5|shallow|Provides more detailed general explanation for the concept of photosynthesis but not in the breakdown of the summary.|Y
Simple|Explain Photosynthesis|Open AI|5|5|5|5|verbosity|Good expalanation, a bit summarized the explanation.|Y
Simple|Explain Photosynthesis|Gemini|5|5|5|5|verbosity|Is the most detailed and elaborate explanation, why I say verbosity, because adds an equation which is quite complex for an initial research.|Y
Role|You are a biology professor. Explain photosynthesis to a high school student.|llama3|3|5|3|5|shallow, persona-losss|It assummed that the student already knew about photosynthesis concepts, so it missed an initial explanation of the concept.|N
Role|You are a biology professor. Explain photosynthesis to a high school student.|Mistral|5|3|3|5|shallow,persona-loss|The response is a good complement for the response given by llama3.|N
Role|You are a biology professor. Explain photosynthesis to a high school student.|OpenAI|5|5|5|5|no failures|Excellent explanation, kept the role and even provided a fun fact in the answer.|Y
Role|You are a biology professor. Explain photosynthesis to a high school student.|Gemini|5|5|5|5|no failures|Good detailed explanation, it even provided supporting materials for students to further see details.|Y
Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs|llama3|3|5|5|5|shallow|Does not explain the concept, jumps directly to inputs and outputs.|N
Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs|Mistral|5|5|3|5|shallow|I see shallow answer since if fails to give a step by step explanation as llama3 did, but overall is a much better answer than llama3 provided.  It gave explanation of the concept, details of stages and clear inpunts and outputs.|Y
Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs|OpenAI|5|5|5|5|no failure|Step by step explanation adding inputs and outputs providing good details of the concept.  And a final one line summary.|Y
Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs|Gemini|5|5|5|5|no failures|Maybe this reponse is a bit better than Open AI since it explains the concept first and then complements very well with inputs and outputs.  But there is no summary of the overall concept.|Y
## Model Summary (After Initial Pass)
| Capability | Best Model(s) | Evidence Snippet | Notes |
|------------|---------------|------------------|-------|
| Explanatory Clarity | | | |
| Chain-of-Thought | | | |
| JSON Adherence | | | |
| Persona Control | | | |
| Instruction Strictness | | | |

## Insight Log
Record notable surprises, regressions, or improvements.
- Day 1:
- Day 2:
- Day 3:

---

### 1. Role Prompting

*   **Best Practice:**
    *   Clearly define the persona or role you want the AI to adopt. This helps to set the context, tone, and level of detail in the response.
*   **Example:**
    *   Instead of "Explain black holes," use "You are an astrophysicist. Explain the concept of a black hole to a curious 10-year-old."

---

### 2. Few-Shot Learning

*   **Best Practice:**
    *   Provide a few examples of the desired input and output format. This is especially useful for tasks like classification, summarization, or code generation.
*   **Example:**
    *   When asking for a summary, provide one or two examples of a text and its corresponding summary before providing the text you want to be summarized.

---

### 3. Chain-of-Thought (CoT)

*   **Best Practice:**
    *   Encourage the model to "think step by step" or to "show its work." This is particularly effective for complex reasoning tasks, such as math problems or logic puzzles.
*   **Example:**
    *   Append "Let's think step by step" to your prompt when you need the model to reason through a problem.

---

### 4. Anti-Patterns to Avoid
## Reflection (End of Week)
Answer briefly:
1. Which two prompt patterns yielded the largest delta between models?
2. Which failure mode was most frequent? Root cause?
3. Default model choice for: explanation / reasoning / structure.
4. Open questions heading into Week 2.
*   **Ambiguity:**
    *   Avoid vague or open-ended questions. Be as specific as possible.
*   **Leading Questions:**
    *   Don't phrase your prompt in a way that suggests a desired answer.
*   **Overly Complex Prompts:**
    *   Break down complex tasks into smaller, more manageable prompts.

---
