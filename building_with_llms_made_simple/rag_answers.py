"""Answers for 03_rag.py notebook."""

import re

import llamabot as lmb


@lmb.prompt("system")
def rag_bot_sysprompt():
    """Generate the system prompt for the RAG bot.

    :return: A system prompt that instructs the bot to:
        - Be a helpful programming language assistant
        - Answer questions based only on provided documents
        - Acknowledge uncertainty when present
        - Keep responses concise and focused
    """
    return """You are a helpful programming language assistant.
    You will be provided documents to answer questions.
    Answer questions solely based on the provided documents
    and not your background knowledge.
    If you're not sure about something, say so.
    Keep your responses concise and focused on the question asked.
    """


def create_knowledge_store():
    """Create and initialize a knowledge store for document storage.

    :return: A LanceDB document store configured for storing the knowledge base
        with table name "knowledge_base". The store is reset before being returned
        to ensure a clean state.
    """
    # Create document stores
    knowledge_store = lmb.LanceDBDocStore(
        table_name="knowledge_base",
    )
    knowledge_store.reset()
    return knowledge_store


def create_memory_store():
    """Create and initialize a memory store for conversation history.

    :return: A LanceDB document store configured for storing conversation memory
        with table name "memory". The store is reset before being returned to
        ensure a clean state.
    """
    memory_store = lmb.LanceDBDocStore(
        table_name="memory",
    )
    memory_store.reset()
    return memory_store


def create_rag_bot(
    knowledge_store: lmb.LanceDBDocStore, memory_store: lmb.LanceDBDocStore
):
    """Create a RAG bot configured with knowledge and memory stores.

    :param knowledge_store: The document store containing the knowledge base
        for answering questions.
    :param memory_store: The document store for maintaining conversation history.
    :return: A configured RAG bot that can answer questions based on the provided
        knowledge store and maintain conversation context using the memory store.
    """
    rag_bot = lmb.QueryBot(
        system_prompt=rag_bot_sysprompt(),
        docstore=knowledge_store,
        memory=memory_store,
        model_name="ollama_chat/llama3.1",
        temperature=0.0,  # Keep responses deterministic
    )
    return rag_bot


def insert_delimiter(text: str, level: int = 1, delim: str = "|||SECTION|||") -> str:
    """Insert delimiters before section headers at a specified level.

    For a given level K, this function:

    1. Adds delimiters to all sections whose own level is from 1 to K.
    2. Crucially, if a section (e.g., "1.2.3") gets a delimiter because its
       level is <= K, then all its parent sections ("1." and "1.2" in this
       example) will also get a delimiter, regardless of whether K would
       have independently selected them.
    3. Places delimiters before section numbers, preserving original formatting.

    For example, if level=2:

    - If we see "1. Title", its level is 1. Since 1 <= 2, "1." gets a delimiter.
    - If we see "1.1 Title", its level is 2. Since 2 <= 2, "1.1" gets a delimiter.
      Its parent "1." also gets a delimiter.
    - If we see "1.1.1 Title", its level is 3. Since 3 > 2, "1.1.1" does NOT get
      a delimiter, and this line does not cause "1." or "1.1" to get delimiters
      if they wouldn't have otherwise.

    :param text: The text to process.
    :param level: The maximum section depth (K) to consider for adding delimiters.
        Sections up to this depth, and their parents, will be marked.
    :param delim: The delimiter string to insert.
    :return: The text with delimiters inserted according to the rules.
    """
    # First, remove any existing delimiters to prevent duplication
    text = text.replace(delim, "")

    lines = text.split("\n")
    result_lines = []

    # Pass 1: Identify all canonical section numbers that need delimiters
    sections_to_delim = set()
    for line_content in lines:
        match = re.match(r"^[ \t]*(\d+(?:\.\d+)*\.?)\s", line_content)
        if match:
            section_num_raw = match.group(1)  # e.g., "1.", "1.1", "1.1.1"

            # Normalize by removing trailing dot for consistent processing
            cleaned_section_num = section_num_raw.rstrip(
                "."
            )  # e.g., "1", "1.1", "1.1.1"

            parts = cleaned_section_num.split(".")
            current_section_level = len(parts)

            if current_section_level <= level:
                # Add this section and all its parents to the set
                for i in range(len(parts)):
                    parent_canonical_num = ".".join(parts[: i + 1])
                    sections_to_delim.add(parent_canonical_num)

    # Pass 2: Add delimiters to the identified sections
    for line_content in lines:
        match = re.match(r"^[ \t]*(\d+(?:\.\d+)*\.?)\s", line_content)
        if match:
            section_num_raw = match.group(1)  # e.g., "1.", "1.1"
            cleaned_section_num = section_num_raw.rstrip(".")  # e.g., "1", "1.1"

            if cleaned_section_num in sections_to_delim:
                # Use regex to insert delimiter while preserving leading whitespace
                # and full section number
                # The pattern matches:
                # (leading whitespace)(section_number_with_optional_dot
                # and_trailing_space)
                # This ensures we re-insert the original section number format
                # from the line.
                line_content = re.sub(
                    r"^([ \t]*)((?:\d+(?:\.\d+)*\.?)\s)",
                    r"\1" + delim + r" \2",
                    line_content,
                    count=1,
                )  # Apply only once per line
        result_lines.append(line_content)

    return "\n".join(result_lines)


