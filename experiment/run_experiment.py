from psychopy import visual, core, event, gui
import random
import csv
import os
import re
from pathlib import Path

# Resolve paths relative to the repository so the experiment can be launched
# from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
ASSET_DIR = Path(__file__).resolve().parent / "assets"

# =====================================================
# 1. Participant Management and Data Initialization
# =====================================================

# Create the directory used to store generated participant files.

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Generate the next available participant ID based on
# previously saved participant files

def get_next_participant_id():
    ids = []

    # Search both participant-group folders for previously used IDs.
    for file in DATA_DIR.glob("*/participant_*.csv"):
        match = re.match(
            r"participant_(\d+)\.csv",
            file.name
        )
        if match:
            ids.append(
                int(match.group(1))
            )

    # Start numbering from 001 when no participant files exist.
    if len(ids) == 0:
        return "001"

    # Return the next available ID with three-digit formatting.
    return f"{max(ids)+1:03d}"


# Collect participant ID and group, then prepare the participant output file.

while True:

    # Suggest the next participant ID automatically.
    suggested_id = get_next_participant_id()

    participant_info = {
        "Participant ID": suggested_id,
        "Gender": ["Female", "Male"]
    }

    # Collect an anonymous participant code and the analysis group.
    dlg = gui.DlgFromDict(
        participant_info,
        title="Participant Information"
    )

    # Exit experiment if the dialog is cancelled.
    if not dlg.OK:
        core.quit()

    participant_id = str(
        participant_info["Participant ID"]
    ).strip()
    gender = participant_info["Gender"]

    # Accept only numeric anonymous participant codes.
    if not re.fullmatch(r"\d{3,}", participant_id):
        warning = gui.Dlg(
            title="Invalid Participant ID"
        )
        warning.addText(
            "Enter a numeric anonymous participant code "
            "containing at least three digits."
        )
        warning.show()
        continue

    # Store each participant file in the group folder expected by the notebook.
    participant_folder = DATA_DIR / gender
    participant_folder.mkdir(
        parents=True,
        exist_ok=True
    )
    filename = participant_folder / f"participant_{participant_id}.csv"

    # Check whether the participant code has already been used in either group.
    existing_files = list(
        DATA_DIR.glob(f"*/participant_{participant_id}.csv")
    )

    if existing_files:

        # Do not allow one participant code to be assigned to two groups.
        if existing_files[0].parent != participant_folder:
            warning = gui.Dlg(
                title="Participant ID already used"
            )
            warning.addText(
                f"Participant ID {participant_id} is already assigned "
                "to another group. Enter a different code."
            )
            warning.show()
            continue

        overwrite = gui.Dlg(
            title="File exists"
        )

        overwrite.addText(
            f"Participant {participant_id} already exists in {gender}.\n"
            "Overwrite this file?"
        )

        overwrite.addField(
            "Overwrite",
            choices=[
                "Yes",
                "No"
            ]
        )

        result = overwrite.show()

        if result is not None and result[0] == "Yes":
            break
        else:
            continue

    else:
        break

# Initialize participant data file

data_file = open(
    filename,
    "w",
    newline="",
    encoding="utf-8"
)

# Initialize CSV writer
writer = csv.writer(data_file)


# Write data column headers
writer.writerow([
    "trial",
    "choice",
    "outcome",
    "choice_rt",
    "confidence_level",
    "confidence_rt",
    "card probs"
])

# =====================================================
# 2. Experiment Window Initialization
# =====================================================

# Create the PsychoPy window used for stimulus presentation
win = visual.Window(
    size=(1200, 800),
    color="black",
    units="pix",
    allowGUI=True,
    checkTiming=False
)

# Bring the experiment window to the foreground
# to ensure keyboard responses are correctly detected
try:
    win.winHandle.activate()
    win.winHandle.set_focus()
except:
    pass

# =====================================================
# 3. Experiment Termination and Exit Handling
# =====================================================

# Safely close data file and PsychoPy window
# when the experiment is terminated
def quit_experiment():
    try:
        data_file.flush()
        data_file.close()
    except:
        pass
    win.close()
    core.quit()

# Allow the experimenter to terminate the task using ESC
event.globalKeys.add(
    key="escape",
    func=quit_experiment
)

# Handle window close button to safely terminate the experiment
try:
    win.winHandle.protocol(
        "WM_DELETE_WINDOW",
        quit_experiment
    )
