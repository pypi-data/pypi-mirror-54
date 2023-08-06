import string as st
import re

text =["'s gemeenthe", "st paul's cathedral", "washington, d.c."]

for item in text:
    nm = st.capwords(item)
    print(nm)
    nm = re.sub(r"(?:[a-z])(\'S )","'s ", nm)
    nm = re.sub(r"D.c.", "D.C.", nm)
    print (nm)