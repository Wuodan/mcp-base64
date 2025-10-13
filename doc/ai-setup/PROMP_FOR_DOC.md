Create high-quality code documentation directly inside the given file. Use **Markdown syntax**.  

General rules:  
- Include only sections with actual content. Never output empty headers.  
- Documentation must be clear, concise, and complete. No filler.  
- Always prefer practical detail (types, edge cases, usage) over vague description.  

Documentation requirements:  

**1. File-Level Header (when info exists)**  
- Short overview of the file’s purpose.  
- Dependencies and external libraries.  

**2. Class / Module Docs (if present)**  
- Purpose and role in the system.  
- Key methods, attributes, and behaviors.  

**3. Function / Method Docs (if present)**  
- Summary of what it does.  
- Parameters: type, purpose, defaults.  
- Return values: type and meaning.  
- Possible exceptions and conditions.  

**4. Code Block Comments**  
- Explain complex or non-obvious logic.  
- Reference or briefly explain algorithms, formulas, or unusual techniques.  

**5. Usage Examples**  
- Add minimal, working code snippets that show how to call functions or instantiate classes.  

**6. Edge Cases and Assumptions**  
- Input assumptions, expected formats.  
- How code behaves under unexpected or boundary conditions.  
- If derived from research papers, libraries, or external resources, add references.  

**7. End-User Notes (if relevant)**  
- Practical notes for developers who will use this code as a tool, API, or library.  

**Important constraints:**  
- Do not mention these guidelines in the output.  
- Always update all necessary sections of the file.  