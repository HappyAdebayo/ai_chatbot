
from task_manager import create_task, update_task, delete_task, complete_task, get_all_tasks, delete_all_tasks, complete_all_tasks



def execute_action(assistant_data):

    action_handlers = {
        "create_task": lambda: create_task(assistant_data.task),

        "list_tasks": lambda: (
            get_all_tasks(
                **assistant_data.filters.model_dump(exclude_none=True)
            )
            if assistant_data.filters
            else get_all_tasks()
        ),

        "update_task": lambda: update_task(assistant_data.task_update),

        "delete_task": lambda: delete_task(assistant_data.task.title),

        "complete_task": lambda: complete_task(assistant_data.task.title),

        "complete_all_tasks": lambda: complete_all_tasks(),

        "delete_all_tasks": lambda: (
            delete_all_tasks(confirmed=True)
            if assistant_data.confirmation == "confirmed"
            else assistant_data.message
        ),

        "chat": lambda: assistant_data.message,

        "clarify": lambda: assistant_data.message,
    }

    handler = action_handlers.get(assistant_data.action)

    if handler is None:
        return "Sorry, I don't recognize that action."

    return handler()
