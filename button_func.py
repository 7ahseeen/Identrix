# Identrix - developed by Girgiti github:7ahseeen

import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


import os 
import datetime

from Bio import pairwise2
from Bio.Align import substitution_matrices

substitution_matrix = substitution_matrices.load('BLOSUM62')  # matrix to load

#   Save output to a file

def saveOut(App):
    # Create Output directory if it doesn't exist
    output_dir = "Output"
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except Exception as e:
        messagebox.showerror("Directory Error", 
                            f"Could not create output directory:\n{str(e)}")
        return

    file_path = os.path.join(output_dir, "resultIdentrix.txt")
    
    # Check if output exists and has content
    if not hasattr(App, 'outBox'):
        messagebox.showwarning("No Results", 
                              "No analysis results available to save")
        return
    
    content = App.outBox.get("1.0", "end-1c").strip()
    if not content:
        messagebox.showwarning("Empty Results", 
                              "The results box is empty")
        return
    
    # Save to file
    try:
        with open(file_path, 'w') as file:
            # Write header
            file.write("Identrix - Sequence Analysis Results\n")
            file.write("=" * 50 + "\n\n")
            
            # Write content
            file.write(content)
            
            # Write footer with timestamp
            file.write("\n\n" + "=" * 50)
            file.write("\nGenerated on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Show success message
        messagebox.showinfo("Success", 
                           f"Results saved to:\n{file_path}")
    
    except Exception as e:
        messagebox.showerror("Save Error", 
                           f"Could not save file:\n{str(e)}")
        

#       Show / Hide Query InputBox
def addQuery(App, selectedInp, queTypeName, queInput, seqInput):
    if(selectedInp.get() == "Proteins"):
        queTypeName.pack( after = seqInput, anchor = "w", padx = 10, pady = (10, 0))
        queInput.pack(after = queTypeName, padx = 10, pady = (4, 0), anchor = "center")
    else:
        queTypeName.pack_forget()
        queInput.pack_forget()

def algo(sequence, query, opt):
    # Parse FASTA sequences
    sequences = []
    headers = []
    current_seq = ""
    
    for line in sequence.split('\n'):
        if line.startswith('>'):
            if current_seq:
                sequences.append(current_seq)
                current_seq = ""
            headers.append(line[1:].strip())
        else:
            current_seq += line.strip().upper()
    
    if current_seq:
        sequences.append(current_seq)
    
    if len(sequences) < 2:
        return "Error: At least two sequences required for comparison"
    
    # Define valid characters for inpSeq
    valid_chars = {
        'DNA': set('ATCGN-'),
        'RNA': set('AUCGN-'),
        'Proteins': set('ACDEFGHIKLMNPQRSTVWY-')
    }.get(opt, set())
    
    # Validate sequences
    for seq in sequences:
        if not all(c.upper() in valid_chars for c in seq):
            invalid_chars = set(c.upper() for c in seq if c.upper() not in valid_chars)
            return f"Error: Sequence contains invalid characters for {opt}: {', '.join(invalid_chars)}"
    
    # Protein Sim groups
    sim_groups = {}
    if opt == "Proteins" and query:
        valid_amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
        for group in query.split(','):
            group = group.strip().upper()
            if not group:
                continue  # Skip empty groups
            # Only include valid amino acids (no hyphens in similarity groups)
            valid_chars = [aa for aa in group if aa in valid_amino_acids]
            if not valid_chars:
                continue
            for aa in valid_chars:
                sim_groups[aa] = valid_chars  # Similar residues list
    
    # pairwise alignments
    results = []
    n = len(sequences)
    
    for i in range(n):
        for j in range(i+1, n):
            try:
                if opt == "Proteins":
                    matrix = substitution_matrices.load("BLOSUM62")
                    alignments = pairwise2.align.globalds(
                        sequences[i].replace('-', ''),  # Remove gaps before alignment
                        sequences[j].replace('-', ''), 
                        matrix,
                        -10,  # gap open penalty
                        -0.5  # gap extension penalty
                    )
                else:
                    alignments = pairwise2.align.globalms(
                        sequences[i].replace('-', ''),  # Remove gaps before alignment
                        sequences[j].replace('-', ''), 
                        2,    # match score
                        -1,   # mismatch penalty
                        -10,  # gap open penalty
                        -0.5  # gap extension penalty
                    )
            except Exception as e:
                return f"Alignment error: {str(e)}"
            
            # best alignment
            best_alignment = alignments[0]
            aligned1, aligned2, score, begin, end = best_alignment
            
            # Calc ident sim
            ident_count = 0
            sim_count = 0
            total = len(aligned1)
            total_non_gap = 0  # Total positions excluding gaps
            
            for k in range(total):
                a = aligned1[k]
                b = aligned2[k]
                
                # Skip if both are gaps
                if a == '-' and b == '-':
                    continue
                    
                total_non_gap += 1
                
                if a == b and a != '-':
                    ident_count += 1
                    sim_count += 1
                elif opt == "Proteins" and a != '-' and b != '-':
                    if a in sim_groups and b in sim_groups and b in sim_groups[a]:
                        sim_count += 1
            
            # Calculate percentages based on non-gap positions
            ident_percent = (ident_count / total_non_gap) * 100 if total_non_gap > 0 else 0
            sim_percent = (sim_count / total_non_gap) * 100 if total_non_gap > 0 else 0
            
            # Format results
            header_i = headers[i] if i < len(headers) else f"Sequence {i+1}"
            header_j = headers[j] if j < len(headers) else f"Sequence {j+1}"
            
            result = (
                f"\nComparison: {header_i} vs {header_j}\n"
                f"Alignment Length: {total} (Non-gap positions: {total_non_gap})\n"
                f"Alignment Score: {score:.2f}\n"
                f"Identity: {ident_count} residues ({ident_percent:.2f}%)\n"
            )
            
            if opt == "Proteins":
                result += f"Similarity: {sim_count} residues ({sim_percent:.2f}%)\n"
            
            # Add aligned sequences for visualization
            result += "\nAligned Sequences:\n"
            result += f"Seq1: {aligned1}\n"
            result += f"Seq2: {aligned2}\n"
            result += "-" * 50  # Separator
            
            results.append(result)
    
    return "\n" + "\n".join(results) + "\n"

#   Output Area
def analyzeBtn(App):
    #   get the sequence
    seqData = App.seqInput.get("1.0", "end-1c").strip()

    #   input blank or invalid
    if not seqData:
        # Hide output - view once
        if hasattr(App, 'errLabel') and App.errLabel.winfo_ismapped():
            App.errLabel.pack_forget()
        if hasattr(App, 'errBox') and App.errBox.winfo_ismapped():
            App.errBox.pack_forget()

        if not App.errLabel.winfo_ismapped():
            App.errLabel.pack(anchor = "w", padx=10, pady=(4,0))
            App.errBox.pack(anchor = "w", padx=10, pady=5)

    #   input valid
    else:
        if hasattr(App, 'errBox') and hasattr(App, 'errLabel'):
             App.errLabel.pack_forget()
             App.errBox.pack_forget()

        # CREATE OUTPUT WIDGETS IF THEY DON'T EXIST
        if not hasattr(App, 'outLabel'):
            App.outLabel = tk.Label(App, text="Result :",
                                    fg="#5c352d", bg='#d0aca1', font=("Courier", 12, "bold"))                           # Identrix - developed by Girgiti github:7ahseeen
        
        if not hasattr(App, 'outBox'):
            App.outBox = ctk.CTkTextbox(
                master=App,
                height=130,               
                width=700,                 
                font=("Courier", 12),
                corner_radius=10,  
                fg_color="#f0e6e0",   
                text_color="#000", 
                wrap="word"
            )
            # Initially disabled
            App.outBox.configure(state="disabled")
        
        # Show output area
        App.outLabel.pack(anchor="w", padx=10, pady=4)
        App.outBox.pack(anchor="w", padx=10, pady=4)

        #   write out result
        queryData = ""
        seqType = App.selectedInp.get()

        if (seqType == "Proteins"):
            queryData = App.queInput.get("1.0", "end-1c").strip()
        
        resData = algo(seqData, queryData, seqType)
        
        # PRINT TO CONSOLE FOR DEBUGGING
        print("\n" + "="*50)
        print("ALGORITHM RESULT:")
        print(resData)
        print("="*50 + "\n")

        # UPDATE THE OUTPUT BOX
        App.outBox.configure(state="normal")
        App.outBox.delete("1.0", "end")
        App.outBox.insert("1.0", resData)
        App.outBox.configure(state="disabled")

#   clear btn func
def clearBtn(App):

    #   remove input texts
    App.queInput.delete("1.0", "end")
    App.seqInput.delete("1.0", "end")

    #   remove results field
    if hasattr(App, 'outLabel') and App.outLabel.winfo_ismapped():
        App.outLabel.pack_forget()
    if hasattr(App, 'outBox') and App.outBox.winfo_ismapped():
        App.outBox.pack_forget()

    #   remove err field
    if hasattr(App, 'errLabel') and App.errLabel.winfo_ismapped():
        App.errLabel.pack_forget()
    if hasattr(App, 'errBox') and App.errBox.winfo_ismapped():
        App.errBox.pack_forget()

#   upload file
def upFile(App):
    fileAddr = filedialog.askopenfile(title = "Select File to Analyze : ", mode = 'r',
                                      filetypes = [("FASTA files", "*.fasta *.fa *.txt"), ("All files", "*.*")])
    
    if fileAddr:
        print("Selected file : ", fileAddr)

        inpTxt = fileAddr.read()
        App.seqInput.delete("1.0", "end")
        App.seqInput.insert("1.0", inpTxt)




