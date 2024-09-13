import gradio as gr
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from langdetect import detect
import re

#  tokenizer تحميل النموذج والـ    
model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

# قائمة بأكواد اللغات والأسماء
language_options = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic": "ar",
}

#  دالة لترجمة الجمل
def translate_sentence(sentence, tgt_lang):
    encoded_text = tokenizer(sentence, return_tensors="pt")
    generated_tokens = model.generate(encoded_text["input_ids"], forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translation

#  دالة لترجمة المقال كاملاً
def translate_article(article, tgt_lang):
    paragraphs = re.split(r'([\r\n]+)', article)                               
    for i, p in enumerate(paragraphs):
        if len(p.strip()) == 0:
            continue
        paragraphs[i] = translate_paragraph(p, tgt_lang)
    return ''.join(paragraphs)

#  دالة لترجمة الفقرات
def translate_paragraph(paragraph, tgt_lang):
    sentences = []
    cursor = 0
    for i, c in enumerate(paragraph):
        if c == '.':
            sentences.append(paragraph[cursor:i + 1])
            cursor = i + 1
    if paragraph and paragraph[-1] != '.':
        sentences.append(paragraph[cursor:])

    # ترجمة الجمل المجمعة في الفقرة
    return ' '.join(translate_sentence(s, tgt_lang) for s in sentences)

# دالة الكشف عن اللغة والترجمة إلى لغات متعددة
def detect_and_translate_multiple(text, tgt_langs):
    detected_lang = detect(text)
    src_lang_code = detected_lang if detected_lang in language_options.values() else "en"
    tokenizer.src_lang = src_lang_code

    translations = {}
    for tgt_lang in tgt_langs:
        translations[tgt_lang] = translate_article(text, language_options[tgt_lang])

    return "\n\n".join([f"{lang}: {translations[lang]}" for lang in translations])

# دالة لقراءة محتوى الملف النصي فقط
def translate_file_in_chunks(file, tgt_langs, chunk_size=2000):
    translations = []
    try:
        # قراءة الملف النصي فقط
        with open(file.name, "r", encoding="utf-8") as f:
            content = f.read()

        # ترجمة المحتوى
        translation = detect_and_translate_multiple(content, tgt_langs)
        translations.append(translation)

        return "\n\n".join(translations)
    except Exception as e:
        return f"Error during file translation: {str(e)}"

# واجهة Gradio
with gr.Blocks() as interface:
    gr.Markdown("## Text Translation with Auto Language Detection (Multiple Outputs)")

    # مكونات الإدخال: مربع نص، قائمة منسدلة متعددة الاختيارات للغات الهدف
    with gr.Row(): #Fixed indentation
        input_text = gr.Textbox(label="Input Text")
        file_input = gr.File(label="Upload Text File (.txt)")  # دعم فقط لملفات TXT

    tgt_langs = gr.CheckboxGroup(list(language_options.keys()), label="Target Languages", value=["English"])

    # مكون الإخراج: نتيجة الترجمة
    output_text = gr.Textbox(label="Translated Text")

    # زر الترجمة للنص المُدخل يدويًا
    translate_button = gr.Button("Translate Text")

    # زر الترجمة للملف المُحمل
    translate_file_button = gr.Button("Translate File")

    # تحديد ما يحدث عند الضغط على زر الترجمة للنص المُدخل
    translate_button.click(
        detect_and_translate_multiple,
        inputs=[input_text, tgt_langs],
        outputs=output_text
    )

    # تحديد ما يحدث عند الضغط على زر الترجمة للملف المُحمل
    translate_file_button.click(
        translate_file_in_chunks,
        inputs=[file_input, tgt_langs],
        outputs=output_text
    )

# تشغيل الواجهة
interface.launch()