except:
    pass

# =====================================================
# 4. Experiment Parameters and Task Configuration
# =====================================================

# Define keyboard keys used for card selection
choice_keys = [
    "a",
    "d",
    "g",
    "j"
]

# Define keyboard keys used for confidence rating
confidence_keys = [
    "1",
    "2",
    "3",
    "4",
    "5"
]

# Define reward probability associated with each card
# These values determine the reinforcement structure
reward_probability = {
    0: 0.70,
    1: 0.60,
    2: 0.50,
    3: 0.40
}

# Define the number of trials in each experimental block
blocks = [
    15,
    30,
    60
]

# Define card background colors for different blocks
# to provide contextual changes between blocks
block_card_colors = {
    1: "gray",
    2: "slategray",
    3: "tan"
}


# =====================================================
# 5. Visual Stimulus and Interface Components
# =====================================================

# Start screen displayed before the experiment begins
start_text = visual.TextStim(
    win,
    text=
    "Welcome!\n\n"
    "Press SPACE to start\n\n"
    "ESC to quit",
    color="white",
    height=45
)

# Instruction pages shown before the first block:

# First instruction page: general task procedure
instruction_page1 = visual.TextStim(
    win,
    text=
    "In this experiment, you will repeatedly choose "
    "one card from a set of four cards.\n\n"

    "Each trial consists of three steps:\n\n"

    "1. Choose a card\n"
    "Select one card by pressing:\n\n"
    "A        D        G        J\n\n"

    "2. Rate your confidence\n"
    "Report how confident you are using:\n\n"
    "1 = Lowest confidence\n"
    "5 = Highest confidence\n\n"

    "3. Receive feedback\n"
    "After your response, feedback will indicate "
    "whether your choice resulted in a reward.\n\n"

    "Press SPACE to continue",

    color="white",
    height=28,
    wrapWidth=1000
)

# Second instruction page: task strategy and block information
instruction_page2 = visual.TextStim(
    win,
    text=
    "Important Instructions\n\n"

    "• The experiment consists of several blocks of trials.\n\n"

    "• Card positions may change between blocks, "
    "but they remain fixed during each block.\n\n"

    "• Try to learn from the feedback you receive "
    "and use it to guide your future choices.\n\n"

    "• There is no time limit for making choices "
    "or reporting confidence.\n\n"

    "• Please keep your attention on the screen "
    "throughout the experiment.\n\n"

    "When you are ready, press SPACE to begin.",

    color="white",
    height=30,
    wrapWidth=1000
)

# Text object used for block start and end messages
block_text = visual.TextStim(
    win,
    text="",
    color="white",
    height=45
)

# Instruction displayed during card selection trials
instruction = visual.TextStim(
    win,
    text="Choose a card: a   d   g   j",
    color="white",
    height=35,
    pos=(0,300)
)

# Confidence rating screen
confidence_text = visual.TextStim(
    win,
    text=
    "How confident are you?\n\n"
    "1      2      3      4      5\n\n"
    "1 = lowest confidence\n"
    "5 = highest confidence",

    color="white",
    height=35
)

# Feedback text displayed after each trial
feedback_text = visual.TextStim(
    win,
    text="",
    color="white",
    height=40,
    pos=(0,-300)
)

# =====================================================
# 4. Card Stimulus Configuration
# =====================================================

# Define the positions of the four cards on the screen
positions = [
    (-450,0),
    (-150,0),
    (150,0),
    (450,0)
]

# Store card objects and their labels
cards = []
labels = []

# Create an outline used to highlight the selected card
selected_outline = visual.Rect(
    win,
    width=170,
    height=260,
    fillColor=None,
    lineColor=[0.8, -0.8, 0.8],
    lineWidth=4
)

# Create card stimuli and corresponding key labels
for i, pos in enumerate(positions):
    # Create card background object
    card = visual.Rect(
        win,
        width=170,
        height=260,
        fillColor="gray",
        lineColor="gray",
        pos=pos
    )
    cards.append(card)

    # Create keyboard label above each card
    label = visual.TextStim(
        win,
        text=choice_keys[i],
        color="white",
        height=45,
        pos=(
            pos[0],
            pos[1]+170
        )
    )

    labels.append(label)




