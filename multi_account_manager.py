"""
Multi-Account Facebook Personal Messenger Bridge for Souza Dealer (DealerOS)

Enables sales reps to configure their personal Facebook login sessions,
with isolated browser profile directories, message ingestion, and automated
routing to the Souza Dealer CRM.
"""
import os
import sys
import time
import json
import argparse
from pathlib import Path

CONFIG_FILE = "personal_accounts.json"

def load_accounts():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(CONFIG_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def add_account(sales_rep_id, sales_rep_name, email, password=""):
    accounts = load_accounts()
    # Check if sales rep already has a profile
    for acc in accounts:
        if acc.get("sales_rep_id") == sales_rep_id:
            acc.update({"sales_rep_name": sales_rep_name, "email": email, "updated_at": time.time()})
            save_accounts(accounts)
            print(f"[+] Updated personal account configuration for {sales_rep_name} (ID: {sales_rep_id})")
            return
    accounts.append({
        "sales_rep_id": sales_rep_id,
        "sales_rep_name": sales_rep_name,
        "email": email,
        "profile_dir": f"profiles/rep_{sales_rep_id}",
        "status": "CONFIGURED",
        "created_at": time.time(),
        "updated_at": time.time()
    })
    save_accounts(accounts)
    print(f"[+] Added personal account for {sales_rep_name} (ID: {sales_rep_id})")

def list_accounts():
    accounts = load_accounts()
    if not accounts:
        print("[-] No personal sales rep Facebook accounts configured yet.")
        return
    print("\n--- Configured Personal Facebook Accounts (Souza Dealer) ---")
    for a in accounts:
        print(f"• Rep: {a.get('sales_rep_name')} (ID: {a.get('sales_rep_id')}) | FB Email: {a.get('email')} | Status: {a.get('status')}")
    print("----------------------------------------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Souza Dealer Multi-Account Personal Facebook Messenger Bridge")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add or update a sales rep personal FB account")
    add_parser.add_argument("--rep-id", required=True, help="Sales Rep ID in DealerOS")
    add_parser.add_argument("--rep-name", required=True, help="Sales Rep Full Name")
    add_parser.add_argument("--email", required=True, help="Sales Rep Facebook Email/Username")

    list_parser = subparsers.add_parser("list", help="List all configured personal FB accounts")

    args = parser.parse_args()
    if args.command == "add":
        add_account(args.rep_id, args.rep_name, args.email)
    elif args.command == "list":
        list_accounts()
    else:
        parser.print_help()