lab_protocol_text = """
1.	Purpose
1.1 The purpose of this standard operating procedure (SOP) is to outline a generic workflow for routine laboratory analyses.
1.1.1 This document is intended as a template to demonstrate hierarchical formatting up to three levels, facilitating chunking for large language models.
1.1.2 It does not describe a specific analytical technique; users should replace placeholder text with details applicable to their own assays.
1.2 By following this SOP, laboratory personnel will ensure consistency, traceability, and compliance with basic quality requirements.
2.	Scope
2.1 This SOP applies to all laboratory staff who perform routine sample preparation, measurement, and data recording activities.
2.1.1 It covers general responsibilities, materials, procedural steps, data management, and safety considerations.
2.1.2 Specialized or highly regulated techniques (e.g., radioactive work, GLP studies) are outside the scope of this document.
2.2 The SOP is suitable for use in academic, industrial, or regulatory research settings where a generic framework is acceptable.
3.	Responsibilities
3.1 Laboratory manager
3.1.1 Review and approve any modifications to this SOP.
3.1.2 Ensure that all staff are trained on the current version.
3.1.3 Conduct periodic audits to confirm adherence.
3.2 Laboratory technician
3.2.1 Follow the procedural steps as written.
3.2.2 Document any deviations or unexpected observations in the laboratory notebook.
3.2.3 Report equipment malfunctions to the laboratory manager immediately.
4.	Materials and equipment
4.1 Reagents
4.1.1 Placeholder buffer solution (e.g., 0.1 M phosphate buffer, pH 7.4).
4.1.2 Calibration standards appropriate for the chosen analytical method.
4.1.3 Deionized water (Type I, <18 MΩ·cm).
4.2 Consumables
4.2.1 Disposable pipette tips (various sizes).
4.2.2 Sample vials or tubes (e.g., 2 mL microcentrifuge tubes).
4.2.3 Laboratory gloves (nitrile or latex, depending on compatibility).
4.3 Equipment
4.3.1 Analytical instrument (e.g., spectrophotometer, chromatography system).
4.3.2 Calibrated balance capable of at least 0.1 mg readability.
4.3.3 Vortex mixer and centrifuge.
4.3.4 Computer workstation with data acquisition software.
5.	Procedure
5.1 Sample preparation
5.1.1 Verify sample identification
5.1.1.1 Confirm that each sample is labeled with a unique identifier (e.g., "SMP-001").
5.1.1.2 Cross-check the sample list in the laboratory information management system (LIMS).
5.1.2 Prepare reagents
5.1.2.1 Retrieve reagents from storage; inspect expiration dates.
5.1.2.2 Prepare working solutions according to manufacturer instructions.
5.1.3 Aliquot samples
5.1.3.1 Pipette the required volume of each sample into a clean tube.
5.1.3.2 If necessary, dilute samples using the placeholder buffer to fall within the calibration range.
5.2 Instrument calibration and setup
5.2.1 Power on the instrument and allow it to warm up for at least 15 minutes.
5.2.2 Perform daily verification using calibration standards.
5.2.2.1 Load the calibration standard.
5.2.2.2 Confirm that the instrument response is within predefined acceptance criteria.
5.2.3 Configure analysis parameters
5.2.3.1 Open the data acquisition software.
5.2.3.2 Select the method file or input method details (e.g., wavelength, flow rate).
5.3 Sample analysis
5.3.1 Place prepared samples in the sample tray or autosampler.
5.3.2 Begin the run sequence according to predefined sample order.
5.3.2.1 Monitor the first few injections or readings to verify stable performance.
5.3.2.2 If abnormalities are detected, pause the run and troubleshoot per Section 7.
5.3.3 Record raw data files in the designated project folder on the laboratory server.
5.3.4 At the end of the sequence, run a system blank to check for carryover.
6.	Data management
6.1 Data recording
6.1.1 Transfer measurement results from the instrument to the LIMS or electronic notebook.
6.1.2 Annotate each data entry with date, operator initials, and instrument ID.
6.1.3 Note any deviations from standard operating conditions (e.g., pump pressure fluctuations).
6.2 Data backup and storage
6.2.1 Save raw data and processed results to a secure network drive.
6.2.2 Maintain a local backup on an external hard drive, if required by institutional policy.
6.2.3 Retain data for at least five years or as dictated by regulatory guidelines.
7.	Safety and quality control
7.1 General safety precautions
7.1.1 Always wear appropriate personal protective equipment (PPE), including lab coat, gloves, and safety glasses.
7.1.2 Refer to material safety data sheets (MSDS) for all reagents at https://www.osha.gov/laboratory-safety.
7.1.3 Maintain a clean work area; immediately clean any spills using appropriate disinfectants.
7.2 Equipment maintenance
7.2.1 Perform weekly checks on critical components (e.g., lamp alignment, pump seals).
7.2.1.1 Document maintenance activities in the instrument logbook.
7.2.1.2 Replace consumables (e.g., septa, tubing) as recommended by the manufacturer.
7.2.2 If the instrument fails calibration for more than two consecutive days, remove it from service and notify the equipment administrator.
8.	References
8.1 Internal documents
8.1.1 Laboratory handbook – Version 3.0 (last updated January 2025).
8.1.2 Instrument user manual (Model ABC-123, Document No. XYZ-789).
8.2 External standards
8.2.1 ISO 17025:2017 – General requirements for the competence of testing and calibration laboratories.
8.2.2 Good Laboratory Practice (GLP) guidelines, U.S. FDA (https://www.fda.gov).
9.	Revision history
9.1 Revision 0 (June 1, 2025)
9.1.1 Initial creation of dummy SOP for LLM chunking demonstration.
9.1.2 Hierarchical numbering tested up to three levels.
9.2 Future revisions
9.2.1 Any updates should include date, author, and a brief description of changes.
"""  # noqa: E501

