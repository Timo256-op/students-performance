import pandas as pd
from student import Student

class DatasetManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.students = []

    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)
            required_columns = ['Student_ID', 'Name', 'Attendance', 'Average_Grade']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")
            
            df = df.drop_duplicates()
            # Only fill numeric columns with their mean
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_cols:
                df[col] = df[col].fillna(df[col].mean())
            
            for _, row in df.iterrows():
                student = Student(row['Student_ID'], row['Name'], row['Attendance'], row['Average_Grade'])
                self.students.append(student)
            return self.students
        except pd.errors.EmptyDataError:
            raise ValueError("The uploaded CSV file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")

