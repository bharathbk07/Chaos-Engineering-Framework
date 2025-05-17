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
            - Return only a JSON array of 20 experiment objects (5 performance + 10 chaos). Do not include any explanation, commentary, or code block formatting such as ``` or ```json.
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
                "title": "Do we remain available in face of pod going down?",
                "description": "We expect Kubernetes to handle the situation gracefully when a pod goes down",
                "tags": ["kubernetes"],
                "steady-state-hypothesis": {
                    "title": "Verifying service remains healthy",
                    "probes": [
                        {
                            "name": "all-our-microservices-should-be-healthy",
                            "type": "probe",
                            "tolerance": true,
                            "provider": {
                                "type": "python",
                                "module": "chaosk8s.probes",
                                "func": "microservice_available_and_healthy",
                                "arguments": {
                                    "name": "myapp"
                                }
                            }
                        }
                    ]
                },
                "method": [
                    {
                        "type": "action",
                        "name": "terminate-db-pod",
                        "provider": {
                            "type": "python",
                            "module": "chaosk8s.pod.actions",
                            "func": "terminate_pods",
                            "arguments": {
                                "label_selector": "app=my-app",
                                "name_pattern": "my-app-[0-9]$",
                                "rand": true
                            }
                        },
                        "pauses": {
                            "after": 5
                        }
                    }
                ]
            }
            ```
            Hypothesis available  for Kubernetes:1)all_microservices_healthy2) deployment_is_fully_available
            3) deployment_is_not_fully_available4) microservice_available_and_healthy
            5) microservice_is_not_available6) read_microservices_logs
            7) secret_exists8) service_endpoint_is_initialized
            9) count_min_pods10) count_pods
            11) pod_is_not_available12) pods_in_conditions
            13) pods_in_phase14) pods_not_in_phase
            15) read_pod_logs16) should_be_found_in_logs
            17) statefulset_fully_available
            18) statefulset_not_fully_available19) get_cluster_custom_object
            20) get_custom_object21) list_cluster_custom_objects
            22) list_custom_objects23) get_network_fault
            24) get_network_faults25) get_stressor
            26) get_stressors27) get_events

            Experiment available for Kubernetes:1) kill_microservice
            2) remove_service_endpoint3) scale_microservice
            4) start_microservice5) all_microservices_healthy
            6) deployment_is_fully_available7) deployment_is_not_fully_available
            8) microservice_available_and_healthy 9) microservice_is_not_available
            10) read_microservices_logs 11) secret_exists
            12) service_endpoint_is_initialized 13) create_daemon_set
            14) delete_daemon_set15) update_daemon_set
            16) daemon_set_available_and_healthy17) daemon_set_fully_available
            18) daemon_set_not_fully_available19) daemon_set_partially_available
            20) create_deployment 21) delete_deployment
            22) rollout_deployment 23) scale_deployment
            24) deployment_available_and_healthy25) deployment_fully_available
            26) deployment_not_fully_available 27) deployment_partially_available
            28) create_namespace29) delete_namespace
            30) namespace_exists 31) allow_dns_access
            32) create_ingress 33) create_network_policy
            34) delete_ingress35) deny_all_egress
            36) deny_all_ingress37) remove_allow_dns_access
            38) remove_deny_all_egress 39) remove_deny_all_ingress
            40) remove_network_policy 41) update_ingress
            42) ingress_exists 43) cordon_node
            44) create_node45) delete_nodes
            46) drain_nodes47) uncordon_node
            48) all_nodes_must_be_ready_to_schedule 49) get_all_node_status_conditions
            50) get_nodes 51) nodes_must_be_healthy 52) verify_nodes_condition
            53) exec_in_pods54) terminate_pods
            55) count_min_pods 56) count_pods
            57) pod_is_not_available 58) pods_in_conditions
            59) pods_in_phase 60) pods_not_in_phase
            61) read_pod_logs 62) should_be_found_in_logs
            63) delete_replica_set 64) create_service_endpoint
            65) delete_service 66) service_is_initialized
            67) create_secret 68) delete_secret
            69) secret_exists 70) create_statefulset
            71) remove_statefulset 72) scale_statefulset
            73) statefulset_fully_available  74) statefulset_not_fully_available
            75) apply_from_json 76) apply_from_yaml
            77) create_cluster_custom_object 78) create_custom_object
            79) delete_cluster_custom_object  80) delete_custom_object
            81) patch_cluster_custom_object 82) patch_custom_object 83) replace_cluster_custom_object
            84) replace_custom_object 85) get_cluster_custom_object
            86) get_custom_object 87) list_cluster_custom_objects
            88) list_custom_objects 89) add_latency
            90) corrupt_packets 91) delete_network_fault
            92) duplicate_packets 93) reorder_packets
            94) set_bandwidth95) set_loss
            96) delete_stressor97) stress_cpu
            98) stress_memory 99) get_network_fault
            100) get_network_faults 101) get_stressor
            102) get_stressors 103) get_events

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