cleaning_protocol_text = """
1.	Purpose
1.1 The purpose of this standard operating procedure (SOP) is to establish a comprehensive cleaning and sanitization protocol for manufacturing equipment and facilities.
1.1.1 This document outlines the procedures for maintaining a clean and sanitized manufacturing environment.
1.1.2 It ensures compliance with current Good Manufacturing Practices (cGMP) and regulatory requirements.
1.2 This SOP helps prevent cross-contamination and ensures product quality and safety.
2.	Scope
2.1 This SOP applies to all manufacturing areas, equipment, and surfaces that come into contact with products.
2.1.1 It covers routine cleaning, sanitization, and disinfection procedures.
2.1.2 It includes both manual and automated cleaning processes.
2.2 The SOP is applicable to all manufacturing personnel, cleaning staff, and quality control personnel.
3.	Responsibilities
3.1 Manufacturing Manager
3.1.1 Ensure proper implementation of cleaning procedures.
3.1.2 Review and approve cleaning validation protocols.
3.1.3 Monitor cleaning effectiveness through regular audits.
3.2 Cleaning Staff
3.2.1 Execute cleaning procedures as specified.
3.2.2 Document cleaning activities in cleaning logs.
3.2.3 Report any cleaning-related issues immediately.
4.	Materials and Equipment
4.1 Cleaning Agents
4.1.1 Approved cleaning detergents (e.g., CIP-100, Alkaline Cleaner).
4.1.2 Sanitizing solutions (e.g., 70% Isopropyl Alcohol, Quaternary Ammonium Compounds).
4.1.3 Deionized water (Type I, <18 MΩ·cm).
4.2 Cleaning Tools
4.2.1 Dedicated cleaning brushes and mops.
4.2.2 Color-coded cleaning cloths.
4.2.3 Non-shedding wipes.
4.3 Equipment
4.3.1 Automated cleaning systems (CIP/SIP).
4.3.2 Pressure washers and steam cleaners.
4.3.3 Cleaning validation test kits.
5.	Procedure
5.1 Pre-cleaning Assessment
5.1.1 Identify cleaning requirements
5.1.1.1 Review product contact surfaces.
5.1.1.2 Determine appropriate cleaning agents.
5.1.2 Prepare cleaning area
5.1.2.1 Remove or protect sensitive equipment.
5.1.2.2 Post appropriate warning signs.
5.2 Cleaning Process
5.2.1 Initial cleaning
5.2.1.1 Remove gross contamination.
5.2.1.2 Apply appropriate cleaning agent.
5.2.2 Detailed cleaning
5.2.2.1 Clean all surfaces thoroughly.
5.2.2.2 Pay special attention to hard-to-reach areas.
5.3 Sanitization
5.3.1 Apply sanitizing solution
5.3.1.1 Use approved sanitizing agents.
5.3.1.2 Follow contact time requirements.
5.3.2 Final rinse
5.3.2.1 Rinse with purified water.
5.3.2.2 Verify no cleaning agent residues.
6.	Documentation
6.1 Cleaning Records
6.1.1 Document cleaning activities in cleaning logs.
6.1.2 Record cleaning agent concentrations and contact times.
6.1.3 Note any deviations or issues.
6.2 Validation Records
6.2.1 Maintain cleaning validation protocols.
6.2.2 Document test results and acceptance criteria.
6.2.3 Keep records for required retention period.
7.	Quality Control
7.1 Visual Inspection
7.1.1 Verify cleanliness of all surfaces.
7.1.2 Check for any residues or stains.
7.2 Microbiological Testing
7.2.1 Perform surface swab tests.
7.2.2 Monitor air quality in clean areas.
7.2.3 Document test results.
8.	References
8.1 Internal Documents
8.1.1 Cleaning Validation Master Plan.
8.1.2 Equipment Cleaning Logs.
8.2 External Standards
8.2.1 FDA cGMP Guidelines.
8.2.2 ISO 14644 Cleanroom Standards.
9.	Revision History
9.1 Revision 0 (June 1, 2025)
9.1.1 Initial creation of cleaning protocol.
9.1.2 Established basic cleaning procedures.
9.2 Future Revisions
9.2.1 Updates to be made as needed based on regulatory changes or process improvements.
"""  # noqa: E501

