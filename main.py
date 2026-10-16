import subprocess
import sys


def run_script(script_path, step_name):
    print("\n" + "=" * 60)
    print(step_name)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_path],
        check=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {step_name} failed.")
        sys.exit(1)

    print(f"\nSUCCESS: {step_name} completed.")


def main():

    print("\n")
    print("=" * 60)
    print("NOVARETAIL CAPSTONE - AUTOMATED QBR GENERATION")
    print("=" * 60)

    # STEP 1 - Business data analysis
    run_script(
        "tools/data_analysis.py",
        "STEP 1: DATA ANALYSIS"
    )

    # STEP 2 - Charts
    run_script(
        "tools/chart_generator.py",
        "STEP 2: CHART GENERATION"
    )

    # STEP 3 - Icon mapping
    run_script(
        "tools/icon_mapper.py",
        "STEP 3: ICON SELECTION"
    )

    # STEP 4 - ADK / Gemini content
    run_script(
        "tools/content_agent.py",
        "STEP 4: AI CONTENT GENERATION"
    )

    # STEP 5 - Final PowerPoint
    run_script(
        "tools/ppt_generator.py",
        "STEP 5: POWERPOINT GENERATION"
    )

    print("\n")
    print("=" * 60)
    print("NOVARETAIL CAPSTONE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(
        "\nFinal presentation:"
        "\noutput/NovaRetail_QBR_Final.pptx"
    )


if __name__ == "__main__":
    main()
    