# =====================================================
# 5. Feedback Stimulus Configuration
# =====================================================

# Create visual stimulus for positive feedback
# displayed when the selected card receives a reward
treasure = visual.ImageStim(
    win,
    image=str(ASSET_DIR / "treasure.png"),
    size=(120,120),
    interpolate=True
)

# Create visual stimulus for negative feedback
# displayed when the selected card does not receive a reward
cross = visual.ImageStim(
    win,
    image=str(ASSET_DIR / "cross.png"),
    size=(120,120),
    interpolate=True
)

# =====================================================
# 6. Keyboard Response and Experiment Control Functions
# =====================================================

def wait_space():

    """
    Wait indefinitely until the participant presses SPACE.
    Used for instruction screens and block transitions.
    """

    # Clear previous keyboard events
    event.clearEvents()

    # Ensure the PsychoPy window remains focused
    try:
        win.winHandle.activate()
        win.winHandle.set_focus()

    except:
        pass

    while True:

        # Check for valid keys
        keys = event.getKeys(
            keyList=[
                "space",
                "escape"
            ]
        )

        # Allow experiment termination using ESC
        if "escape" in keys:

            quit_experiment()

        # Continue when SPACE is pressed
        if "space" in keys:

            return

        core.wait(0.01)


def get_key(valid_keys):

    """
    Collect a participant response without a time limit.

    Returns:
        - pressed key
        - reaction time
    """

    # Remove previous keyboard events
    event.clearEvents()

    # Start reaction time measurement
    clock = core.Clock()

    while True:

        # Check whether one of the valid response keys was pressed
        keys = event.getKeys(
            keyList=valid_keys
        )

        if keys:

            return (
                keys[0],
                clock.getTime()
            )

        # Allow emergency exit during response collection
        if "escape" in event.getKeys():

            quit_experiment()

        core.wait(0.01)


# =====================================================
# 7. Instruction and Block Transition Screens
# =====================================================

def show_instructions():

    """
    Display the two instruction pages before the experiment starts.
    """

    # Display first instruction page
    instruction_page1.draw()
    win.flip()
    wait_space()

    # Display second instruction page
    instruction_page2.draw()
    win.flip()
    wait_space()

def show_block_start(block_number):

    """
    Display block start message and wait for participant confirmation.
    """

    block_text.text = (
        f"Block {block_number} is starting\n\n"
        "Press SPACE to continue"
    )
    block_text.draw()
    win.flip()
    wait_space()

def show_block_end(block_number):

    """
    Display block completion message and wait before continuing.
    """

    block_text.text = (
        f"Block {block_number} finished\n\n"
        "Press SPACE to continue"
    )

    block_text.draw()
    win.flip()

    wait_space()

# =====================================================
# 8. Card Rendering Function
# =====================================================

def draw_cards(block_number):

    """
    Draw all cards with the color associated with
    the current experimental block.
    """

    for i in range(4):

        # Update card appearance according to current block
        cards[i].fillColor = block_card_colors[block_number]
        cards[i].lineColor = block_card_colors[block_number]

        # Draw card and corresponding keyboard label
        cards[i].draw()
        labels[i].draw()

# =====================================================
# 9. Trial Execution and Behavioral Data Collection
# =====================================================

