from collections import deque
import heapq

def generate_project_plan(project, mode="fastest"):
    """
    Generates a project plan based on tasks, dependencies, and optimization mode.
    """

    tasks = project.tasks
    task_map = {t.id: t for t in tasks}                     # O(n)

    # Build dependency graph
    graph = {t.id: [] for t in tasks}                       # O(n)
    indegree = {t.id: 0 for t in tasks}                     # O(n)

    for task in tasks:                                      # O(n + edges)
        for dep in task.dependencies:
            graph[dep.id].append(task.id)
            indegree[task.id] += 1

    # Linear ordering
    queue = deque([task_id for task_id, degree in indegree.items() if degree == 0])  # O(n)
    topo_order = []

    while queue:                                            # O(n)
        current = queue.popleft()
        topo_order.append(current)

        for next_task in graph[current]:                    # O(edges)
            indegree[next_task] -= 1
            if indegree[next_task] == 0:
                queue.append(next_task)

    # Priority‑based scheduling
    heap = []

    def push(task):
        if mode == "fastest":
            key = (task.deadline, task.hours, -task.priority)
        else:
            key = (-task.hours, -task.priority, task.deadline)
        heapq.heappush(heap, (key, task.id))                # O(log n)

    for task_id in topo_order:                              # O(n log n)
        push(task_map[task_id])

    # Build plan
    current_time = 0
    plan = []

    while heap:                                             # O(n log n)
        _, task_id = heapq.heappop(heap)
        task = task_map[task_id]

        start = current_time
        end = current_time + task.hours
        current_time = end

        plan.append({
            "task_id": task.id,
            "task_name": task.name,
            "start": start,
            "end": end,
            "assigned_member": None,
            "dependencies": [d.id for d in task.dependencies]
        })

    return plan
