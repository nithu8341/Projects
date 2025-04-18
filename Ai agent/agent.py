import os
import google.generativeai as genai
import subprocess

# Get API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# Ask Gemini to generate code for the given task
def generate_code(task):
    prompt = f"Write simple, runnable Python code to do the following task:\n{task}\nOnly return valid Python code without any explanation or markdown formatting."
    response = model.generate_content(prompt)
    code = response.text.strip()

    # Remove markdown-style code block formatting if present
    if code.startswith("```"):
        code = code.strip("`")
        lines = code.splitlines()
        if lines[0].lower().startswith("python"):
            lines = lines[1:]
        code = "\n".join(lines).strip()

    return code

# Write code to a .py file
def save_code_to_file(code, filename="task_code.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    return filename

# Run the code using subprocess
def run_code(filename="task_code.py"):
    try:
        subprocess.run(["python", filename], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Error during execution:\n", e)
        return False

# Retry flow with user feedback
def handle_failure(task):
    while True:
        reason = input("Why did it fail? ")
        updated_task = f"The previous task had this issue: {reason}. Please fix it and return corrected code."
        fixed_code = generate_code(updated_task)
        filename = save_code_to_file(fixed_code)
        print("\nUpdated code:\n")
        print(fixed_code)
        approve = input("\nDo you want to run this updated code? (y/n): ")
        if approve.lower() == "y":
            if run_code(filename):
                print("Task completed successfully after retry.")
                return
        else:
            print("Retry aborted.")
            return

# Main flow
def main():
    print("What task should the AI agent perform?")
    task = input("> ")

    print("\nGenerating code...\n")
    try:
        code = generate_code(task)
        print("Generated code:\n")
        print(code)

        approve = input("\nDo you want to run this code? (y/n): ")
        if approve.lower() == "y":
            filename = save_code_to_file(code)
            if run_code(filename):
                print("Task completed successfully.")
            else:
                print("Initial run failed.")
                fix = input("Do you want to try fixing it? (y/n): ")
                if fix.lower() == "y":
                    handle_failure(task)
                else:
                    print("Exiting.")
        else:
            print("Task aborted.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
