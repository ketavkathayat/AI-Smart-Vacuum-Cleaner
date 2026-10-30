
import streamlit as st
import pandas as pd
import time

from config import MAX_BATTERY, CLEAN_COST
from environment import Environment
from state import VacuumState

from agents.goal_agent import choose_target as goal_agent
from agents.utility_agent import choose_target as utility_agent

from algorithms.astar import search as astar_search

from simulation.battery import (
    required_battery,
    recharge_vacuum
)

from simulation.movement import move_one_step

from simulation.cleaning import (
    clean_current_area,
    cleaning_completed
)


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Smart Vacuum Cleaner",
    page_icon="🤖",
    layout="wide"
)


# INITIALIZE ENVIRONMENT

if "environment" not in st.session_state:

    st.session_state.environment = Environment()

    st.session_state.vacuum = VacuumState(
        st.session_state.environment.start
    )

    st.session_state.last_algorithm = "A*"
    st.session_state.last_agent = "Goal-Based Agent"

env = st.session_state.environment
vacuum = st.session_state.vacuum


# GRID DISPLAY FUNCTION

def create_grid():

    grid = []

    for r in range(env.size):

        row = []

        for c in range(env.size):

            pos = (r, c)

            if pos == vacuum.position:
                symbol = "🤖"

            elif pos == env.charging_station:
                symbol = "🔋"

            elif pos in env.obstacles:
                symbol = "⬛"

            elif pos in env.dirty_areas:
                level = env.dirt_levels.get(pos, 1)
                symbol = f"🟥{level}"

            elif pos in env.cleaned_areas:
                symbol = "🟩"

            else:
                symbol = "⬜"

            row.append(symbol)

        grid.append(row)

    return pd.DataFrame(grid)


# ANIMATION FUNCTION

def animate_path(path, placeholder, delay=0.08):

    for position in path[1:]:

        success = move_one_step(
            env,
            vacuum,
            position
        )

        if not success:
            return False

        placeholder.dataframe(
            create_grid(),
            width="stretch",
            hide_index=True
        )

        time.sleep(delay)

    return True


# HEADER

st.title("🤖 AI Smart Vacuum Cleaner")

st.caption(
    "Autonomous House Cleaning Using Artificial Intelligence"
)

st.divider()


# SIDEBAR

st.sidebar.title("⚙️ AI Configuration")

algorithm = st.sidebar.selectbox(
    "Search Algorithm",
    [
        "BFS",
        "DFS",
        "Uniform Cost Search",
        "Greedy Best-First Search",
        "A*"
    ],
    key="algorithm_selection"
)

agent_type = st.sidebar.selectbox(
    "Intelligent Agent",
    [
        "Goal-Based Agent",
        "Utility-Based Agent"
    ],
    key="agent_selection"
)

animation_speed = st.sidebar.slider(
    "Animation Speed",
    0.01,
    0.5,
    0.08
)


# PERFORMANCE DASHBOARD

st.subheader("📊 Live Performance")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Battery", f"{vacuum.battery}%")

c2.metric(
    "Cleaned Areas",
    len(env.cleaned_areas)
)

c3.metric(
    "Remaining Dirt",
    len(env.dirty_areas)
)

c4.metric(
    "Distance Travelled",
    vacuum.distance_travelled
)

st.divider()


# HOUSE ENVIRONMENT

st.subheader("🏠 House Environment")

st.write(
    "🤖 Vacuum | 🟥 Dirty | 🟩 Cleaned | "
    "⬛ Obstacle | 🔋 Charging | ⬜ Empty"
)

grid_placeholder = st.empty()

grid_placeholder.dataframe(
    create_grid(),
    width="stretch",
    hide_index=True
)


# SIMULATION CONTROLS

st.divider()

st.subheader("🚀 Automatic AI Cleaning")

start_button = st.button(
    "▶ Start Automatic Cleaning",
    type="primary",
    width="stretch"
)


