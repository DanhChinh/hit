import numpy as np
import time
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression

# Import rich for live table display
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.text import Text

# Import your custom functions from env.py (assuming they exist)
# from env import make_data, handle_progress

# --- MOCK env.py functions for demonstration ---
# (Remove these mocks if you have your actual env.py)
def make_data():
    # Simulate data generation for demonstration
    X = np.random.rand(1000, 10) # 1000 samples, 10 features
    y = np.random.randint(0, 2, 1000) # Binary labels
    # Simulate a scaler
    class MockScaler:
        def transform(self, data):
            return np.array(data) * 10 # Just a simple transformation
    return MockScaler(), X, y

def handle_progress(progress_val, isEnd=False):
    # Simulate handling progress and returning a feature vector
    return [progress_val * i for i in range(10)]
# --- END MOCK ---

def isPass(data, label, x_pred):
    model = RandomForestClassifier(random_state=42) # Added random_state for reproducibility
    model.fit(data, label)
    probabilities = model.predict_proba(x_pred)[0]
    return round(probabilities[1], 2)

class Model:
    def __init__(self, data, label, model_instance, model_name):
        self.model = model_instance # Renamed 'model' to 'model_instance' to avoid confusion with self.model_name
        self.label_percent = 0
        self.model_name = model_name
        self.x_test = None # Initialize to None
        self.mask = None # Initialize to None
        self.filter(data, label) # Call filter during initialization
        self.hs = [] # History of checks
        self.sid = None
        self.predict_value = None # Renamed 'predict' to 'predict_value' to avoid conflict with method name
        self.probability = 0 # Store the probability for display
        self.percent = 0 # Percentage of correct checks

    def filter(self, data, label):
        # Ensure label_percent is calculated at least once, or until condition is met
        attempts = 0
        max_attempts = 100 # Prevent infinite loops if condition is never met
        while self.label_percent < 0.1 and attempts < max_attempts:
            x_train, self.x_test, y_train, y_test = train_test_split(
                data, label,
                train_size=0.19,
                test_size=0.019,
                shuffle=True,
                stratify=label,
                random_state=random.randint(0, 10000) # New random state for each split
            )

            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(self.x_test)
            self.mask = (y_pred == y_test) # Boolean mask
            self.label_percent = round(sum(self.mask) / len(self.mask), 2)
            # print(f"Ti le nhan dung cua {self.model_name}:{self.label_percent}") # Can comment this out, rich will show it

            attempts += 1
        if attempts == max_attempts and self.label_percent < 0.1:
            print(f"[WARNING] {self.model_name}: Could not reach 0.1 label_percent after {max_attempts} attempts.")


    def make_predict(self, current_sid, x_pred): # Pass sid as argument
        self.sid = current_sid # Assign the current sid to the model instance
        if self.x_test is None or self.mask is None:
            # Handle case where filter might not have run or failed
            self.probability = 0
            self.predict_value = None
            return None

        # self.x_test should be a 2D array for isPass (model.fit expects 2D)
        # self.mask should be 1D array of labels (True/False)
        self.probability = isPass(self.x_test, self.mask, x_pred)

        if self.probability >= 0.6:
            # Re-predict using the actual model, not isPass again
            # The 'isPass' function is for determining the probability of a 'pass' on a given x_pred,
            # using a RandomForest trained on the model's test set and mask.
            # The actual prediction from THIS model should come from self.model.predict
            # Let's assume predict_proba for the actual prediction as well for consistency with `isPass`'s output logic
            try:
                # Predict from the model itself, not from the RandomForest trained on x_test/mask
                self.predict_value = int(self.model.predict(x_pred)[0])
            except Exception as e:
                print(f"Error predicting with {self.model_name}: {e}")
                self.predict_value = None
        else:
            self.predict_value = None
        return self.predict_value

    def check(self, current_sid, result): # Pass sid as argument
        if self.sid is None:
            # print(f"{self.model_name} is not sid set") # Debug print, can remove
            return
        if self.sid != current_sid: # Compare with current_sid passed in
            # print(f"{self.model_name} != current sid (stale prediction)") # Debug print, can remove
            return
        if self.predict_value is None: # Use self.predict_value
            # print(f"{self.model_name} is not predict set") # Debug print, can remove
            return

        # Ensure self.hs is initialized as a list before appending
        if not isinstance(self.hs, list):
            self.hs = []

        if self.predict_value == result:
            self.hs.append(1)
        else:
            self.hs.append(0)

        # Ensure hs is not empty to avoid ZeroDivisionError
        if len(self.hs) > 0:
            self.percent = round(sum(self.hs) / len(self.hs), 2)
        else:
            self.percent = 0


    def to_dict(self):
        """
        Trả về các thuộc tính của đối tượng dưới dạng một từ điển.
        Tên các khóa trong từ điển được đặt theo yêu cầu của bạn.
        """
        return {
            "ID": self.sid if self.sid is not None else "N/A", # Display N/A if sid not set
            "Tên Model": self.model_name,
            "Độ chính xác Lb.": f"{self.label_percent:.2f}",
            "Khả năng Pass": f"{self.probability:.2f}", # Probability from isPass
            "Dự đoán": str(self.predict_value) if self.predict_value is not None else "---",
            "Tỷ lệ đúng": f"{self.percent:.2f}",
            "Lịch sử": len(self.hs) # Display length of history for brevity in table
        }

