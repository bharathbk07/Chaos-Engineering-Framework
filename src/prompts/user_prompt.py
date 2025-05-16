def userprompt():
    prompt = """
    I have an application and I'm providing you with its `README.md` file and optionally some of the source code.

    Your task is to:

    1. Understand the architecture, functionality, and key components of the application.
    2. Identify possible weak points or assumptions in the system design.
    3. Create **10 chaos engineering experiments** in **JSON format** as described below.

    Each experiment should include the following fields:

    - "experiment_title": Short title of the experiment.
    - "hypothesis": A clear hypothesis about the system’s behavior under stress or failure.
    - "experiment_description": A short scenario describing what failure will be injected and where.
    - "expected_outcome": What the system should ideally do when this chaos is injected.
    - "component_to_be_tested": Service, container, pod, or system layer being targeted.
    - "failure_type": Type of failure (e.g., pod delete, network latency, CPU hog, DNS loss, etc.).
    - "blast_radius": Expected scope of the impact (e.g., frontend, backend, specific microservice).
    - "rollback_plan": What action to take if the system becomes unstable during the test.
    - "observability_check": What metrics/logs/traces to observe to validate the system behavior.
    - "priority": Low, Medium, or High – based on risk and impact.

    Use your reasoning on the architecture to create realistic and diverse experiments (infrastructure, network, process, disk, CPU, dependencies, etc.). If the README or code gives you access to environment info (like Kubernetes, Docker, AWS), take it into account.

    Return only a JSON array of 10 experiment objects without including ``` or ```json.
    """
    return prompt