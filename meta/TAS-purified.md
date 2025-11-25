01. Load application configuration files (YAML/JSON) into a Pydantic Settings model. ⟹ Configuration files (YAML/JSON) exist ⇢ Pydantic Settings model populated with configuration
02. Validate configuration schema using Pydantic validators. ⟹ Pydantic Settings model exists and is populated ⇢ Validated configuration schema
03. Create Path Management utilities (get_root(), ensure_dir()). ⟹ None ⇢ Path management utilities (get_root(), ensure_dir()) available
04. Implement Logging Setup (basic config, handlers, formatters). ⟹ Path management utilities (get_root()) available ⇢ Basic logging setup configured
05. Add Logging Formatter Customization (colors, JSON). ⟹ Basic logging setup configured ⇢ Custom logging formatters (colors, JSON) integrated
06. Develop File I/O Utilities (read/write text & binary, safe mode). ⟹ Path management utilities available ⇢ File I/O utilities (read/write, safe mode) implemented
07. Define Data Structure Definitions (Pydantic models & dataclasses) for: AgentSpec, TaskSpec, Artifact, Session, ExecutionContext. ⟹ None ⇢ Pydantic models/dataclasses for AgentSpec, TaskSpec, Artifact, Session, ExecutionContext defined
08. Build Prompt Management module: load prompt templates from prompts/ directory, expose get_prompt(name). ⟹ Configuration loaded, File I/O utilities available ⇢ Prompt Management module with get_prompt(name) function
09. Create Agent Specification Loading (parse YAML/JSON spec files into AgentSpec models). ⟹ AgentSpec Pydantic model defined, Prompt Management module available ⇢ Agent specifications loaded as AgentSpec models
10. Design Agent Base class (abstract run(task: TaskSpec) -> AgentResponse). ⟹ TaskSpec and AgentResponse models defined ⇢ Abstract Agent Base class with run method defined
11. Implement Agent Discovery/Lookup (search registry by role, name). ⟹ Agent specifications loaded, Agent Base class defined ⇢ Agent Discovery/Lookup mechanism implemented
12. Write Agent Instantiation Factory (creates concrete Agent objects from AgentSpec). ⟹ Agent Base class defined, Agent Discovery/Lookup mechanism available ⇢ Agent Instantiation Factory implemented
13. Develop LLM Provider Abstraction (interface LLMProvider with generate(prompt)). ⟹ Prompt Management module available ⇢ LLMProvider interface defined
14. Build Model‑Specific LLM Wrappers (Gemini, Ollama, Kimi, Mistral) implementing LLMProvider. ⟹ LLMProvider interface defined ⇢ Model-specific LLM wrappers (Gemini, Ollama, Kimi, Mistral) implemented
15. Create LLM Client Initialization (load API keys, endpoints, instantiate wrappers). ⟹ Model-specific LLM wrappers available ⇢ LLM client initialized with API keys and endpoints
16. Implement Prompt Template Loading (read raw prompt files, support Jinja2 rendering). ⟹ Prompt Management module available, File I/O utilities available ⇢ Prompt template loading with Jinja2 rendering implemented
17. Build Dynamic Prompt Updates (agents can modify own prompt via update_prompt). ⟹ Prompt template loading implemented ⇢ Dynamic prompt update mechanism for agents available
18. Develop Task Management core (TaskSpec, TaskQueue, status tracking). ⟹ TaskSpec Pydantic model defined ⇢ Task Management core with TaskSpec, TaskQueue, and status tracking implemented
19. Implement Task Dependency Management (topological sort, detect cycles). ⟹ Task Management core available ⇢ Task Dependency Management (topological sort, cycle detection) implemented
20. Create Artifact Handling module (store, retrieve, version artifacts). ⟹ File I/O utilities available ⇢ Artifact Handling module for storage, retrieval, and versioning
21. Add Artifact Contextualization (provide prior artifacts to agents on demand). ⟹ Artifact Handling module available ⇢ Artifact contextualization mechanism implemented
22. Design Execution Context (environment vars, runtime flags, current session). ⟹ ExecutionContext Pydantic model defined, Path Management utilities available ⇢ Execution Context designed and accessible
23. Construct Workflow State Management (state machine: INIT → RUNNING → COMPLETED / FAILED). ⟹ Execution Context available ⇢ Workflow State Management (state machine) implemented
24. Write Session Management (track a single run, persist logs, artifacts). ⟹ Workflow State Management, Logging Setup, Artifact Handling available ⇢ Session Management implemented
25. Develop Bootstrap Process (sequence: Config → Logging → Path → DB → LLM → Agents → Workflow). ⟹ Config, Logging, Path, LLM, Agent, Workflow components available ⇢ Bootstrap process implemented
26. Implement Workflow Orchestration Loop (iteration over rounds, fetch next tasks, dispatch agents). ⟹ Bootstrap process complete, Task Dependency Management, Workflow State Management available ⇢ Workflow Orchestration Loop implemented
27. Create Task Dependency Management (prereq handling inside orchestration). ⟹ Workflow Orchestration Loop, Task Dependency Management (topological sort) available ⇢ Task Dependency Management integrated into orchestration
28. Add Agent Output Structuring (standard JSON schema: status, output, artifacts). ⟹ Agent Base class defined ⇢ Standard JSON schema for Agent output (status, output, artifacts) defined
29. Build System Runtime Class (holds global state, registry, config, logger). ⟹ Session Management, Bootstrap Process complete ⇢ System Runtime Class implemented
30. Design CLI Parsing (argparse/typer: subcommands run, init, status). ⟹ Path Management, Logging Setup, Custom Logging available ⇢ CLI Parsing for subcommands (run, init, status) designed
31. Write System Entry Point (main.py: parse CLI, instantiate SystemRuntime, start bootstrap). ⟹ CLI Parsing, System Runtime Class available ⇢ System Entry Point (main.py) implemented
32. Define Database Schema for Persistent Artifacts, Sessions, and Agent Metadata. ⟹ Artifact, Session, AgentSpec Pydantic models defined ⇢ Database schema for artifacts, sessions, and agent metadata defined
33. Generate SQL DDL for the schema (PostgreSQL dialect). ⟹ Database schema defined ⇢ SQL DDL generated for PostgreSQL
34. Create migration script (CREATE TABLE …) and apply via psql or SQLAlchemy engine. ⟹ SQL DDL generated, LLM Client Initialization complete ⇢ Database migration script created and applied
35. Add Schema Validation for LLM Output (Pydantic models matching AgentResponse). ⟹ AgentResponse Pydantic model defined ⇢ Schema validation for LLM output implemented
36. Implement Error Handling & Logging (exception wrappers, retry policies). ⟹ Logging Setup, Custom Logging available ⇢ Error Handling and Logging (exception wrappers, retry policies) implemented
37. Add Response Format Handling (detect JSON vs plain text, deserialize accordingly). ⟹ Schema Validation for LLM Output available ⇢ Response format handling (JSON/plain text detection, deserialization) implemented
38. Write Plan Generation & Validation (orchestrator builds execution plan, validates DAG). ⟹ Task Dependency Management, Schema Validation for LLM Output available ⇢ Plan Generation and Validation for orchestrator implemented
39. Develop Documentation (README, Architecture Overview, API Reference, Deployment Guide). ⟹ System Entry Point, Database migration, Plan Generation and Validation complete ⇢ Comprehensive documentation generated
40. Finalize Artifact Packaging (zip source, generate checksum, publish to GitHub release). ⟹ System Entry Point, Documentation complete ⇢ Final artifact packaging and publishing implemented