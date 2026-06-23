"""Task manager for background processing."""
import threading
import queue
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import uuid


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None


class TaskManager:
    """Manages background tasks with progress reporting."""
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize TaskManager.
        
        Args:
            max_workers: Maximum number of concurrent workers
        """
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.result_queue = queue.Queue()
        self._lock = threading.Lock()
        self._shutdown = False
        
    def submit_task(
        self,
        func: Callable,
        *args,
        task_name: str = "Task",
        progress_callback: Optional[Callable[[float, str], None]] = None,
        **kwargs
    ) -> str:
        """
        Submit a task for background execution.
        
        Args:
            func: Function to execute
            *args: Function arguments
            task_name: Name of the task
            progress_callback: Callback for progress updates (progress, message)
            **kwargs: Function keyword arguments
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        task = Task(
            task_id=task_id,
            name=task_name,
            func=func,
            args=args,
            kwargs=kwargs,
            progress_callback=progress_callback
        )
        
        with self._lock:
            self.tasks[task_id] = task
            
        # Start worker thread
        thread = threading.Thread(
            target=self._run_task,
            args=(task,),
            daemon=True
        )
        task.thread = thread
        thread.start()
        
        return task_id
        
    def _run_task(self, task: 'Task'):
        """Run a task in background."""
        try:
            task.status = TaskStatus.RUNNING
            
            # Execute the function
            result = task.func(*task.args, **task.kwargs)
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            
            # Put result in queue
            self.result_queue.put(TaskResult(
                task_id=task.task_id,
                status=TaskStatus.COMPLETED,
                result=result
            ))
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            
            # Put error in queue
            self.result_queue.put(TaskResult(
                task_id=task.task_id,
                status=TaskStatus.FAILED,
                error=str(e)
            ))
            
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running task.
        
        Args:
            task_id: ID of the task to cancel
            
        Returns:
            True if task was cancelled, False otherwise
        """
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.CANCELLED
                    # Note: We can't actually kill a thread in Python,
                    # but we can mark it as cancelled
                    return True
        return False
        
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get task status."""
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id].status
        return None
        
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """Get task result."""
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id].result
        return None
        
    def get_task_error(self, task_id: str) -> Optional[str]:
        """Get task error message."""
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id].error
        return None
        
    def update_progress(self, task_id: str, progress: float, message: str = ""):
        """
        Update task progress.
        
        Args:
            task_id: Task ID
            progress: Progress value between 0 and 1
            message: Progress message
        """
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.progress = progress
                task.progress_message = message
                
                # Call progress callback if set
                if task.progress_callback:
                    task.progress_callback(progress, message)
                    
    def check_results(self) -> list:
        """
        Check for completed task results.
        
        Returns:
            List of TaskResult objects
        """
        results = []
        while not self.result_queue.empty():
            try:
                result = self.result_queue.get_nowait()
                results.append(result)
            except queue.Empty:
                break
        return results
        
    def get_all_tasks(self) -> list:
        """Get all tasks."""
        with self._lock:
            return list(self.tasks.values())
            
    def clear_completed(self):
        """Clear completed and failed tasks."""
        with self._lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    to_remove.append(task_id)
                    
            for task_id in to_remove:
                del self.tasks[task_id]
                
    def shutdown(self):
        """Shutdown the task manager."""
        self._shutdown = True
        # Cancel all running tasks
        with self._lock:
            for task in self.tasks.values():
                if task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.CANCELLED


class Task:
    """Represents a background task."""
    
    def __init__(
        self,
        task_id: str,
        name: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ):
        self.task_id = task_id
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.progress_callback = progress_callback
        
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.progress = 0.0
        self.progress_message = ""
        self.thread = None


# Global task manager instance
_task_manager = None


def get_task_manager() -> TaskManager:
    """Get the global task manager instance."""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager


def shutdown_task_manager():
    """Shutdown the global task manager."""
    global _task_manager
    if _task_manager:
        _task_manager.shutdown()
        _task_manager = None
