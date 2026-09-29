import streamlit as st
import time

from tools import list_pods, describe_pod, get_events, get_logs
from remediation import get_proposed_fix, execute_fix


st.set_page_config(
    page_title="BigBlueOnCall",
    page_icon="🚨",
    layout="wide",
)


# ============================================================
# Styling
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-size: 42px;
    font-weight: 750;
    margin-bottom: 0;
}

.subtitle {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.incident-card {
    padding: 20px;
    border-radius: 14px;
    border-left: 6px solid #ef4444;
    background: #fff5f5;
    margin-bottom: 15px;
}

.success-card {
    padding: 20px;
    border-radius: 14px;
    border-left: 6px solid #22c55e;
    background: #f0fdf4;
    margin-bottom: 15px;
}

.info-card {
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
    background: #eff6ff;
    margin-bottom: 10px;
}

.approval-card {
    padding: 18px;
    border-radius: 12px;
    border: 2px solid #f59e0b;
    background: #fffbeb;
    margin-top: 15px;
    margin-bottom: 15px;
}

.resolved-card {
    padding: 18px;
    border-radius: 14px;
    border-left: 6px solid #16a34a;
    background: #f0fdf4;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# Session state
# ============================================================

if "pods" not in st.session_state:
    st.session_state["pods"] = []

if "healthy" not in st.session_state:
    st.session_state["healthy"] = 0

if "unhealthy" not in st.session_state:
    st.session_state["unhealthy"] = 0

if "resolved_incidents" not in st.session_state:
    st.session_state["resolved_incidents"] = []


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">🚨 BigBlueOnCall</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Kubernetes Incident Investigation & SRE Assistant'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    namespace = st.text_input(
        "Kubernetes Namespace",
        value="default",
    )

    st.divider()

    st.markdown("### 🛡️ Safety")

    st.info(
        "BigBlueOnCall never automatically executes remediation. "
        "An operator must review and approve the proposed commands."
    )

    st.divider()

    st.markdown("### 🔄 Incident Workflow")

    st.markdown("""
    **1.** 🔎 Detect  
    **2.** 🔍 Investigate  
    **3.** 📋 Collect evidence  
    **4.** 🧠 Diagnose  
    **5.** 🛠 Propose fix  
    **6.** 👤 Human approval  
    **7.** 🚀 Execute  
    **8.** ✅ Verify
    """)


# ============================================================
# Scan Cluster
# ============================================================

if st.button(
    "🔍 Scan Cluster",
    type="primary",
):

    pods = list_pods(namespace)

    pod_lines = pods.splitlines()

    healthy = 0
    unhealthy = 0

    for line in pod_lines:

        parts = line.split(" | ")

        if len(parts) < 2:
            continue

        status = parts[1]

        if status == "Running":
            healthy += 1
        else:
            unhealthy += 1

    st.session_state["pods"] = pod_lines
    st.session_state["healthy"] = healthy
    st.session_state["unhealthy"] = unhealthy

    st.success(
        f"Cluster scan completed. Found {len(pod_lines)} workload(s)."
    )


# ============================================================
# Dashboard
# ============================================================

if st.session_state["pods"]:

    healthy = st.session_state["healthy"]
    unhealthy = st.session_state["unhealthy"]
    resolved = len(st.session_state["resolved_incidents"])

    st.markdown(
        '<div class="section-title">📊 Cluster Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Workloads",
            len(st.session_state["pods"]),
        )

    with col2:
        st.metric(
            "Healthy",
            healthy,
        )

    with col3:
        st.metric(
            "Active Incidents",
            unhealthy,
        )

    with col4:
        st.metric(
            "Resolved",
            resolved,
        )


    # ========================================================
    # Active Incidents
    # ========================================================

    active_incidents = []

    for line in st.session_state["pods"]:

        parts = line.split(" | ")

        if len(parts) >= 2 and parts[1] != "Running":
            active_incidents.append(
                (parts[0], parts[1])
            )


    if active_incidents:

        st.markdown(
            '<div class="section-title">🚨 Active Incidents</div>',
            unsafe_allow_html=True,
        )


    # ========================================================
    # Workloads
    # ========================================================

    st.markdown(
        '<div class="section-title">🖥️ Cluster Workloads</div>',
        unsafe_allow_html=True,
    )


    for line in st.session_state["pods"]:

        parts = line.split(" | ")

        if len(parts) < 2:
            continue

        pod_name = parts[0]
        status = parts[1]


        # ====================================================
        # HEALTHY
        # ====================================================

        if status == "Running":

            st.markdown(
                f"""
                <div class="success-card">
                    🟢 <b>{pod_name}</b><br>
                    Status: <b>Running</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

            continue


        # ====================================================
        # FAILED POD
        # ====================================================

        st.markdown(
            f"""
            <div class="incident-card">
                🚨 <b>{pod_name}</b><br>
                Status: <b>{status}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # INVESTIGATION
        # ====================================================

        with st.expander(
            f"🔍 Investigate & Remediate — {pod_name}",
            expanded=True,
        ):

            # ------------------------------------------------
            # Collect evidence
            # ------------------------------------------------

            description = describe_pod(
                pod_name,
                namespace,
            )

            events = get_events(
                pod_name,
                namespace,
            )

            logs = get_logs(
                pod_name,
                namespace,
            )


            st.markdown(
                "## 🔎 Incident Investigation"
            )

            st.caption(
                "BigBlueOnCall collected Kubernetes evidence "
                "before proposing remediation."
            )


            # =================================================
            # Evidence tabs
            # =================================================

            tab1, tab2, tab3 = st.tabs(
                [
                    "📋 Pod Details",
                    "📅 Kubernetes Events",
                    "📜 Container Logs",
                ]
            )


            with tab1:

                st.code(
                    description,
                    language="text",
                )


            with tab2:

                if events:

                    st.code(
                        events,
                        language="text",
                    )

                else:

                    st.info(
                        "No Kubernetes events found."
                    )


            with tab3:

                if logs.startswith("Could not get logs"):

                    st.warning(
                        "⚠️ Application logs are unavailable "
                        "because the container has not successfully started."
                    )

                    st.caption(
                        "For ImagePullBackOff and other startup failures, "
                        "Kubernetes Events contain the relevant failure details."
                    )

                else:

                    st.code(
                        logs,
                        language="text",
                    )


            # =================================================
            # Investigation / Diagnosis
            # =================================================

            st.markdown(
                '<div class="section-title">🧠 BigBlueOnCall Investigation</div>',
                unsafe_allow_html=True,
            )


            findings = []


            if "ImagePullBackOff" in status:

                findings.append(
                    "The pod cannot start because Kubernetes "
                    "cannot pull the configured container image."
                )


            if "nginx:doesnotexist" in description:

                findings.append(
                    "The configured image is "
                    "`nginx:doesnotexist`, which is not a valid "
                    "image tag for this workload."
                )


            if "lookup registry-1.docker.io" in events:

                findings.append(
                    "Kubernetes Events also show DNS resolution "
                    "failure while contacting Docker Hub."
                )


            if "Could not get logs" in logs:

                findings.append(
                    "Container logs are unavailable because "
                    "the container never successfully started."
                )


            if findings:

                for i, finding in enumerate(
                    findings,
                    1,
                ):

                    st.markdown(
                        f"""
                        <div class="info-card">
                            <b>Evidence {i}</b><br>
                            {finding}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:

                st.info(
                    "No specific diagnosis was generated from "
                    "the currently collected evidence."
                )


            # =================================================
            # Proposed remediation
            # =================================================

            st.markdown(
                '<div class="section-title">🛠 Proposed Remediation</div>',
                unsafe_allow_html=True,
            )


            proposal = get_proposed_fix(
                pod_name,
                status,
                description,
                events,
            )


            if proposal:

                st.markdown(
                    f"### {proposal['title']}"
                )

                st.write(
                    proposal["reason"]
                )


                st.markdown(
                    "#### 💻 Commands BigBlueOnCall will execute"
                )

                st.code(
                    proposal["display"],
                    language="bash",
                )


                # =================================================
                # Human approval
                # =================================================

                st.markdown(
                    """
                    <div class="approval-card">
                    <b>👤 Human Approval Required</b><br>
                    Review the commands above before authorizing execution.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                approved = st.checkbox(
                    "I have reviewed these commands and approve the remediation.",
                    key=f"approve_{pod_name}",
                )


                if approved:

                    st.success(
                        "👤 Approval received. "
                        "The remediation is ready to execute."
                    )


                    if st.button(
                        "🚀 APPROVE & FIX INCIDENT",
                        type="primary",
                        key=f"execute_{pod_name}",
                    ):

                        with st.spinner(
                            "Executing approved remediation..."
                        ):

                            results = execute_fix(
                                proposal["commands"]
                            )


                        # =========================================
                        # Execution result
                        # =========================================

                        st.markdown(
                            "### 🚀 Remediation Execution"
                        )


                        all_success = True


                        for result in results:

                            st.code(
                                f"$ {result['command']}\n\n"
                                f"{result['stdout']}"
                                f"{result['stderr']}",
                                language="text",
                            )


                            if result["returncode"] == 0:

                                st.success(
                                    "✓ Command completed successfully."
                                )

                            else:

                                all_success = False

                                st.error(
                                    "✗ Command failed."
                                )


                        # =========================================
                        # Verification
                        # =========================================

                        if all_success:

                            st.markdown(
                                "### 🔍 Verification"
                            )

                            st.info(
                                "Checking Kubernetes workload health..."
                            )

                            time.sleep(2)

                            refreshed = list_pods(
                                namespace
                            )

                            verified = False

                            for refreshed_line in refreshed.splitlines():

                                refreshed_parts = (
                                    refreshed_line.split(" | ")
                                )

                                if len(refreshed_parts) < 2:
                                    continue

                                refreshed_pod = refreshed_parts[0]
                                refreshed_status = refreshed_parts[1]

                                if (
                                    refreshed_pod.startswith("broken-")
                                    and refreshed_status == "Running"
                                ):

                                    verified = True
                                    break


                            if verified:

                                st.success(
                                    "🎉 INCIDENT RESOLVED — "
                                    "the workload is now Running."
                                )


                                already_exists = any(
                                    item["pod"] == pod_name
                                    for item in st.session_state[
                                        "resolved_incidents"
                                    ]
                                )


                                if not already_exists:

                                    st.session_state[
                                        "resolved_incidents"
                                    ].append(
                                        {
                                            "pod": pod_name,
                                            "title": proposal["title"],
                                            "commands": proposal["display"],
                                        }
                                    )


                                st.balloons()

                                st.info(
                                    "Click **Scan Cluster** to refresh "
                                    "the dashboard."
                                )

                            else:

                                st.warning(
                                    "Commands completed, but the workload "
                                    "has not yet reached Running state."
                                )


            else:

                st.info(
                    "No safe remediation is currently available "
                    "for this incident."
                )


# ============================================================
# Resolved Incidents
# ============================================================

if st.session_state["resolved_incidents"]:

    st.markdown(
        '<div class="section-title">✅ Resolved Incidents</div>',
        unsafe_allow_html=True,
    )


    for incident in reversed(
        st.session_state["resolved_incidents"]
    ):

        st.markdown(
            f"""
            <div class="resolved-card">
                🟢 <b>{incident['pod']}</b><br>
                {incident['title']}<br>
                Human approval → Remediation → Verification
            </div>
            """,
            unsafe_allow_html=True,
        )


        with st.expander(
            f"View resolution — {incident['pod']}"
        ):

            st.markdown(
                "**Approved commands:**"
            )

            st.code(
                incident["commands"],
                language="bash",
            )

            st.success(
                "✓ Human approval received"
            )

            st.success(
                "✓ Remediation executed"
            )

            st.success(
                "✓ Workload verified"
            )
