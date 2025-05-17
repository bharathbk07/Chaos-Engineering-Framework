def userprompt(prompt):
    prompts ={
        "analyze_application":"""
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
            - Return only a JSON array of 15 experiment objects (5 performance + 10 chaos). Do not include any explanation, commentary, or code block formatting such as ``` or ```json.
            """,
        "kubernetes_prompt": """
            I will provide you with the following:

            - **Experiment Details**, including:
            - `experiment_title`: Name of the chaos experiment
            - `hypothesis`: A clear, testable statement about expected system behavior
            - `failure_type`: Type of chaos (e.g., pod delete, CPU hog, network delay)
            - `target_component`: Object containing:
                - `resource`: Kubernetes resource type (e.g., pod, deployment)
                - `label_selector`: Label to identify the resource
                - `namespace`: Namespace of the component
            - `expected_outcome`: What resilience or recovery should look like
            - `rollback_plan`: Steps to restore system health if chaos fails
            - `observability_check`: List of metrics or indicators to validate hypothesis
            - `priority`: Low, Medium, or High (used in tags)
            
            - **Kubernetes Environment Details**, such as:
            - `namespace`: Primary namespace where the chaos will be injected
            - `resource`: Type and name or label of the Kubernetes object to target
            - `label_selectors`: Optional label-based filtering
            - `kubeconfig_path`: Path to kubeconfig if different from default
            - `tooling`: Available observability tools (e.g., Prometheus, Loki, Datadog, etc.)

            - **Choas Toolkit discovery file**: A JSON file containing the experiment details and the Kubernetes environment details.

            ---

            ### 🎯 Your Task

            Using the **Chaos Toolkit**, generate a **complete chaos experiment file in valid JSON format**, ready to run in the Kubernetes cluster.  
            The structure **must conform to the [Chaos Toolkit experiment schema](https://chaostoolkit.org/reference/api/experiment/)**.

            ---

            ### 📋 The Output JSON Must Include:

            - `version`: Always set to `"1.0.0"`
            - `title`: Same as `experiment_title`
            - `description`: Human-readable summary of the goal
            - `tags`: Include failure type and priority
            - `configuration`: Use `"kubernetes"` key with config (like kubeconfig path if provided)
            - `steady-state-hypothesis`: 
            - `title`: A short summary of the expected behavior
            - `probes`: Use HTTP probe, Kubernetes pod status probe, or Prometheus probe (based on `observability_check`)
            - `method`: 
            - A list of actions including the main chaos action (e.g., delete pod)
            - Include `pauses` (before and/or after)
            - Include optional verification probes post-injection
            - `rollbacks`: (if `rollback_plan` is provided)
            - Add steps to revert or recover the system

            ---

            ### 🔍 Guidelines

            - Use Chaos Toolkit plugins appropriately:
            - For K8s actions: `chaostoolkit-kubernetes`
            - For metric probes: `chaostoolkit-prometheus`, `chaostoolkit-http`, etc.
            - Ensure all `probes`, `actions`, and `pauses` use correct parameter formats
            - Use values from `target_component` and `kubernetes` input fields
            - The final JSON must be valid, indented, and immediately executable via `chaos run`
            - Before returning the JSON, validate that it conforms to the Chaos Toolkit experiment schema.
            - To validate locally, first install the Chaos Toolkit CLI: `pip install chaos-toolkit`
            - Save the generated JSON to a file (e.g., `experiment.json`) and run: `chaos validate experiment.json`
            - Only return the JSON if it passes validation. If not, fix the structure and try again.
            

            Return only the JSON content of the experiment definition. Do not include any explanation, commentary, or code block formatting such as ``` or ```json.
            """
        }
    return prompts.get(prompt, "Prompt not found.")
