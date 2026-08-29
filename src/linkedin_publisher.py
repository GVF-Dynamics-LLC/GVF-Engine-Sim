import json
import os
import argparse
import sys

def prompt_review(platform, content):
    """Interactive review prompt for LinkedIn content."""
    print("\n" + "="*60)
    print(f" [HUMAN REVIEW GATE] Draft Content for: {platform.upper()}")
    print("="*60)
    print(f"{content}")
    print("="*60)

    while True:
        choice = input(f"Approve posting to {platform}? [y = Approve, n = Skip/Reject, e = Edit Text]: ").strip().lower()
        if choice in ["y", "yes"]:
            return "approved", content
        elif choice in ["n", "no"]:
            return "rejected", content
        elif choice == "e":
            print("\nEnter replacement text below (single line):")
            new_text = input("> ").strip()
            return "approved", new_text
        else:
            print("Invalid selection. Please enter y, n, or e.")

def execute_linkedin_post(content):
    """Simulates live LinkedIn Organization update."""
    print("\n[LINKEDIN PUBLISHER API]")
    print(f"-> Publishing Organization Update to GVF Dynamics Company Page:\n\n{content}\n")
    print("Status: [SUCCESS] Posted to LinkedIn Company Page.\n")

def main():
    parser = argparse.ArgumentParser(description="GVF LinkedIn Publisher with Human Gate")
    parser.add_argument("--payload", type=str, default="data/latest_agent_output.json", help="Path to payload file")
    args = parser.parse_args()

    if not os.path.exists(args.payload):
        print(f"Error: Payload file not found at {args.payload}")
        return

    with open(args.payload, "r") as f:
        payload = json.load(f)

    # --- LinkedIn Review & Execution ---
    li_draft = payload.get("linkedin_company_update", "")
    if li_draft:
        status, final_li = prompt_review("LinkedIn Company Page", li_draft)
        if status == "approved":
            execute_linkedin_post(final_li)
        else:
            print("\n[LINKEDIN] Skipped by user.")

if __name__ == "__main__":
    main()
