import pandas as pd

class Analyzer:
    def __init__(self, students):
        self.students = students
        self.df = pd.DataFrame([{
            'ID': s.student_id,
            'Name': s.name,
            'Attendance': s.attendance,
            'Average_Grade': s.average_grade,
            'Attendance_Level': s.attendance_level
        } for s in students])

    def compute_statistics(self):
        # Helper function to convert numpy types to native Python types
        def convert_numpy(value):
            if pd.isna(value):  # Handle NaN/None
                return None
            try:
                return value.item()  # Converts numpy types to native Python types
            except:
                return float(value) if isinstance(value, (float, int)) else value

        stats = {
            'mean_attendance': round(float(self.df['Attendance'].mean()), 2),
            'mean_grade': round(float(self.df['Average_Grade'].mean()), 2),
            'max_attendance': float(self.df['Attendance'].max()),
            'min_attendance': float(self.df['Attendance'].min()),
            'max_grade': float(self.df['Average_Grade'].max()),
            'min_grade': float(self.df['Average_Grade'].min()),
            'correlation': round(float(self.df['Attendance'].corr(self.df['Average_Grade'])), 3)
        }
        
        # Convert any remaining numpy types
        return {k: convert_numpy(v) for k, v in stats.items()}