if start_button:

    progress = st.progress(0)

    status_box = st.empty()

    animation_box = st.empty()

    explored_total = 0

    cleaned_count = 0

    total_initial = len(env.dirty_areas)

    agent_function = (
        goal_agent
        if agent_type == "Goal-Based Agent"
        else utility_agent
    )

    st.session_state.last_algorithm = algorithm
    st.session_state.last_agent = agent_type

    # CLEAN ALL REACHABLE AREAS

    while env.dirty_areas:

        target, path, explored, score = agent_function(
            env,
            vacuum.position,
            algorithm
        )

        explored_total += explored

        if not path or target is None:
            status_box.warning(
                "No more reachable dirty areas."
            )
            break

        # Calculate return path for battery safety

        home_path, _, _ = astar_search(
            env,
            target,
            env.charging_station
        )

        if not home_path:
            status_box.warning(
                "Charging station is unreachable."
            )
            break

        required = required_battery(
            path,
            home_path
        )

        # Recharge if required

        if vacuum.battery < required:

            status_box.info(
                "🔋 Battery management: Returning to charging station..."
            )

            charge_path, _, _ = astar_search(
                env,
                vacuum.position,
                env.charging_station
            )

            if not charge_path:
                status_box.error(
                    "Unable to reach charging station."
                )
                break

            if vacuum.battery < len(charge_path) - 1:
                status_box.error(
                    "Insufficient battery to reach charging station."
                )
                break

            if not animate_path(
                charge_path,
                grid_placeholder,
                animation_speed
            ):
                break

            recharge_vacuum(vacuum)

            status_box.success(
                "Battery fully charged!"
            )

        # Move to selected dirty area

        status_box.info(
            f"🤖 Moving towards dirty area {target}"
        )

        success = animate_path(
            path,
            grid_placeholder,
            animation_speed
        )

        if not success:
            status_box.error("Movement failed.")
            break

        # Clean area

        if clean_current_area(env, vacuum):

            cleaned_count += 1

            status_box.success(
                f"🧹 Area {target} cleaned successfully!"
            )

        progress.progress(
            min(
                1.0,
                cleaned_count / max(total_initial, 1)
            )
        )

        grid_placeholder.dataframe(
            create_grid(),
            width="stretch",
            hide_index=True
        )

    # Return to charging station after cleaning

    if cleaning_completed(env):

        return_path, _, _ = astar_search(
            env,
            vacuum.position,
            env.charging_station
        )

        if return_path:

            if vacuum.battery >= len(return_path) - 1:

                status_box.info(
                    "Returning to charging station..."
                )

                animate_path(
                    return_path,
                    grid_placeholder,
                    animation_speed
                )

        progress.progress(1.0)

        if cleaning_completed(env):
            status_box.success(
                "🎉 Cleaning completed successfully!"
            )

    vacuum.nodes_explored += explored_total

    st.rerun()


# ADDITIONAL OPERATIONS

st.divider()

st.subheader("🛠️ Environment Controls")

col1, col2 = st.columns(2)

with col1:

    if st.button("Generate New Dirt"):

        env.generate_dirt(1)

        st.rerun()

with col2:

    if st.button("Reset Simulation"):

        st.session_state.environment = Environment()

        st.session_state.vacuum = VacuumState(
            st.session_state.environment.start
        )

        st.rerun()


# FINAL STATISTICS

st.divider()

st.subheader("📋 Simulation Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Nodes Explored",
    vacuum.nodes_explored
)

col2.metric(
    "Cleaning Time",
    vacuum.cleaning_time
)

col3.metric(
    "Total Areas Cleaned",
    vacuum.total_cleaned
)

st.write("**Selected Algorithm:**", algorithm)

st.write("**Selected Agent:**", agent_type)

st.write("**Vacuum Position:**", vacuum.position)

st.write("**Current Status:**", vacuum.status)

if cleaning_completed(env):

    st.success("All reachable dirty areas have been cleaned.")