def run_trial(block, trial, global_trial, card_order, card_probs):

    """
    Execute one experimental trial.

    The trial consists of:
    1. Card selection
    2. Confidence rating
    3. Probabilistic reward calculation
    4. Feedback presentation
    5. Behavioral data saving
    """

    # -------------------------------------------------
    # Step 1: Card selection
    # -------------------------------------------------

    # Display card selection instructions and cards
    instruction.draw()
    draw_cards(block)
    win.flip()

    # Collect participant's card selection response
    choice_key, choice_RT = get_key(
        choice_keys
    )

    # Convert pressed key into card position index
    selected_position = choice_keys.index(
        choice_key
    )

    # Map screen position to the actual card identity
    # according to the current block arrangement
    selected_card = card_order[selected_position]

    # -------------------------------------------------
    # Step 2: Confidence rating
    # -------------------------------------------------

    # Display confidence scale
    confidence_text.draw()
    win.flip()

    # Collect confidence response (1-5)
    confidence_key, confidence_RT = get_key(
        confidence_keys
    )

    confidence = int(confidence_key)

    # -------------------------------------------------
    # Step 3: Probabilistic reward calculation
    # -------------------------------------------------

    # Generate random value and compare it with
    # the selected card's reward probability
    
    random_value = random.random()
    

    reward = (
        random_value
        <
        reward_probability[selected_card]
    )

    # -------------------------------------------------
    # Step 4: Present selected card and feedback
    # -------------------------------------------------

    # Redraw cards before showing feedback
    draw_cards(block)

    # Highlight the selected card with a colored outline
    selected_outline.pos = positions[selected_position]
    selected_outline.draw()

    # Define feedback image position below the selected card
    feedback_position = (
        positions[selected_position][0],
        -250
    )

    # Display reward or no-reward feedback
    if reward:
        treasure.pos = feedback_position
        treasure.draw()

    else:
        cross.pos = feedback_position
        cross.draw()

    win.flip()

    # Keep feedback visible for two seconds
    core.wait(2)

    # -------------------------------------------------
    # Step 5: Prepare next trial
    # -------------------------------------------------

    # Clear feedback display
    win.flip()

    # Short pause before the next trial starts
    core.wait(0.5)

    # -------------------------------------------------
    # Step 6: Save trial data
    # -------------------------------------------------

    writer.writerow([
        global_trial,
        selected_position,
        "win" if reward else "lose",
        choice_RT,
        confidence,
        confidence_RT,
        card_probs
    ])

    # Ensure data is written immediately to disk
    data_file.flush()

    return reward

# =====================================================
# 10. Experiment Execution and Block Management
# =====================================================

# Start experiment and display instructions

# Display initial welcome screen
start_text.draw()
win.flip()

# Wait until participant starts the experiment
wait_space()

# Display task instructions
show_instructions()

# Ensure the experiment window remains focused
# for correct keyboard response detection
try:
    win.winHandle.activate()
    win.winHandle.set_focus()
except:
    pass

# Wait for participant readiness before starting blocks
wait_space()

# Reward counters for each block.
# A reward is not the same as an optimal choice in a probabilistic task.
block_reward_count = {
    1: 0,
    2: 0,
    3: 0
}

# Run experimental blocks
for block_number, n_trials in enumerate(blocks, start=1):
    # Display block introduction screen
    show_block_start(
        block_number
    )

    # Generate card arrangement for current block
    # Card positions are randomized only once per block
    # and remain fixed during all trials in that block

    card_order = [
        0,
        1,
        2,
        3
    ]

    # Randomize card identities at block onset
    random.shuffle(card_order)

    # Store reward probabilities according to
    # the current card arrangement
    card_probs = [
        reward_probability[card_order[0]],
        reward_probability[card_order[1]],
        reward_probability[card_order[2]],
        reward_probability[card_order[3]]
    ]

    # Execute trials within the current block
    for trial in range(1, n_trials + 1):
        global_trial = sum(blocks[:block_number - 1]) + trial - 1

        reward = run_trial(
            block=block_number,
            trial=trial,
            global_trial=global_trial,
            card_order=card_order,
            card_probs=card_probs
        )

        if reward:
            block_reward_count[block_number] += 1

    # Display block completion message
    show_block_end(
        block_number
    )

# Save participant summary results

summary_file = DATA_DIR / "summary_results.csv"
file_exists = os.path.exists(summary_file)

with open(
    summary_file,
    "a",
    newline="",
    encoding="utf-8"
) as f:
    writer_summary = csv.writer(f)
    # Write header only for a new file
    if not file_exists:
        writer_summary.writerow([
            "participant_id",
            "block_1_reward_count",
            "block_2_reward_count",
            "block_3_reward_count",
            "total_reward_count"
        ])

    total_reward_count = (
        block_reward_count[1]
        + block_reward_count[2]
        + block_reward_count[3]
    )

    writer_summary.writerow([
        participant_id,
        block_reward_count[1],
        block_reward_count[2],
        block_reward_count[3],
        total_reward_count
    ])

# =====================================================
# 11. Experiment Completion and Termination
# =====================================================

# Create final message displayed after all blocks
end_text = visual.TextStim(
    win,
    text=
    "Experiment finished\n\n"
    "Thank you!",
    color="white",
    height=45
)

# Display completion message
end_text.draw()
win.flip()

# Keep final screen visible briefly
core.wait(5)

# Safely close the experiment
quit_experiment()