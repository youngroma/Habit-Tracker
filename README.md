# Habit Graph Tracker

## Project Description

The **Habit Tracker** is a web-based application designed to help users monitor their habits, both good and bad. The primary goal of this project is to allow users to track the frequency of their habits over time and visualize their progress using interactive graphs. 

With the Habit Tracker, users can:

- Add new habits they want to track.
- Mark a habit as repeated (or performed) on a daily or periodic basis.
- View graphical representations of their habits' progress, including the frequency and consistency of each habit.

By repeating a habit, the user records data on a graph, allowing them to visualize how frequently they engage in the habit and track any patterns over time. This visualization helps the user understand whether they are making progress or need to improve.

---

## Setup Instructions

Follow the instructions below to set up the Habit Tracker project on your local machine.

### Prerequisites

1. **Python** (version 3.1 or later) is required.
2. **Flask** web framework is used in this project. You can install it using pip.

### Installation Steps

1. **Clone the Repository:**

   Begin by cloning the repository to your local machine:

   ```bash
   git clone https://github.com/youngroma/Habit-Tracker.git
   ```

### Install Dependencies:

2. **Navigate to the project directory and install the necessary dependencies:**

  ```bash
  cd Habit-Tracker
  pip install -r requirements.txt
  ```


### Set up the Database:

3. **Run the following command to initialize the database:**
  ```bash
  flask db init
  flask db migrate
  flask db upgrade
  ```

## Run the Application:

After setting up the database, start the Flask development server:

```bash
flask run
```
The application should now be running on http://127.0.0.1:5000/.
