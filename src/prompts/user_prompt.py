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
            # Improved GenAI Prompt for Generating a Chaos Toolkit Experiment JSON

            ---

            I will provide you with the following input data:

            - **Experiment Details**:
            - `experiment_title`: Name of the chaos experiment (string)
            - `hypothesis`: A clear, testable statement describing the expected system behavior (string)
            - `failure_type`: Type of chaos to inject (e.g., `"pod-delete"`, `"cpu-hog"`, `"network-delay"`) (string)
            - `target_component`: Object describing the Kubernetes target:
                - `resource`: Kubernetes resource type, e.g., `"pod"`, `"deployment"` (string)
                - `label_selector`: Label selector string to identify target resource(s) (string)
                - `namespace`: Kubernetes namespace where the target lives (string)
            - `expected_outcome`: Description of what resilience or recovery looks like (string)
            - `rollback_plan`: Optional steps to restore system health if chaos injection fails (string or structured list)
            - `observability_check`: List of observability probes or metrics to verify the hypothesis (array of strings)
            - `priority`: `"Low"`, `"Medium"`, or `"High"` — to be used as experiment tags (string)

            - **Kubernetes Environment Details**:
            - `namespace`: Primary namespace for chaos injection (string)
            - `resource`: Target Kubernetes resource type and either name or label (string/object)
            - `label_selectors`: Optional labels for filtering targets (string or array)
            - `kubeconfig_path`: Optional path to kubeconfig file if not default (string)
            - `tooling`: List of observability tools available, e.g., `["prometheus", "loki", "datadog"]` (array of strings)

            - **Chaos Toolkit discovery file**:
            - A JSON file that encapsulates the above experiment and Kubernetes environment details.

            ---

            ### 🎯 Your Task

            Using the **Chaos Toolkit** specifications, **generate a fully valid chaos experiment JSON file** ready to be executed with the `chaos run` CLI command in a Kubernetes environment.

            - The JSON must **strictly conform to the [Chaos Toolkit experiment schema](https://chaostoolkit.org/reference/api/experiment/)**.
            - Use appropriate Chaos Toolkit plugins:
            - Kubernetes actions and probes: `"chaostoolkit-kubernetes"`
            - Metric or HTTP probes (if applicable): `"chaostoolkit-prometheus"`, `"chaostoolkit-http"`, etc.

            ---

            ### 📋 Output Requirements

            Your output JSON must contain:

            - `"version"`: Always `"1.0.0"`
            - `"title"`: Use the `experiment_title`
            - `"description"`: Human-readable summary including the hypothesis and expected outcome
            - `"tags"`: Include the `failure_type` and `priority` values as lowercase strings
            - `"configuration"`:
            - Include `"kubernetes"` key with relevant config (e.g., `kubeconfig_path` if provided)
            - `"steady-state-hypothesis"`:
            - `"title"`: Short description summarizing the expected normal system behavior (e.g., from `hypothesis`)
            - `"probes"`: List of probes matching `observability_check` (HTTP, Kubernetes status, Prometheus, etc.)
            - `"method"`: Ordered list of activities including:
            - Pre-chaos probes (optional)
            - Main chaos action (e.g., delete pod, create CPU hog)
            - Pauses before/after chaos injection where relevant
            - Post-chaos verification probes (optional)
            - `"rollbacks"` (optional): Steps from `rollback_plan` to restore system state if chaos fails

            ---

            ### 🔍 Guidelines & Best Practices

            - Dynamically build Kubernetes actions using `target_component` info (resource, label_selector, namespace).
            - Select appropriate probe types based on `observability_check` and `tooling`. For example:
            - Use Kubernetes pod status probes if checking pod readiness.
            - Use Prometheus queries if metric-based validation is requested.
            - Use HTTP probes if endpoint health checks are needed.
            - Tags should be lowercase and reflect failure type and priority, e.g., `["pod-delete", "high"]`.
            - Ensure all actions and probes have unique names.
            - Include pauses (`"pause"` action) before and/or after chaos injection to allow observation.
            - If `rollback_plan` is provided, translate it into actionable rollback steps in the `"rollbacks"` section.
            - Validate the final JSON using `chaos validate` before returning it.
            - The returned JSON must be pretty-printed, syntactically valid, and immediately executable by Chaos Toolkit.

            ---

            ### Example Skeleton of the Resulting JSON (abbreviated)

            ```json
            {
            "version": "1.0.0",
            "title": "<experiment_title>",
            "description": "<human-readable summary including hypothesis and expected_outcome>",
            "tags": ["<failure_type>", "<priority>"],
            "configuration": {
                "kubernetes": {
                "kubeconfig_path": "<kubeconfig_path>"
                }
            },
            "steady-state-hypothesis": {
                "title": "<hypothesis summary>",
                "probes": [
                {
                    "type": "probe",
                    "name": "check-pod-status",
                    "provider": {
                    "type": "python",
                    "module": "chaosk8s.probes",
                    "func": "pod_status",
                    "arguments": {
                        "label_selector": "<label_selector>",
                        "namespace": "<namespace>"
                    }
                    }
                }
                // Additional probes as per observability_check
                ]
            },
            "method": [
                {
                "type": "action",
                "name": "pre-chaos-check",
                "provider": {
                    // ...
                }
                },
                {
                "type": "action",
                "name": "inject-chaos",
                "provider": {
                    "type": "python",
                    "module": "chaosk8s.actions",
                    "func": "<action-function-based-on-failure_type>",
                    "arguments": {
                    "resource": "<resource>",
                    "label_selector": "<label_selector>",
                    "namespace": "<namespace>"
                    }
                }
                },
                {
                "type": "pause",
                "duration": 30
                },
                {
                "type": "probe",
                "name": "post-chaos-check",
                "provider": {
                    // ...
                }
                }
            ],
            "rollbacks": [
                {
                "type": "action",
                "name": "rollback-action",
                "provider": {
                    // Steps from rollback_plan if any
                }
                }
            ]
            }

            Return only the JSON content of the experiment definition. Do not include any explanation, commentary, or code block formatting such as ``` or ```json.
            """,
        "python_chaos_code": """
                # GenAI Prompt for Generating Chaos Toolkit Experiment in Python

                ---

                I will provide you with the following input data:

                - 🎯 Experiment Details:
                - experiment_title: Name of the chaos experiment (string)
                - hypothesis: A clear, testable statement describing the expected system behavior (string)
                - failure_type: Type of chaos to inject (e.g., "pod-delete", "cpu-hog", "network-delay") (string)
                - target_component: Object describing the Kubernetes target:
                    - resource: Kubernetes resource type, e.g., "pod", "deployment" (string)
                    - label_selector: Label selector string to identify target resource(s) (string)
                    - namespace: Kubernetes namespace where the target lives (string)
                - expected_outcome: Description of what resilience or recovery looks like (string)
                - rollback_plan: Optional steps to restore system health if chaos injection fails (string or structured list)
                - observability_check: List of observability probes or metrics to verify the hypothesis (array of strings)
                - priority: "Low", "Medium", or "High" — to be used as experiment tags (string)

                - 🧠 Kubernetes Environment Details:
                - namespace: Primary namespace for chaos injection (string)
                - label_selectors: Optional labels for filtering targets (string or array)
                - kubeconfig_path: Optional path to kubeconfig file if not default (string)
                - tooling: List of observability tools available, e.g., ["prometheus", "loki", "datadog"] (array of strings)

                ---

                ## Your Task

                Generate a Python script (not JSON) using the Chaos Toolkit's chaoslib modules that:

                - Builds the chaos experiment using procedural Python
                - Defines:
                - A steady-state hypothesis function
                - The main chaos method function
                - Optional rollback function
                - Uses appropriate chaoslib modules and providers such as:
                - chaosk8s.probes, chaosk8s.actions
                - chaosprometheus.probes (if Prometheus-based)
                - chaoslib.pause for pause activities

                ---

                ## Output Requirements

                Return a Python file (.py) that includes:

                - Imports of relevant chaoslib modules
                - A main() method to invoke the experiment
                - A structured function for:
                - Defining steady-state hypothesis with probes (based on observability_check)
                - Injecting chaos using the specified failure_type
                - Optional rollback step using rollback_plan
                - Execution of the experiment via chaoslib run()

                The code must:

                - Be Pythonic and well-commented
                - Support CLI execution (include if __name__ == "__main__")
                - Use kubeconfig_path if provided in configuration
                - Validate probe success/failure and log outcomes
                - Include helpful logging for tracing progress

                ---

                ## Example Skeleton (Python)

                ```python
                from chaoslib.types import Configuration, Secrets
                from chaosk8s.probes import pod_status
                from chaosk8s.actions import delete_pods, kill_pods
                from chaoslib import run_experiment
                from chaoslib.pause import pause
                import logging

                logging.basicConfig(level=logging.INFO)

                def steady_state(config: Configuration):
                    logging.info("Checking steady-state hypothesis...")
                    return pod_status(
                        name=None,
                        label_selector="app=example",
                        ns="default",
                        secrets=None,
                        configuration=config
                    )

                def inject_chaos(config: Configuration):
                    logging.info("Injecting chaos...")
                    delete_pods(
                        label_selector="app=example",
                        ns="default",
                        secrets=None,
                        configuration=config
                    )
                    pause(30)

                def rollback(config: Configuration):
                    logging.info("Rollback step: redeploying pod or restarting service (if needed)...")
                    # implement rollback logic if provided

                def main():
                    config = {
                        "kubeconfig_path": "~/.kube/config"
                    }

                    if not steady_state(config):
                        logging.error("Initial steady-state check failed. Aborting experiment.")
                        return

                    inject_chaos(config)

                    if not steady_state(config):
                        logging.error("Post-chaos steady-state check failed.")
                        rollback(config)
                    else:
                        logging.info("System recovered as expected.")

                if __name__ == "__main__":
                    main()

                ```
                Return only the Python code. Do not include any explanation, commentary, or code block formatting such as ``` or ```python.
        """,
        "chaos_experiment_file_validation": """
                I will provide the following input:

                1. 🧪 A Chaos Toolkit experiment JSON file (may contain schema issues or structural mistakes)
                2. 🧾 One or more error messages generated from:
                - chaos validate <filename>.json
                - chaos run <filename>.json

                ---

                ## 🎯 Your Task

                Analyze the provided experiment JSON and error message(s) to:

                - Identify the root cause(s) of validation or runtime errors
                - Fix the experiment JSON so that it:
                - Passes chaos validate without errors
                - Adheres to the official Chaos Toolkit experiment schema: https://chaostoolkit.org/reference/api/experiment/
                - Is immediately runnable via chaos run <filename>.json
                - Retains the original intent and purpose of the experiment

                ---

                ## 📋 Output Requirements

                You must return:

                - ✅ A fixed, valid Chaos Toolkit experiment in JSON format
                - Include: version, title, description, tags, configuration, steady-state-hypothesis, method, and optional rollbacks
                - All probes and actions must conform to the correct structure
                - Only include secrets/config if they were in the original
                - 🧾 A short explanation of what was fixed and why (commented if needed)
                - ✅ Ensure the final JSON conforms to the Chaos Toolkit schema and passes validation

                ---

                ## 🧠 Example Use Cases

                - If a probe is missing required fields like type or provider → add them correctly
                - If label_selector is not provided for a Kubernetes probe or action → insert with a valid string
                - If configuration is malformed → correct the dictionary and keys
                - If there are syntax or indentation issues → fix JSON structure

                ---

                ## 💡 Guidelines

                - Validate JSON using: chaos validate <experiment_file>.json
                - Refer to: https://chaostoolkit.org/reference/api/experiment/
                - Use plugins as required: e.g., chaosk8s, chaosprometheus, chaoslib.pause
                - Maintain original semantics (title, failure type, resource target, etc.)
                - Fix gracefully — don’t strip useful intent or metadata

                ---

        """
        }
    return prompts.get(prompt, "Prompt not found.")
