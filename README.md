# Text-Translation
This project provides a simple interface for translating text using the M2M100 model by Facebook AI, with automatic detection of the input language. The user can input text or upload a file and translate the content into multiple  languages.

- ## Models Used
- **Model**: `facebook/m2m100_418M`
  - **Purpose**: Multilingual translation.
  - **Tokenizer**: `M2M100Tokenizer` used for tokenizing the input text into tokens that the model can process.
  - **Framework**: PyTorch.

## Features

- **Automatic language detection**: Detects the input language and translates it accordingly.
- **Multiple output languages**: Supports English, French, Spanish, German and Arabic.
- **File support**: Upload `.txt` or `.pdf` files for translation.
- **Gradio interface**: Simple web-based interface using Gradio.


  - ## Requirements
  - **You need to have the following libraries installed:**

transformers (for Hugging Face model)
langdetect (for language detection)
gradio (for building the UI)
pdfplumber (for reading PDF files)

*You can install the requirements with:*
pip install transformers langdetect gradio pdfplumber

 **How to Run the Project:**
you can use the link below for hugging face 
or you can download the script

 **Usage:**
 1. Input Text:  You can type the text you want to translate in the text box.
 2. Upload File: Or you can upload a TXT or PDF file containing the text you want to translate.
 3. Select Target Languages:  Choose the languages ​​you want to translate the text to.
 4. Translation Output: The translation will appear in the dedicated box once the process is complete.
 5. Supported Formats: Text files (TXT) and PDF files are supported in the project.

**Example:**
*Input:*
Hello, how are you?

*Target Languages:*
Arabic, Spanish, French, German

*Output*
Arabic: مرحبا، كيف حالك؟
Spanish: Hola, ¿cómo te sientes?
French: Bonjour, comment vous êtes-vous?
German: Hallo, wie bist du?


**Known Issues**
Large files may affect performance.

**Performance Tips**
If there is a slowdown in translation, you can use cloud computing services or GPU to speed up performance.


## Demo

You can try out the project live on Hugging Face Spaces:
[Demo on Hugging Face](https://huggingface.co/spaces/Yaz1-e/Project_1)



