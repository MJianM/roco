import subprocess
import os
from glob import glob
import json

def test_run_dialog(task: str, num_runs: int, output_dir: str):
    print(f"Testing Task: {task}")
    result = subprocess.run(['python', 'run_dialog.py', '--task', task, '--run_name', task, 
                             '--data_dir', output_dir,
                             '--start_id', str(-1),
                             '--num_runs', str(num_runs),
                             '--skip_display',
                             '--tsteps', str(5)], 
                            capture_output=True, text=True)
    
    success_cnt = 0
    total_cnt = 0
    total_steps = 0

    all_runs = glob(os.path.join(output_dir, task, 'run_*'))
    for i, run in enumerate(all_runs):

        all_jsons = glob(os.path.join(run, "*.json"))
        if len(all_jsons) == 0:
            print(f"Run {i} has no json files")
            continue
        json_dir = all_jsons[0]
        with open(json_dir, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            success = json_data['success']
            steps = json_data['step']
            if success:
                success_cnt += 1
                total_steps += steps
        
        total_cnt += 1

    if total_cnt < num_runs:
        print(f"Task {task} has less than {num_runs} runs")
        # success_cnt = 0

    print("-" * 40)
    print(f"Task: {task}")
    print(f"Success Rate: {success_cnt}/{total_cnt}")
    if success_cnt > 0:
        print(f"Average Steps: {total_steps/success_cnt}")
    else:
        print("Average Steps: N/A")
    print(f"Error: {result.stderr}")
    print(f"Return Code: {result.returncode}")
    print("-" * 40)

if __name__ == "__main__":

    # tasks = ["sort", "cabinet", "rope", "sweep", "sandwich", "pack"]  

    test_run_dialog("sort", 1, "output")
    test_run_dialog("cabinet", 1, "output")
    test_run_dialog("rope", 1, "output")
    test_run_dialog("sweep", 1, "output")
    test_run_dialog("sandwich", 1, "output")
    test_run_dialog("pack", 1, "output")