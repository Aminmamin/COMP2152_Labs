# ============================================================
#  WEEK 13 LAB — Q2: ASCII DASHBOARD
#  COMP2152 — Muhammad-Amin Farhan Ali
# ============================================================

import csv


SAMPLE_FILE = "scan_results.csv"


def load_findings(filename):
    with open(filename, "r") as f:
        return list(csv.DictReader(f))


# draw simple bar chart
def bar_chart(data, title, max_width=30):
    print(title)

    if not data:
        return

    max_val = max(count for _, count in data)

    for label, count in data:
        if max_val == 0:
            bar_len = 0
        else:
            bar_len = int((count / max_val) * max_width)

        print(f"  {label:<15} {'█' * bar_len} {count}")


# count severity
def severity_summary(findings):
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for f in findings:
        sev = f["severity"]
        counts[sev] += 1

    return [("HIGH", counts["HIGH"]),
            ("MEDIUM", counts["MEDIUM"]),
            ("LOW", counts["LOW"])]


# count by date
def timeline(findings):
    counts = {}

    for f in findings:
        d = f["date"]
        if d in counts:
            counts[d] += 1
        else:
            counts[d] = 1

    return sorted(counts.items())


# --- Main ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: ASCII DASHBOARD")
    print("=" * 60)

    findings = load_findings(SAMPLE_FILE)

    print()
    sev = severity_summary(findings)
    bar_chart(sev, "SEVERITY BREAKDOWN")

    print()
    dates = timeline(findings)
    bar_chart(dates, "FINDINGS BY DATE")

    print()
    type_counts = {}
    for f in findings:
        t = f["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    type_data = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    bar_chart(type_data, "VULNERABILITY TYPES")

    print("\n" + "=" * 60)