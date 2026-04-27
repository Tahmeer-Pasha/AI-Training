# Prompt Engineering Assignment

## Objective

Understand how different prompting techniques affect LLM output quality and structure.

---

## 1. Zero-Shot Prompting

### Prompt

```
What is REST API?
```

### Output (Summary)

* Detailed explanation of REST architecture
* Includes principles like statelessness, client-server, caching
* Covers HTTP methods (GET, POST, PUT, DELETE)

### Observation

* Output is **correct but generic**
* Covers a lot, but not tailored

---

## 2. Few-Shot Prompting

### Prompt

```
Q: What is HTTP?
A: A protocol for communication

Q: What is REST API?
```

### Output (Summary)

* Model reused previous context
* Answer was shorter and more direct

### Observation

* Output becomes **guided by examples**
* Improves structure but depends on context clarity

---

## 3. Role Prompting

### Prompt

```
You are a senior backend engineer.
Explain REST API to a junior developer.
```

### Output (Summary)

* Uses analogy (restaurant example)
* Step-by-step explanation
* Covers API, REST, HTTP methods
* More conversational and practical

### Observation

* Output is **more practical and beginner-friendly**
* Role improves tone and clarity

---

## 4. Structured Output (JSON)

### Prompt

```
Explain REST API in JSON format:
{
  "definition": "",
  "advantages": [],
  "use_cases": []
}
```

### Output

```json
{
  "definition": "REST is an architectural style using HTTP for communication.",
  "advantages": [
    "Simple",
    "Scalable",
    "Flexible"
  ],
  "use_cases": [
    "Web applications",
    "Mobile apps",
    "APIs for services"
  ]
}
```

### Observation

* Output is **machine-readable and structured**
* Useful for backend systems and APIs

---

## Comparison Table

| Technique | Output Quality | Structure | Use Case                |
| --------- | -------------- | --------- | ----------------------- |
| Zero-shot | Generic        | Medium    | Basic queries           |
| Few-shot  | Guided         | Better    | Pattern-based tasks     |
| Role      | Practical      | High      | Teaching / explanations |
| JSON      | Structured     | Very High | Production systems      |

---

## Key Insights

* Prompt design significantly impacts output quality
* Few-shot improves consistency
* Role prompting improves clarity and usefulness
* Structured prompting enables system integration

---

## Conclusion

Prompt engineering is a critical skill when working with LLMs. By modifying prompts, we can control tone, structure, and accuracy of outputs, making them suitable for different use cases like education, development, and production systems.