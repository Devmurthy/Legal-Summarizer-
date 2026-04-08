
import re

LEGAL_MAP = {
    # 1. CRIMINAL LAW
    r"IPC|Indian Penal Code|Section \d+ of IPC|murder|theft|assault|cheating|fraud|kidnapping|rape|homicide|extortion": [
        {"act": "Indian Penal Code (IPC), 1860", "suggestion": "This document involves potential criminal activities covered by the IPC. Consult sections relevant to the specific offense (e.g., Sec 302 for murder, Sec 378 for theft) for procedural details."},
    ],
    r"CrPC|Code of Criminal Procedure|bail|arrest|warrant|investigation|FIR|charge sheet|remand|Section 438|Section 439": [
        {"act": "Code of Criminal Procedure (CrPC), 1973", "suggestion": "Since this document pertains to criminal procedural matters like arrest, FIR, or bail (Anticipatory/Regular), refer to CrPC for legal protocols and defense strategies."},
    ],
    r"Evidence Act|testimony|witness|confession|relevancy|Section 32|Section 65B|electronic evidence": [
        {"act": "Indian Evidence Act, 1872", "suggestion": "This document discusses evidence admissibility or witness testimony. Refer to the Evidence Act, especially Section 65B for electronic records if applicable."},
    ],

    # 2. CIVIL & CONSTITUTIONAL LAW
    r"Constitution|Article \d+|Fundamental Rights|Writ Petition|Mandamus|Habeas Corpus|Certiorari|Quo Warranto|PIL|Public Interest Litigation": [
        {"act": "The Constitution of India, 1950", "suggestion": "This case involves constitutional matters or writ petitions. Refer to Articles 32 (Supreme Court) or 226 (High Court) for enforcement of fundamental rights."},
    ],
    r"CPC|Code of Civil Procedure|civil suit|injunction|property|written statement|summons|decree|execution|Section 96|Order \d+": [
        {"act": "Code of Civil Procedure (CPC), 1908", "suggestion": "For civil disputes related to property, suits, or injunctions, refer to CPC for filing procedures, written statements, and execution of decrees."},
    ],

    # 3. FAMILY LAW
    r"Marriage|Divorce|Hindu Marriage Act|Muslim Law|Special Marriage Act|alimony|custody|restitution of conjugal rights|Section 13|Section 9": [
        {"act": "Hindu Marriage Act, 1955 / Muslim Personal Law", "suggestion": "This document relates to matrimonial disputes. Refer to the Hindu Marriage Act for divorce/custody or relevant Personal Laws for specific community practices."},
    ],
    r"Domestic Violence|DV Act|husband|wife|marriage|maintenance|Section 125|cruelty|Section 498A": [
        {"act": "Protection of Women from Domestic Violence Act, 2005", "suggestion": "Cases involving domestic disputes or cruelty should be analyzed under the DV Act and Section 498A of IPC for criminal liability."},
    ],

    # 4. COMMERCIAL & CONTRACT LAW
    r"Contract Act|agreement|breach of contract|consideration|indemnity|guarantee|agency|Section 73|Section 74": [
        {"act": "Indian Contract Act, 1872", "suggestion": "This document involves an agreement or a breach of contract. Refer to the Contract Act for rules on damages, performance, and validity of the agreement."},
    ],
    r"Negotiable Instruments|NI Act|Cheque|Section 138|dishonour of cheque|drawer|payee": [
        {"act": "Negotiable Instruments (NI) Act, 1881", "suggestion": "For cheque bounce cases, Section 138 of the NI Act is highly relevant for legal notice and mandatory filing procedures."},
    ],
    r"Companies Act|director|shareholder|incorporation|winding up|NCLT|corporate fraud|dividend": [
        {"act": "Companies Act, 2013", "suggestion": "This document relates to corporate governance or company disputes. Consult the Companies Act and NCLT rules for compliance and litigation."},
    ],

    # 5. SPECIALIZED LAWS
    r"Consumer Protection|Consumer Forum|deficiency in service|unfair trade practice|COPRA|district commission": [
        {"act": "Consumer Protection Act, 2019", "suggestion": "For disputes related to defective goods or deficiency in services, refer to the Consumer Protection Act for filing complaints in consumer forums."},
    ],
    r"Income Tax|Taxation|GST|Customs|Excise|Assessment|CBDT|Indirect Tax": [
        {"act": "Income Tax Act, 1961 / GST Act, 2017", "suggestion": "This document relates to taxation. Consult the relevant Finance Acts, GST schedules, and CBDT circulars for compliance and assessment rules."},
    ],
    r"Cyber|IT Act|hacking|online fraud|data breach|Section 66|identity theft|phishing": [
        {"act": "Information Technology (IT) Act, 2000", "suggestion": "Since this involves cyber-related activities, refer to the IT Act for sections on hacking (66), data protection, and digital evidence protocols."},
    ],
    r"Environment|Pollution|Forest|Wildlife|Water Act|Air Act|NGT|National Green Tribunal": [
        {"act": "Environment Protection Act, 1986", "suggestion": "For environmental compliance or NGT matters, refer to the EP Act and specific Air/Water Acts for penalties and regulatory guidelines."},
    ],
    r"Labour|Employee|Workman|Industrial Disputes|Minimum Wages|Gratuity|EPF|Trade Union": [
        {"act": "Industrial Disputes Act, 1947 / Code on Wages", "suggestion": "This document pertains to employment or industrial relations. Consult the Industrial Disputes Act for layoffs/retrenchment and the Code on Wages for payment rules."},
    ],
    r"Intellectual Property|IPR|Copyright|Trademark|Patent|Infringement|Design Act": [
        {"act": "IPR Laws (Copyright Act 1957 / Trademarks Act 1999)", "suggestion": "For matters related to artistic work, brand names, or inventions, refer to the respective Copyright, Trademark, or Patent Acts for infringement remedies."},
    ],
    r"Real Estate|RERA|builder|buyer|possession|allotment|Section 18": [
        {"act": "Real Estate (Regulation and Development) Act, 2016 (RERA)", "suggestion": "For property disputes between builders and buyers, RERA provides a specialized framework for compensation and timely possession."},
    ]
}

def suggest_legal_acts(text):
    """
    Analyzes the provided text and suggests relevant Indian legal acts/sections.
    """
    if not text:
        return []

    suggestions = []
    seen_acts = set()

    for pattern, acts in LEGAL_MAP.items():
        if re.search(pattern, text, re.IGNORECASE):
            for act_info in acts:
                if act_info["act"] not in seen_acts:
                    suggestions.append(act_info)
                    seen_acts.add(act_info["act"])

    # Default suggestion if no specific act is matched but it looks like a legal document
    if not suggestions and len(text.strip()) > 100:
        suggestions.append({
            "act": "General Legal Reference",
            "suggestion": "No specific Act was identified. Please manually review the document for procedural relevance to local and national laws."
        })

    return suggestions
