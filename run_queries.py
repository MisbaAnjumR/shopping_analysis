import sqlite3
import pandas as pd
from fpdf import FPDF

class ReportPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Customer Behavior Analysis Report', border=False, align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def main():
    print("Connecting to the database...")
    conn = sqlite3.connect('customer_behavior.db')

    print("Reading queries.sql...\n")
    with open('queries.sql', 'r') as file:
        sql_content = file.read()
        
    # Standard splitting, queries separated by ;
    queries = [q.strip() for q in sql_content.split(';') if q.strip()]
    
    print(f"Found {len(queries)} queries. Executing them and generating PDF...\n")

    # Initialize PDF
    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, query in enumerate(queries):
        # Extract the comment line if it exists to display the question
        lines = query.strip().split('\n')
        question_text = lines[0] if lines[0].startswith('--') else f"Query {i+1}"
        
        print(f"{'='*60}")
        print(f"Q{i+1}: {question_text}")
        print(f"{'-'*60}")
        
        # Add to PDF
        pdf.set_font("helvetica", "B", 11)
        pdf.multi_cell(0, 8, f"Q{i+1}: {question_text.lstrip('-').strip()}")
        pdf.ln(2)
        
        try:
            df = pd.read_sql(query, conn)
            # Print to terminal
            print(df.to_string(index=False))
            
            # Add to PDF
            pdf.set_font("helvetica", size=9)
            with pdf.table(text_align="CENTER") as table:
                header_row = table.row()
                for col_name in df.columns:
                    pdf.set_font("helvetica", "B", 9)
                    header_row.cell(str(col_name))
                pdf.set_font("helvetica", size=9)
                for _, data_row in df.iterrows():
                    row = table.row()
                    for item in data_row:
                        val = f"{item:.2f}" if isinstance(item, float) else str(item)
                        row.cell(val)
        except Exception as e:
            print(f"Error executing query: {e}")
            pdf.set_font("helvetica", "I", 10)
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, f"Error executing query: {e}")
            pdf.set_text_color(0, 0, 0)
            
        print("\n")
        pdf.ln(8)

    conn.close()
    print("All queries executed successfully!")
    
    # Output PDF
    output_filename = "Analysis_Report.pdf"
    pdf.output(output_filename)
    print(f"PDF successfully generated: {output_filename}")

if __name__ == "__main__":
    main()
