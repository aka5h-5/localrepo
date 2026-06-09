tests/components/Runs/MetricCard.test.tsx
tests/components/Runs/MetricsSection.test.tsx
tests/components/Runs/RunsToolbar.test.tsx
tests/components/Runs/TestCaseCard.test.tsx
tests/components/Runs/TestCaseGrid.test.tsx
tests/components/Runs/TestCaseTable.test.tsx
tests/components/Sidebar.test.tsx
tests/components/TestCaseModal.test.tsx
tests/constants/routes.test.ts
tests/context/RunsFiltersContext.test.tsx
tests/index.test.tsx
tests/pages/Analytics.test.tsx
tests/pages/Dashboard.test.tsx
tests/pages/NotFound.test.tsx
tests/pages/Runs.test.tsx
tests/theme.test.ts
tests/types/run.test.ts
tests/utils/runUtils.test.ts
tsconfig.json
Traceback (most recent call last):
  File "c:\Users\akashs1\AI_testcase\tree.py", line 30, in <module>
    result = graph.invoke(state)
             ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\pregel\main.py", line 3884, in invoke
    for chunk in self.stream(
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\pregel\main.py", line 2938, in stream
    for _ in runner.tick(
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\pregel\_runner.py", line 207, in tick
    run_with_retry(
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\pregel\_retry.py", line 617, in run_with_retry
    return task.proc.invoke(task.input, config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\_internal\_runnable.py", line 684, in invoke
    input = context.run(step.invoke, input, config, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\langgraph\_internal\_runnable.py", line 426, in invoke
    ret = self.func(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\akashs1\AI_testcase\node3.py", line 9, in getDiff
    URL = f"{state.owner}/{state.repository}"
             ^^^^^^^^^^^
  File "C:\Users\akashs1\AI_testcase\.venv\Lib\site-packages\pydantic\main.py", line 1042, in __getattr__
    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
AttributeError: 'AgentState' object has no attribute 'owner'
During task with name 'get_diff' and id '4f350775-e4cf-2602-766e-7c161d087c53'
PS C:\Users\akashs1\AI_testcase> 
