#This is my version two (v2) of expense tracker and I named is FinSight 
from datetime import datetime

# ANSI colour codes for terminal rendering
CYN = "\033[96m"
GRN = "\033[92m"
YEL = "\033[93m"
RST = "\033[0m"
BOLD = "\033[1m"


def ask_int(prompt, low=None, high=None):
    """Prompt for integer input with simple validation and helpful messages."""
    while True:
        s = input(prompt).strip()
        if not s:
            print("  enter a value")
            continue
        try:
            v = int(s)
            if low is not None and v < low:
                print(f"  must be ≥ {low}")
                continue
            if high is not None and v > high:
                print(f"  must be ≤ {high}")
                continue
            return v
        except ValueError:
            print("  integers only")


def ask_float(prompt, low=None, high=None):
    """Prompt for float input with validation. Accepts integers too."""
    while True:
        s = input(prompt).strip()
        if not s:
            print("  enter a value")
            continue
        try:
            v = float(s)
            if low is not None and v < low:
                print(f"  must be ≥ {low}")
                continue
            if high is not None and v > high:
                print(f"  must be ≤ {high}")
                continue
            return v
        except ValueError:
            print("  numbers only")


def pad(text, width):
    """Short helper to align table columns. Truncate with ellipsis if too long."""
    t = str(text)
    if len(t) > width:
        return t[: width - 1] + "…"
    return t.ljust(width)


def human_header():
    """Print the small ANSI-coloured header. Kept minimal to appear human-printed."""
    print(f"{CYN}{BOLD}Energy Analyzer — CLI{RST}  |  simple usage")
    print()


def collect_devices(n):
    """Collect device information from user and compute per-device daily kWh."""
    devices = []
    print("\nEnter device details (example names: Air Conditioner, Fridge, Fan).")
    for i in range(1, n + 1):
        name = input(f"  {i}. Device name: ").strip() or f"Device{i}"
        watts = ask_float("     Watts (W): ", low=1)
        hours = ask_float("     Hours per day: ", low=0, high=24)
        qty = ask_int("     Quantity: ", low=1, high=1000)
        kwh_day = (watts * hours * qty) / 1000.0
        devices.append({"name": name, "watts": watts,
                       "hours": hours, "qty": qty, "kwh_day": kwh_day})
    return devices


def summary_and_report(devices, days, tariff):
    """Compute totals, print summary, and write a plain-text report file."""
    total_kwh_day = sum(d["kwh_day"] for d in devices)
    total_kwh_month = total_kwh_day * days
    est_bill = total_kwh_month * tariff
    top = max(devices, key=lambda d: d["kwh_day"])
    # Table header
    print()
    print(f"{BOLD}Per-Device Daily Usage{RST}")
    h1, h2, h3, h4, h5 = "Device", "Watts", "Hours", "Qty", "kWh/day"
    w1, w2, w3, w4, w5 = 20, 7, 7, 5, 10
    total_width = w1 + w2 + w3 + w4 + w5 + 8
    print("-" * total_width)
    print(pad(h1, w1), "|", pad(h2, w2), "|", pad(
        h3, w3), "|", pad(h4, w4), "|", pad(h5, w5))
    print("-" * total_width)
    for d in devices:
        print(pad(d["name"], w1), "|", pad(str(int(d["watts"])), w2), "|", pad(
            f'{d["hours"]:.1f}', w3), "|", pad(str(d["qty"]), w4), "|", pad(f'{d["kwh_day"]:.3f}', w5))
    print("-" * total_width)
    # Summary (minimal color)
    print()
    print(f"{GRN}{BOLD}Summary{RST}")
    print(f"  Total daily consumption      : {total_kwh_day:.3f} kWh")
    print(
        f"  Billing cycle consumption    : {total_kwh_month:.3f} kWh (days={days})")
    print(f"  Estimated bill @ ₹{tariff:.2f}/kWh : {YEL}₹{est_bill:,.2f}{RST}")
    print(
        f"  Highest daily consumer       : {top['name']} ({top['kwh_day']:.3f} kWh/day)")
    print()
    # Practical tips (simple heuristics)
    print("Tips:")
    if total_kwh_day > 15:
        print("  • Consider staggering heavy loads to reduce peak usage.")
    if top["hours"] > 8 and top["watts"] > 200:
        print(
            f"  • Try reducing {top['name']} hours or enable energy-saver settings.")
    if tariff > 9:
        print("  • Tariff is relatively high—small savings on daily kWh translate to meaningful ₹ reductions.")
    if any(d["watts"] < 80 and d["hours"] > 10 for d in devices):
        print("  • Long-running low-watt devices add up—audit always-on equipment.")

    # Write report
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "Energy Analyzer Report",
        f"Generated: {stamp}",
        "",
        f"Billing days: {days}",
        f"Tariff (₹/kWh): {tariff}",
        "",
        "Per-Device Daily Usage:",
        f"{h1:20} {h2:>7} {h3:>7} {h4:>5} {h5:>10}"
    ]
    for d in devices:
        lines.append(
            f"{d['name']:20} {int(d['watts']):7d} {d['hours']:7.1f} {d['qty']:5d} {d['kwh_day']:10.3f}")
    lines += [
        "",
        f"Total daily kWh: {total_kwh_day:.3f}",
        f"Monthly kWh   : {total_kwh_month:.3f}",
        f"Est. bill (₹) : {est_bill:.2f}",
        f"Top device    : {top['name']} ({top['kwh_day']:.3f} kWh/day)"
    ]
    with open("energy_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\nReport saved to: energy_report.txt")


def main():
    human_header()
    days = ask_int("Billing days (typical 30): ", low=1, high=365)
    tariff = ask_float("Tariff ₹/kWh (e.g., 8): ", low=0)
    n = ask_int("Number of devices: ", low=1, high=100)
    devices = collect_devices(n)
    if not devices:
        print("No devices entered; exiting.")
        return
    summary_and_report(devices, days, tariff)


if __name__ == "__main__":
    main()
