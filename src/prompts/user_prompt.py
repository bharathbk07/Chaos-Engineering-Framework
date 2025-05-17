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
            - Do not include any explanation or commentary — just return the final JSON array with 15 items (5 performance + 10 chaos).


            Return only a JSON array of 10 experiment objects without including ``` or ```json.
            """,
        "kubernetes_prompt": """
                I will provide you with the following:

                - **Experiment Details** including:
                - Title
                - Hypothesis
                - Failure type (e.g., pod delete, CPU hog, network latency, etc.)
                - Target component (e.g., namespace, pod label, deployment name)
                - Expected outcome
                - Rollback plan
                - Observability/metrics to validate
                - Priority level

                - **Kubernetes Environment Details** such as:
                - Namespace
                - Target resource type and name (pod, deployment, service, etc.)
                - Label selectors (if applicable)
                - Cluster config (if relevant or mocked)
                - Tooling available (e.g., `kubectl`, Prometheus, Loki, etc.)

                ---

                ### 🎯 Your task:

                Using **Chaos Toolkit**, create a **complete chaos experiment definition file** in **YAML format**, designed to run in the Kubernetes environment provided.

                ### 📋 The YAML file must include:

                - **Experiment Metadata**
                - Title, description, tags
                - **Configuration Section**
                - Kubernetes connection settings (`kubernetes` provider)
                - **Steady State Hypothesis**
                - Probes to validate system health before and after the chaos
                - Use `http-probe`, `kubernetes` probe, or `prometheus` probe based on inputs
                - **Method Section**
                - Inject the specified chaos using appropriate Chaos Toolkit action
                - Include pause before and after the action
                - Rollback or cleanup step (if rollback plan is provided)
                - **Rollbacks or Cleanup**
                - Defined action if the chaos causes instability

                ---

                ### 🔍 Additional Guidelines:

                - Use appropriate Chaos Toolkit plugins for Kubernetes (`chaostoolkit-kubernetes`, `chaostoolkit-prometheus`, etc.)
                - Ensure all `probes` and `actions` are syntactically valid and use recommended parameters
                - For failure modes like `pod delete`, `container kill`, or `CPU hog`, use Chaos Toolkit idiomatic actions
                - If metrics are provided, create Prometheus-based probes to validate them
                - If labels are provided, use them in the `selector` for targeting
                - Ensure the YAML is valid and can be executed directly with Chaos Toolkit
                - Use `kubectl` or `curl` commands to validate the state of the system before and after the chaos
                ---

                ### 📥 Example Input Format

                ```json
                {
                "experiment_title": "Delete API Pod",
                "hypothesis": "The API service should auto-recover without impacting users.",
                "failure_type": "pod delete",
                "target_component": {
                    "resource": "pod",
                    "label_selector": "app=api-service",
                    "namespace": "production"
                },
                "expected_outcome": "Pod is recreated and traffic continues as expected.",
                "rollback_plan": "Reapply deployment using kubectl or wait for HPA restart.",
                "observability_check": [
                    "Pod restart count",
                    "HTTP 5xx error rate",
                    "Response latency"
                ],
                "priority": "Medium"
                }
            """
        }
    return prompts.get(prompt, "Prompt not found.")
