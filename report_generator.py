from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, stats):
        self.stats = stats

    def generate(self):
        os.makedirs("reports", exist_ok=True)
        report_path = "reports/summary_report.txt"
        with open(report_path, "w") as f:
            f.write("STUDENT ATTENDANCE AND PERFORMANCE REPORT\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Summary Statistics:\n")
            for k, v in self.stats.items():
                f.write(f"  {k}: {v:.2f}\n")

            f.write("\nRecommendations:\n")
            f.write("- Encourage students with low attendance (<60%) to participate more.\n")
            f.write("- Reward students with consistent high attendance.\n")
            f.write("- Investigate causes of chronic absenteeism.\n")
        return report_path
