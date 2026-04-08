import sys
from summarizer import abstractive_summary

text = "1 Introduction: Registration refers to the recording of the contents of a document with a Registering Officer appointed by the Government. The main purpose of registration is to ensure information about all deals are recorded and maintained apart from giving the document its authenticity. The process of registering a document is done under the provisions of the Registration Act, 1908. The main objects of the law of registration are – (a) to provide a conclusive proof of genuineness of documents; (b) to afford publicity of transaction in respect of properties; (c) to prevent fraud; (d) to afford facility for ascertaining whether a property has already been dealt with; and (e) to afford security of the title deeds and facility of proving titles in case the original deeds are lost or destroyed. Documents generally required for registration (a) Duly stamped, signed and executed document."

print("Testing abstractive summary...")
try:
    res = abstractive_summary(text, max_length=150, min_length=40)
    print("RESULT:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
