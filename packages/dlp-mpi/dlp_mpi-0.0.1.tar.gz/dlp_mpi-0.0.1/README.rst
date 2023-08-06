




+-------------------------------------------+--------------------------------------------------+
| **Run an algorithm on multiple examples** | **Use dlp_mpi to run the loop body in parallel** |
+-------------------------------------------+--------------------------------------------------+
| .. code:: python                          | .. code:: python                                 |
|                                           |                                                  |
|  # python script.py                       |   # mpiexec -np 8 python script.py               |
|                                           |                                                  |
|  import time                              |   import time                                    |
|                                           |   import dlp_mpi                                 |
|                                           |                                                  |
|  examples = list(range(10))               |   examples = list(range(10))                     |
|                                           |                                                  |
|  for i in examples:                       |   for i in dlp_mpi.split_managed(examples):      |
|      # load, process and write data       |       # load, process and write data             |
|      # for index i                        |       # for index i                              |
|      time.sleep(0.2)                      |       time.sleep(0.2)                            |
|      data = {'a': i}                      |       data = {'a': i}                            |
|      data['a'] += 2                       |       data['a'] += 2                             |
|      print(data)                          |       print(data)                                |
|                                           |                                                  |
|      # Remember the results               |       # Remember the results                     |
|      results.append(data['a'])            |       results.append(data['a'])                  |
|                                           |                                                  |
|                                           |  results = dlp_mpi.gather(results)               |
|                                           |                                                  |
|                                           |  if dlp_mpi.IS_MASTER:                           |
|                                           |      results = [                                 |
|                                           |          result                                  |
|                                           |          for worker_results in results           |
|                                           |          for result in worker_results            |
|                                           |      ]                                           |
|                                           |                                                  |
|  # Summarize your experiment              |      # Summarize your experiment                 |
|  print(sum(results))                      |      print(sum(results))                         |
|                                           |                                                  |
|                                           |                                                  |
+-------------------------------------------+--------------------------------------------------+