# --- MAIN SCRIPT EXECUTION ---

scaler, data, label = make_data()

classifiers = {}
# Initialize multiple RandomForest models
for i in range(5): # Let's create 5 RandomForest models for demonstration
    classifiers[f"RandomForest_{i}"] = Model(data, label, RandomForestClassifier(random_state=i), f"RF_{i}")
    # print(f"Initialized {classifiers[f'RandomForest_{i}'].model_name} with label_percent: {classifiers[f'RandomForest_{i}'].label_percent}")

# Global sid (this will change per prediction cycle)
current_global_sid = 0

# --- RICH TABLE DISPLAY ---
console = Console()

def generate_table(models_dict):
    table = Table(title="Trạng thái Mô hình Học máy", show_header=True, header_style="bold green")

    # Define columns explicitly for better control and order
    columns = ["ID", "Tên Model", "Độ chính xác Lb.", "Khả năng Pass", "Dự đoán", "Tỷ lệ đúng", "Lịch sử"]
    for col_name in columns:
        if col_name == "Dự đoán":
            table.add_column(col_name, justify="center", style="bold yellow")
        elif col_name == "Tỷ lệ đúng":
            table.add_column(col_name, justify="right", style="bold cyan")
        elif col_name == "Khả năng Pass":
             table.add_column(col_name, justify="right", style="magenta")
        else:
            table.add_column(col_name)

    # Add rows
    for model_name, model_obj in models_dict.items():
        model_data = model_obj.to_dict()
        row_values = [
            model_data["ID"],
            model_data["Tên Model"],
            model_data["Độ chính xác Lb."],
            model_data["Khả năng Pass"],
            model_data["Dự đoán"],
            model_data["Tỷ lệ đúng"],
            str(model_data["Lịch sử"])
        ]
        # Optional: Add color coding to the prediction column
        if model_data["Dự đoán"] == "1":
            row_values[4] = Text(model_data["Dự đoán"], style="bold green")
        elif model_data["Dự đoán"] == "0":
            row_values[4] = Text(model_data["Dự đoán"], style="bold red")
        else:
            row_values[4] = Text(model_data["Dự đoán"], style="dim")

        table.add_row(*row_values)
    return table

# Main loop for continuous operation with Rich Live display
print("Bắt đầu mô phỏng hoạt động của các mô hình. Nhấn Ctrl+C để thoát.")
with Live(generate_table(classifiers), refresh_per_second=1, screen=True) as live:
    try:
        simulation_steps = 10 # Run for 100 simulation steps
        for step in range(simulation_steps):
            current_global_sid = f"SESS_{step+1:03d}" # Generate a new SID for each step

            # 1. Simulate new incoming data (x_pred)
            progress_val = random.uniform(0.1, 10.0)
            x_pred_raw = handle_progress(progress_val, isEnd=False)
            x_pred_scaled = scaler.transform([x_pred_raw])
            x_pred_final = np.round(x_pred_scaled, 1)

            # 2. Each model makes a prediction
            ensemble_c1 = 0
            ensemble_c2 = 0
            for name, model in classifiers.items():
                y_pred_model = model.make_predict(current_global_sid, x_pred_final) # Pass current_global_sid
                if y_pred_model is not None:
                    if y_pred_model == 1:
                        ensemble_c1 += 1
                    else:
                        ensemble_c2 += 1

            # Determine the "true" result for checking (simulated)
            # For demonstration, let's say true result is 1 if more than half predict 1, else 0
            simulated_true_result = 1 if ensemble_c1 >= ensemble_c2 else 0
            if ensemble_c1 == 0 and ensemble_c2 == 0: # If no model made a prediction
                simulated_true_result = random.randint(0,1) # Fallback random

            # 3. Check predictions against the simulated true result
            for name, model in classifiers.items():
                model.check(current_global_sid, simulated_true_result) # Pass current_global_sid

            # 4. Update the live display
            live.update(generate_table(classifiers))

            time.sleep(0.5) # Pause for half a second

    except KeyboardInterrupt:
        live.console.print("\n[bold red]Đã dừng mô phỏng.[/bold red]")
    finally:
        # Ensure the cursor is at the end of the content after Live finishes
        live.console.print("\n")