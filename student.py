class Student:
    def __init__(self, student_id, name, attendance, average_grade):
        self.student_id = student_id
        self.name = name
        self.attendance = attendance
        self.average_grade = average_grade
        self.attendance_level = self.categorize_attendance()

    def categorize_attendance(self):
        if self.attendance >= 80:
            return 'High'
        elif self.attendance >= 60:
            return 'Medium'
        else:
            return 'Low'

    def __repr__(self):
        return f"{self.name} ({self.attendance_level}) - Grade: {self.average_grade}"
