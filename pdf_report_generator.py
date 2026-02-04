from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self, stats, scatter_path="reports/scatter_plot.png", bar_path="reports/bar_chart.png"):
        self.stats = stats
        self.scatter_path = scatter_path
        self.bar_path = bar_path
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        os.makedirs("reports", exist_ok=True)
        
        # Compact custom styles for 2-page layout
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=10,
            leading=16
        ))
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            leading=14
        ))
        self.styles.add(ParagraphStyle(
            name='CompactNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            spaceBefore=2,
            spaceAfter=2
        ))
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=colors.whitesmoke
        ))
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11
        ))

    def _create_stats_table(self):
        """Create a compact formatted table of statistics"""
        data = [['Metric', 'Value']]
        metrics_map = {
            'mean_attendance': 'Mean Attendance (%)',
            'mean_grade': 'Mean Grade',
            'max_attendance': 'Highest Attendance (%)',
            'min_attendance': 'Lowest Attendance (%)',
            'max_grade': 'Highest Grade',
            'min_grade': 'Lowest Grade',
            'correlation': 'Attendance-Grade Correlation'
        }
        
        for key, value in self.stats.items():
            formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            if key in metrics_map:
                data.append([metrics_map[key], formatted_value])
        
        # Create compact table
        table = Table(data, colWidths=[250, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
        ]))
        return table

    def _get_correlation_insight(self):
        """Generate insight text based on correlation value"""
        corr = self.stats.get('correlation', 0)
        if abs(corr) > 0.7:
            strength = "strong"
        elif abs(corr) > 0.4:
            strength = "moderate"
        else:
            strength = "weak"
            
        direction = "positive" if corr > 0 else "negative"
        return f"There is a {strength} {direction} correlation ({corr:.3f}) between attendance and grades, " \
               f"suggesting that {'higher attendance tends to be associated with better grades' if corr > 0 else 'the relationship between attendance and grades needs further investigation'}."

    def generate_pdf(self):
        """Generate a compact two-page PDF report"""
        pdf_path = "reports/summary_report.pdf"
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=36,  # Reduced margins
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        # Build the document parts
        story = []
        
        # Title and date in one line
        title_date = Table([
            [Paragraph("Student Attendance and Performance Report", self.styles['CustomTitle']),
             Paragraph(datetime.now().strftime('%Y-%m-%d %H:%M'), self.styles['CompactNormal'])]
        ], colWidths=[400, 120])
        title_date.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(title_date)
        story.append(Spacer(1, 10))
        
        # 1. Statistics Section
        story.append(Paragraph("1. Summary Statistics", self.styles['SectionTitle']))
        story.append(self._create_stats_table())
        story.append(Spacer(1, 20))
        
        # Correlation Analysis in compact form
        story.append(Paragraph("Key Insight:", self.styles['SectionTitle']))
        story.append(Paragraph(self._get_correlation_insight(), self.styles['CompactNormal']))
        story.append(Spacer(1, 10))
        
        # 2. Visualizations Section (start on page 2)
        story.append(PageBreak())
        
        # Create visualization section header
        viz_header = ParagraphStyle(
            'VizHeader',
            parent=self.styles['SectionTitle'],
            spaceBefore=10,
            spaceAfter=10,
            fontSize=12,
            textColor=colors.HexColor('#2C3E50')
        )
        story.append(Paragraph("2. Data Visualizations", viz_header))
        
        # Calculate available width for compact layout
        available_width = doc.width * 0.98  # Use more width
        
        if os.path.exists(self.scatter_path):
            # Compact scatter plot section
            scatter_style = ParagraphStyle(
                'ScatterHeader',
                parent=self.styles['Heading3'],
                spaceBefore=6,
                spaceAfter=6,
                fontSize=10,
                textColor=colors.HexColor('#34495E')
            )
            story.append(Paragraph("Attendance vs Performance Scatter Plot:", scatter_style))
            
            # Add the image with compact sizing
            img = Image(self.scatter_path)
            # Scale image to fit width while maintaining aspect ratio
            aspect = img.imageHeight / float(img.imageWidth)
            img.drawWidth = available_width
            img.drawHeight = available_width * 0.5  # Make it shorter
            story.append(img)
            story.append(Spacer(1, 6))
            
            # Compact description style
            desc_style = ParagraphStyle(
                'PlotDescription',
                parent=self.styles['CompactNormal'],
                spaceBefore=4,
                spaceAfter=10,
                fontSize=9,
                leading=11,
                alignment=4  # Justified alignment
            )
            
            scatter_desc = Paragraph(
                "This scatter plot shows the relationship between student attendance and their academic performance. "
                "Each point represents a student, with colors indicating their attendance level category. "
                "The pattern suggests a positive correlation between attendance and grades.",
                desc_style
            )
            story.append(scatter_desc)
            story.append(Spacer(1, 20))
        
        if os.path.exists(self.bar_path):
            story.append(PageBreak())  # Start bar chart on new page
            
            # Add bar chart section with consistent styling
            bar_style = ParagraphStyle(
                'BarHeader',
                parent=self.styles['Heading3'],
                spaceBefore=60,  # Match the top spacing of the previous page
                spaceAfter=20,
                fontSize=12,
                textColor=colors.HexColor('#34495E'),
                leading=14
            )
            story.append(Paragraph("Average Grade by Attendance Level:", bar_style))
            
            # Add the bar chart image
            img = Image(self.bar_path)
            aspect = img.imageHeight / float(img.imageWidth)
            img.drawWidth = available_width * 0.9
            img.drawHeight = (available_width * 0.9) * aspect
            story.append(img)
            story.append(Spacer(1, 30))
            
            # Add plot description
            bar_desc = Paragraph(
                "This bar chart compares the average grades across different attendance level categories. "
                "It helps visualize how academic performance varies with attendance levels, "
                "showing the aggregate impact of attendance on grades.",
                self.styles['Normal']
            )
            story.append(bar_desc)
        
        # 3. Recommendations Section
        story.append(Paragraph("3. Recommendations", self.styles['SectionTitle']))
        recommendations = [
            "Based on the analysis, we recommend the following actions:",
            "• Monitor and Support: Identify students with attendance below 80% for early intervention.",
            "• Recognition Program: Implement rewards for students maintaining high attendance rates.",
            "• Attendance Tracking: Set up a system to track attendance patterns and trigger alerts.",
            "• Student Engagement: Develop strategies to make classes more engaging and interactive.",
            "• Communication: Regular updates to stakeholders about attendance-performance correlation.",
            "• Resource Access: Ensure students have necessary resources for consistent attendance.",
        ]
        for rec in recommendations:
            story.append(Paragraph(rec, self.styles['Normal']))
            story.append(Spacer(1, 10))
            
        # Build PDF
        doc.build(story)
        return pdf_path
