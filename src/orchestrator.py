# src/orchestrator.py
"""Manages the main workflow orchestration loop, fetching and dispatching tasks."""
import logging
from typing import List
from src.task_manager import task_queue
from src.agents.factory import AgentFactory
from src.workflow.state import workflow_state_machine, WorkflowState
from src.models import TaskSpec, AgentResponse
from src.session_manager import session_manager
from src.task_dependencies import topological_sort, detect_cycles # Import dependency management

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        
    def run_workflow(self, initial_tasks: List[TaskSpec]):
        """
        Executes the main workflow orchestration loop.
        Processes tasks based on dependencies.
        """
        session = session_manager.get_current_session()
        if not session:
            logger.error("No active session found. Cannot run workflow.")
            return

        workflow_state_machine.transition_to(WorkflowState.RUNNING)
        logger.info(f"Workflow orchestration started for session {session.id}.")

        try:
            # 1. Validate and sort tasks based on dependencies
            if detect_cycles(initial_tasks):
                raise ValueError("Circular dependency detected in the initial task list.")
            sorted_tasks = topological_sort(initial_tasks)

            # 2. Populate task queue with sorted tasks
            for task in sorted_tasks:
                task_queue.add_task(task)

            # 3. Main orchestration loop
            while True:
                task = task_queue.get_next_task()
                if not task:
                    logger.info("No more tasks in queue. Workflow complete.")
                    break

                logger.info(f"Dispatching task: {task.name} (ID: {task.id}) to agent: {task.agent_name}")
                session_manager.add_log_entry(f"Dispatching task: {task.name} to agent: {task.agent_name}")

                try:
                    agent = self.agent_factory.create_agent(task.agent_name)
                    response: AgentResponse = agent.run(task)
                    
                    task_queue.update_task_status(task.id, response.status)
                    session_manager.add_log_entry(f"Task {task.name} (ID: {task.id}) completed with status: {response.status}")
                    
                    # Process agent response (artifacts, output etc.)
                    if response.artifacts:
                        for artifact in response.artifacts:
                            session_manager.add_artifact(artifact)
                            logger.info(f"Agent {task.agent_name} produced artifact: {artifact.name}")

                    if response.status == "failed":
                        logger.error(f"Task {task.name} reported failure: {response.output.get('error_message', 'No error message provided')}")
                        workflow_state_machine.transition_to(WorkflowState.FAILED)
                        break # Stop workflow on agent-reported failure

                except Exception as e:
                    task_queue.update_task_status(task.id, "failed")
                    session_manager.add_log_entry(f"Task {task.name} (ID: {task.id}) failed due to exception: {e}")
                    logger.error(f"Task {task.name} (ID: {task.id}) failed unexpectedly: {e}", exc_info=True)
                    workflow_state_machine.transition_to(WorkflowState.FAILED)
                    break
        except ValueError as ve: # Catch dependency errors
            logger.error(f"Workflow failed due to dependency issue: {ve}")
            workflow_state_machine.transition_to(WorkflowState.FAILED)
        except Exception as e: # Catch any other unexpected errors during setup
            logger.error(f"An unexpected error occurred during workflow setup: {e}", exc_info=True)
            workflow_state_machine.transition_to(WorkflowState.FAILED)
        finally:
            # Final state transition if loop completed without breaking
            if workflow_state_machine.get_state() == WorkflowState.RUNNING:
                workflow_state_machine.transition_to(WorkflowState.COMPLETED)
                session_manager.end_session(status=WorkflowState.COMPLETED)
            else:
                session_manager.end_session(status=workflow_state_machine.get_state())
                
            logger.info(f"Workflow orchestration finished for session {session.id} with final status: {workflow_state_machine.get_state().value}.")