quality_control_protocol_text = """
1.	Purpose
1.1 The purpose of this standard operating procedure (SOP) is to establish specific quality control testing procedures for pharmaceutical tablet products.
1.1.1 This document outlines the exact methods, equipment, and acceptance criteria for tablet testing.
1.1.2 It ensures compliance with USP <711> Dissolution, USP <905> Uniformity of Dosage Units, and USP <1217> Tablet Breaking Force.
1.2 This SOP maintains product quality standards for immediate-release tablet formulations.
2.	Scope
2.1 This SOP applies to all immediate-release tablet products manufactured in Facility A.
2.1.1 It covers physical testing (hardness, friability, disintegration), chemical testing (assay, content uniformity, dissolution), and microbiological testing (bioburden, endotoxin).
2.1.2 It includes stability testing at 25°C/60%RH, 30°C/65%RH, and 40°C/75%RH conditions.
2.2 The SOP is applicable to quality control laboratory personnel and manufacturing staff in the tablet production department.
3.	Responsibilities
3.1 Quality Control Manager
3.1.1 Review and approve all test results exceeding ±5% of target values.
3.1.2 Authorize method modifications and equipment calibration schedules.
3.1.3 Lead out-of-specification (OOS) investigations when results exceed USP limits.
3.2 Quality Control Technicians
3.2.1 Perform testing using calibrated equipment within 24 hours of sample receipt.
3.2.2 Document all test results in the Laboratory Information Management System (LIMS).
3.2.3 Maintain equipment calibration records and perform daily system suitability tests.
4.	Materials and Equipment
4.1 Physical Testing Equipment
4.1.1 Tablet Hardness Tester (Pharma Test PTB 311E, calibrated monthly)
4.1.2 Friability Tester (Erweka TAR 10, calibrated quarterly)
4.1.3 Disintegration Tester (Erweka ZT 3, calibrated quarterly)
4.2 Chemical Testing Equipment
4.2.1 HPLC System (Agilent 1260 Infinity II, calibrated monthly)
4.2.2 UV-Vis Spectrophotometer (PerkinElmer Lambda 35, calibrated monthly)
4.2.3 Dissolution Apparatus (Agilent 708-DS, calibrated quarterly)
4.3 Reference Materials
4.3.1 USP Reference Standards (stored at 2-8°C)
4.3.2 Working Standards (prepared monthly)
4.3.3 System Suitability Solutions (prepared daily)
5.	Procedure
5.1 Physical Testing
5.1.1 Tablet Hardness
5.1.1.1 Test 10 tablets from each batch
5.1.1.2 Acceptance criteria: 4-8 kp (kiloponds)
5.1.2 Friability Testing
5.1.2.1 Test 20 tablets for 4 minutes at 25 rpm
5.1.2.2 Acceptance criteria: ≤1.0% weight loss
5.1.3 Disintegration Testing
5.1.3.1 Test 6 tablets in 900mL purified water at 37°C
5.1.3.2 Acceptance criteria: ≤15 minutes
5.2 Chemical Testing
5.2.1 Assay Testing
5.2.1.1 Prepare sample solution in mobile phase (0.1% TFA in water:acetonitrile 70:30)
5.2.1.2 Run HPLC method: Column: C18, 250mm x 4.6mm, 5μm
5.2.1.3 Flow rate: 1.0 mL/min, Detection: 254nm
5.2.1.4 Acceptance criteria: 95.0-105.0% of label claim
5.2.2 Content Uniformity
5.2.2.1 Test 10 individual tablets
5.2.2.2 Acceptance criteria: Each unit 85.0-115.0% of label claim
5.2.3 Dissolution Testing
5.2.3.1 Apparatus: USP Apparatus 2 (Paddle), 50 rpm
5.2.3.2 Medium: 900mL 0.1N HCl, 37°C
5.2.3.3 Test 12 tablets, sample at 15, 30, 45, and 60 minutes
5.2.3.4 Acceptance criteria: Q=80% at 30 minutes
6.	Documentation
6.1 Test Records
6.1.1 Record all raw data in bound notebooks (pre-numbered pages)
6.1.2 Document instrument parameters, calibration status, and environmental conditions
6.1.3 Include chromatograms, spectra, and dissolution profiles
6.2 Certificate of Analysis
6.2.1 Include batch number, manufacturing date, and expiry date
6.2.2 List all test results with acceptance criteria
6.2.3 Require signatures from analyst, reviewer, and QC manager
7.	Quality Assurance
7.1 Method Validation
7.1.1 Specificity: Resolution ≥2.0 between peaks
7.1.2 Linearity: R²≥0.999 over 50-150% of target concentration
7.1.3 Accuracy: 98.0-102.0% recovery
7.1.4 Precision: RSD≤2.0% for six replicates
7.2 Out-of-Specification Investigation
7.2.1 Phase 1: Laboratory investigation (24 hours)
7.2.2 Phase 2: Full-scale investigation (5 business days)
7.2.3 Phase 3: CAPA implementation (10 business days)
8.	References
8.1 Internal Documents
8.1.1 Quality Manual (QM-001, Rev. 5)
8.1.2 Test Method Procedures (TMP-001 through TMP-010)
8.2 External Standards
8.2.1 USP <711> Dissolution
8.2.2 USP <905> Uniformity of Dosage Units
8.2.3 USP <1217> Tablet Breaking Force
9.	Revision History
9.1 Revision 0 (June 1, 2025)
9.1.1 Initial creation of tablet testing protocol
9.1.2 Established specific acceptance criteria
9.2 Future Revisions
9.2.1 Updates to be made as needed based on regulatory changes or process improvements
"""  # noqa: E501
