import pdfplumber
import csv

struct_data = {}


class Extract():
    

    def __init__(self, report) -> None:
        self.report = report

    # def extract_table(self):
    #     pdf_file = fitz.open(self.report)
    #     with open("annual_report2.csv", "a", newline="", encoding="utf-8") as table_doc:
    #         writer = csv.writer(table_doc)
    #         writer.writerow(["Tabelleninhalt"])

    #         for page_number in range(len(pdf_file)):
    #             #duchlaufen jeder Seite in dem Pdf
    #             page = pdf_file[page_number]
    #             #Tabellen in der PDF finden 
    #             tables = page.find_tables()
    #             #Falls Tabelle geufnden wurde, werden werte extrahiert und an Dict & CSV übergeben
    #             if len(tables.tables) > 0:
    #                 struct_data["Tables"] = []    
    #                 for table in tables.tables:
    #                     for content in table.extract():
    #                     # for text in tables[0].extract():
    #                         struct_data["Tables"].append(content)
    #                     #     writer.writerow([table.header.names, table.col_count, table.row_count])
    #                     #     for line in tables[0].extract():
    #                     #         writer.writerow([line])   

    def get_text(self) : 
        pdf_file = pdfplumber.open(self.report)
        #pdf_file = PdfReader(self.report)
        if self.report != struct_data:
            struct_data["Report"] = [self.report] * len(pdf_file.pages)
            # Öffne die CSV-Datei zum Schreiben
            with open("annual_report.csv", "a", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
            #     # Schreibe die Überschriften in die CSV-Datei
            #     csv_writer.writerow(["Seite", "Text"])

                # Durchlaufe jede Seite der PDF
                struct_data["Page"] = []
                struct_data["Text"] = []
                for page_num in range(len(pdf_file.pages)):
                    page = pdf_file.pages[page_num]
                        # Extrahiere den Text von der aktuellen Seite
                    text = page.extract_text()
                        # Schreibe die Seite und den Text in die CSV-Datei
                    csv_writer.writerow([text])
                    struct_data["Page"].append(page_num)
                    struct_data["Text"].append(text)
        return struct_data

    