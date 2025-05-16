def userprompt():
    prompt = """
    I have an application and I'm providing you with its `README.md` file and optionally some of the source code.

    Your task is to:

    1. Understand the architecture, functionality, and key components of the application.
    2. Identify possible weak points or assumptions in the system design.
    3. Based on this understanding, generate a JSON array that includes:
    - **5 Performance Test Scenarios**
    - **10 Chaos Engineering Experiments**
    ### Format:

    Return the output as a JSON array. Each entry in the array must be a JSON object with the following keys:
    - `"performance"`: (only for performance test scenarios)
    - `"scenario_title"`: Brief title of the test.
    - `"scenario_description"`: Purpose and type of performance test (load, stress, endurance, etc.).
    - `"user_flow"`: Description of user behavior simulated in this test.
    - `"expected_outcome"`: What metrics indicate success (e.g., response time, throughput, error rate).
    - `"priority"`: Low, Medium, or High — based on risk and impact.
    - `"observability_check"`: Metrics, logs, or traces to watch to validate the scenario.
    - '"test_type"': Type of test (e.g., load, stress, endurance, spike, etc.).
    - `"test_tool"`: Tool to be used for the test (e.g., JMeter, Locust, etc.).

    - `"chaos"`: (only for chaos engineering experiments)
    - `"experiment_title"`: Short title of the experiment.
    - `"hypothesis"`: A clear hypothesis about the system’s behavior under stress or failure.
    - `"experiment_description"`: What failure will be injected and where.
    - `"expected_outcome"`: What the system should ideally do when this chaos is injected.
    - `"component_to_be_tested"`: Service, container, pod, or system layer being targeted.
    - `"failure_type"`: Type of failure (e.g., pod delete, network latency, CPU hog, etc.).
    - `"blast_radius"`: Expected scope of the impact (e.g., frontend, backend, DB).
    - `"rollback_plan"`: Action to take if the system becomes unstable during the test.
    - `"observability_check"`: Metrics, logs, or traces to watch to validate the hypothesis.
    - `"priority"`: Low, Medium, or High — based on risk and impact.
    - '"test_tool"`: Tool to be used for the test (e.g., Litmus, ChaosMesh, Gremlin, etc.).
    - '""metrics_to_monitor"': Metrics to monitor during the chaos experiment (e.g., CPU, memory, latency, etc.).

    ### Instructions:

    - Use your reasoning to infer architectural patterns, backend APIs, frontend routes, or third-party services from the `README.md` and source files.
    - Make the experiments and scenarios **diverse** across infrastructure, network, app logic, and database layers.
    - Ensure **realistic and actionable suggestions** that could be executed with tools like JMeter, Locust, Litmus, ChaosMesh, or Gremlin.
    - Do not include any explanation or commentary — just return the final JSON array with 15 items (5 performance + 10 chaos).


    Return only a JSON array of 10 experiment objects without including ``` or ```json.
    """
    return prompt