import seaborn as sns
import matplotlib.pyplot as plt
import os

class Visualizer:
    def __init__(self, df):
        self.df = df
        os.makedirs("reports", exist_ok=True)

    def scatter_plot(self):
        plt.figure(figsize=(10, 6))
        # Create scatter plot with larger points and better spacing
        scatter = sns.scatterplot(
            data=self.df,
            x='Attendance',
            y='Average_Grade',
            hue='Attendance_Level',
            s=100,
            alpha=0.7
        )
        
        # Improve plot formatting
        plt.title("Attendance vs Academic Performance", pad=20, fontsize=14)
        plt.xlabel("Attendance (%)", labelpad=10)
        plt.ylabel("Average Grade (%)", labelpad=10)
        
        # Add gridlines and adjust their style
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Adjust layout to prevent cutoff
        plt.tight_layout()
        
        # Adjust legend position and format
        plt.legend(title="Attendance Level", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Save with high DPI and larger size
        plt.savefig("reports/scatter_plot.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def bar_chart(self):
        plt.figure(figsize=(10, 6))
        
        # Calculate average grades
        avg_grades = self.df.groupby('Attendance_Level')['Average_Grade'].mean()
        
        # Create bar plot with better formatting
        bar = sns.barplot(
            x=avg_grades.index,
            y=avg_grades.values,
            palette='deep'
        )
        
        # Add value labels on top of bars
        for i, v in enumerate(avg_grades.values):
            bar.text(i, v, f'{v:.1f}%', ha='center', va='bottom')
        
        # Improve plot formatting
        plt.title("Average Grade by Attendance Level", pad=20, fontsize=14)
        plt.xlabel("Attendance Level", labelpad=10)
        plt.ylabel("Average Grade (%)", labelpad=10)
        
        # Add gridlines
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Ensure y-axis starts at 0 and has reasonable margin at top
        max_grade = avg_grades.max()
        plt.ylim(0, max_grade * 1.15)  # Add 15% margin at top
        
        # Adjust layout
        plt.tight_layout()
        
        # Save with high DPI
        plt.savefig("reports/bar_chart.png", dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close()
